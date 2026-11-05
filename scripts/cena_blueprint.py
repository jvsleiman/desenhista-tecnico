#!/usr/bin/env python3
"""Construtor de pranchas no estilo Blueprint a partir de JSON — sem escrever gerador próprio.

  cena_blueprint.py --api              lista as peças e parâmetros
  cena_blueprint.py --exemplo-json     mostra um JSON completo de exemplo
  cena_blueprint.py prancha.json saida gera saida.svg e saida.html

JSON:
{
 "tela": [largura, altura, ox, oy, escala],          # origem isométrica e escala do mundo
 "fig": "FIG_001", "nome": "SSD M.2 2280, 2026",       # moldura editorial
 "titulo": "...", "subtitulo": "...", "legenda": "frase da página HTML",
 "pecas": [["caixa", x, y, z, w, d, h, {"faces": "padrao|branco|destaque|corte"}], ...],   # de trás para frente
 "chamadas": [{"texto": "CONTROLADOR", "detalhe": ["linha 1", "linha 2"], "alvo": [x, y, z], "lado": "esq"}, ...],
 "colunas": [x_esq, x_dir]                             # opcional: onde ficam as colunas de chamadas
}
As chamadas são distribuídas sozinhas em colunas à esquerda e à direita, sem sobrepor, com guias que não se cruzam.
Peças 2D (plantas): ret, circ, linha2d, cota, hachura, texto, carimbo — coordenadas em pixels da prancha.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iso import proj, pts, box, cyl  # noqa: E402

MONO = "'Departure Mono','IBM Plex Mono',ui-monospace,monospace"
CSS = """
.bp .traco{fill:none;stroke:#0043ff;stroke-width:1.25;stroke-linejoin:round;stroke-linecap:round}
.bp .fino{fill:none;stroke:#0043ff;stroke-width:.75}
.bp .grosso{fill:none;stroke:#0043ff;stroke-width:1.5;stroke-linejoin:round}
.bp .oculta{fill:none;stroke:#0043ff;stroke-width:1;stroke-dasharray:4 2}
.bp .centro{fill:none;stroke:#0043ff;stroke-width:.75;stroke-dasharray:10 2 2 2}
.bp .construcao{fill:none;stroke:#0043ff;stroke-width:.75;stroke-dasharray:3 3;opacity:.7}
.bp .topo{fill:#e6ebff;stroke:#0043ff;stroke-width:1.25;stroke-linejoin:round}
.bp .esq{fill:#f4f5f9;stroke:#0043ff;stroke-width:1.25;stroke-linejoin:round}
.bp .dir{fill:#97acff;stroke:#0043ff;stroke-width:1.25;stroke-linejoin:round}
.bp .branco{fill:#ffffff;stroke:#0043ff;stroke-width:1.25;stroke-linejoin:round}
.bp .sombra{fill:#b6c8ff;stroke:#0043ff;stroke-width:1.25;stroke-linejoin:round}
.bp .solido{fill:#0043ff;stroke:#0043ff;stroke-width:1}
.bp .corte{fill:url(#hachura);stroke:#0043ff;stroke-width:1.25}
.bp .vazio{fill:#fbfbfb;stroke:#0043ff;stroke-width:1.25}
.bp .guia{fill:none;stroke:#103dff;stroke-width:.75}
.bp .ponto{fill:#103dff}
.bp .chamada{fill:#103dff;font-size:12px}
.bp .detalhe{fill:#7d7d7d;font-size:10px}
.bp .fig{fill:#7d7d7d;font-size:10px}
.bp .titulo{fill:#103dff;font-size:16px}
.bp .cota{fill:none;stroke:#7d7d7d;stroke-width:.75}
.bp .cota-txt{fill:#103dff;font-size:10px}
.bp .rot{fill:#103dff;font-size:11px}
.bp .moldura{fill:none;stroke:#e1e1e1;stroke-width:1}
"""
DEFS = """<defs>
<pattern id="grade" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#0043ff" fill-opacity=".18"/></pattern>
<pattern id="hachura" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#e6ebff"/><line x1="0" y1="0" x2="0" y2="6" stroke="#b6c8ff" stroke-width="2"/></pattern>
<marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9" fill="none" stroke="#0043ff" stroke-width="1.4"/></marker>
<marker id="seta-cota" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,2 L10,5 L0,8 Z" fill="#7d7d7d"/></marker>
</defs>"""

FACES = {  # (topo, esquerda, direita)
    "padrao": ("topo", "esq", "dir"),
    "branco": ("branco", "esq", "dir"),
    "destaque": ("topo", "esq", "solido"),
    "corte": ("corte", "corte", "corte"),
    "sombra": ("sombra", "esq", "dir"),
}


def _t(x, y, txt, cls, anchor="start", extra=""):
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}"{extra}>{html.escape(str(txt))}</text>'


class Prancha:
    def __init__(self, largura=960, altura=640, ox=480, oy=320, escala=1.0):
        self.w, self.h, self.ox, self.oy, self.s = largura, altura, ox, oy, escala
        self.camadas = []
        self.vx, self.vy, self.k = 0.0, 0.0, 1.0  # vista 2D ativa: origem em px e px por mm

    def _v(self, x, y):
        return round(self.vx + x * self.k, 1), round(self.vy + y * self.k, 1)

    def vista(self, x, y, mm=1.0, titulo="", titulo_dy=None):
        """Abre uma vista 2D: a partir daqui ret/circ/linha2d/cota/chamada2d/texto usam MILÍMETROS com origem
        (0,0) no canto superior esquerdo da vista, posicionada em (x, y) px; `mm` = px por mm (use o mesmo em
        todas as vistas). `titulo` é escrito centralizado abaixo da vista na próxima chamada a fim_vista."""
        self.vx, self.vy, self.k = x, y, mm
        self._titulo_vista = (titulo, titulo_dy)
        self._ext = [0, 0]

    def fim_vista(self, largura_mm, altura_mm):
        """Escreve o título da vista aberta, centralizado sob a largura dada, e volta às coordenadas em px."""
        titulo, dy = getattr(self, "_titulo_vista", ("", None))
        if titulo:
            cx, by = self._v(largura_mm / 2, altura_mm)
            self.camadas.append(_t(cx, by + (dy if dy is not None else 44), titulo, "rot", "middle"))
        self.vx, self.vy, self.k = 0.0, 0.0, 1.0

    def p(self, x, y, z):
        return proj(x, y, z, self.ox, self.oy, self.s)

    # ---------- isométrico ----------
    def caixa(self, x, y, z, w, d, h, faces="padrao"):
        """Caixa de canto vivo. faces: padrao | branco | destaque | sombra | corte."""
        t, e, dr = FACES[faces]
        svg = box(x, y, z, w, d, h, self.ox, self.oy, self.s)
        svg = svg.replace('class="esq"', f'class="{e}"').replace('class="dir"', f'class="{dr}"').replace('class="topo"', f'class="{t}"')
        self.camadas.append(svg)

    def cilindro(self, cx, cy, z, r, h, faces="padrao"):
        """Cilindro vertical (prato, botão, capacitor, parafuso)."""
        t, _, dr = FACES[faces]
        self.camadas.append(cyl(cx, cy, z, r, h, self.ox, self.oy, self.s)
                            .replace('class="dir"', f'class="{dr}"').replace('class="topo"', f'class="{t}"'))

    def guias(self, x, y, z, w, d, h, ate):
        """Guias tracejadas de vista explodida nos 4 cantos, do topo da peça (z+h) até a altura `ate`."""
        for a, b in [(x, y), (x + w, y), (x + w, y + d), (x, y + d)]:
            (x1, y1), (x2, y2) = self.p(a, b, z + h), self.p(a, b, ate)
            self.camadas.append(f'<line class="construcao" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')

    def guia(self, de, ate):
        """Uma guia tracejada entre dois pontos 3D [x,y,z]."""
        (x1, y1), (x2, y2) = self.p(*de), self.p(*ate)
        self.camadas.append(f'<line class="construcao" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')

    def plano(self, pontos, z, cls="topo"):
        """Polígono deitado no plano z (pegada de chip, área marcada). pontos = [[x,y], ...]. cls: topo|sombra|branco|corte|vazio|fino|construcao."""
        self.camadas.append(f'<polygon class="{cls}" points="{pts([self.p(a, b, z) for a, b in pontos])}"/>')

    def poli3d(self, pontos, cls="esq"):
        """Polígono 3D preenchido numa face qualquer (triângulo de mão-francesa, chanfro). pontos = [[x,y,z], ...]."""
        self.camadas.append(f'<polygon class="{cls}" points="{pts([self.p(*q) for q in pontos])}"/>')

    def furo(self, cx, cy, cz, r, plano="xy", cls="vazio"):
        """Furo/círculo isométrico (elipse) numa face: plano "xy" (topo), "xz" (face de y constante) ou "yz" (face de x constante)."""
        import math
        q = []
        for i in range(24):
            a, b = r * math.cos(i * math.pi / 12), r * math.sin(i * math.pi / 12)
            q.append({"xy": (cx + a, cy + b, cz), "xz": (cx + a, cy, cz + b), "yz": (cx, cy + a, cz + b)}[plano])
        self.poli3d(q, cls)

    def linha3d(self, pontos, cls="fino"):
        """Polilinha 3D (trilhas, contatos, riscos). pontos = [[x,y,z], ...]. cls: traco|fino|construcao."""
        self.camadas.append(f'<polyline class="{cls}" points="{pts([self.p(*q) for q in pontos])}"/>')

    def cabo(self, pontos, rotulo="", tracejado=False, seta=True, z=0):
        """Ligação de diagrama no plano do chão: pontos [[x,y], ...] seguindo os eixos X/Y, com seta no fim e
        rótulo mono opcional (ex. '01 FIBRA') sobre fundo de papel no meio do maior trecho.
        Termine o cabo na borda da peça de destino (não no centro), para a seta não sumir embaixo dela."""
        pp = [self.p(a, b, z) for a, b in pontos]
        cls = "traco" + ('" stroke-dasharray="4 3' if tracejado else "")
        mk = ' marker-end="url(#seta)"' if seta else ""
        self.camadas.append(f'<polyline class="{cls}" points="{pts(pp)}"{mk}/>')
        if rotulo:
            i = max(range(len(pp) - 1), key=lambda k: abs(pp[k + 1][0] - pp[k][0]) + abs(pp[k + 1][1] - pp[k][1]))
            mx, my = (pp[i][0] + pp[i + 1][0]) / 2, (pp[i][1] + pp[i + 1][1]) / 2
            larg = 6.2 * len(rotulo) + 8
            self.camadas.append(f'<rect x="{mx - larg / 2:.1f}" y="{my - 8:.1f}" width="{larg:.1f}" height="14" fill="#fbfbfb"/>'
                                + _t(mx, my + 3, rotulo, "rot", "middle"))

    def grupo(self, x, y, w, d, nome="", z=0):
        """Agrupamento (VLAN, rede, máquina física): contorno tracejado cinza no chão com o nome no canto de trás."""
        q = [self.p(x, y, z), self.p(x + w, y, z), self.p(x + w, y + d, z), self.p(x, y + d, z)]
        self.camadas.append(f'<polygon points="{pts(q)}" fill="none" stroke="#7d7d7d" stroke-width=".75" stroke-dasharray="4 3"/>')
        if nome:
            self.camadas.append(_t(q[0][0], q[0][1] - 6, nome, "fig", "middle"))

    def passos(self, x, y, linhas, titulo="PASSOS"):
        """Legenda numerada de passos (diagramas que contam uma sequência), em px."""
        out = [_t(x, y, titulo, "fig")]
        for i, l in enumerate(linhas):
            out.append(_t(x, y + 18 + 15 * i, l, "rot"))
        self.camadas.append("\n".join(out))

    def listras(self, x, y, z, w, d, n, eixo="x", cls="fino"):
        """n riscos paralelos no topo de uma área (contatos dourados, ventilação, código de barras)."""
        for i in range(n):
            f = (i + .5) / n
            if eixo == "x":
                a, b = self.p(x + w * f, y, z), self.p(x + w * f, y + d, z)
            else:
                a, b = self.p(x, y + d * f, z), self.p(x + w, y + d * f, z)
            self.camadas.append(f'<line class="{cls}" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')

    def cota_iso(self, de, ate, texto, desloca=(0, 0, 0)):
        """Cota ao longo de uma aresta 3D, deslocada por `desloca` [dx,dy,dz] no mundo."""
        a = [de[i] + desloca[i] for i in range(3)]
        b = [ate[i] + desloca[i] for i in range(3)]
        (x1, y1), (x2, y2) = self.p(*a), self.p(*b)
        self.camadas.append(f'<line class="cota" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-start="url(#seta-cota)" marker-end="url(#seta-cota)"/>')
        import math
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        if ang > 90 or ang < -90:
            ang += 180
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        self.camadas.append(_t(mx, my - 5, texto, "cota-txt", "middle", f' transform="rotate({ang:.1f} {mx:.1f} {my - 5:.1f})"'))

    # ---------- 2D (plantas, vistas ortográficas) ----------
    def ret(self, x, y, w, h, cls="grosso"):
        """Retângulo 2D em px. cls: grosso (contorno visível) | oculta | fino | corte | topo | esq."""
        (X, Y), W, H = self._v(x, y), round(w * self.k, 1), round(h * self.k, 1)
        self.camadas.append(f'<rect class="{cls}" x="{X}" y="{Y}" width="{W}" height="{H}"/>')

    def circ(self, cx, cy, r, cls="grosso", centro=True):
        """Círculo 2D (furo). centro=True desenha a cruz de linha de centro."""
        (cx, cy), r = self._v(cx, cy), round(r * self.k, 1)
        self.camadas.append(f'<circle class="{cls}" cx="{cx}" cy="{cy}" r="{r}"/>')
        if centro:
            e = r + 6
            self.camadas.append(f'<path class="centro" d="M{cx - e},{cy} H{cx + e} M{cx},{cy - e} V{cy + e}"/>')

    def linha2d(self, pontos, cls="grosso"):
        """Polilinha 2D (px, ou mm dentro de uma vista). cls: grosso | oculta | centro | fino | construcao | corte | topo (fechada com preenchimento)."""
        q = [self._v(a, b) for a, b in pontos]
        tag = "polygon" if cls in ("corte", "topo", "esq", "dir", "sombra") else "polyline"
        self.camadas.append(f'<{tag} class="{cls}" points="{pts(q)}"/>')

    def cota(self, x1, y1, x2, y2, texto=None, desloca=14):
        """Cota 2D (NBR 10126) entre dois pontos de uma aresta horizontal ou vertical, afastada `desloca` px
        (positivo = para baixo/direita). Sem `texto`, escreve a distância em mm (dentro de uma vista).
        Use texto "200*" para marcar medida assumida."""
        if texto is None:
            d = abs(x2 - x1) + abs(y2 - y1)
            texto = f"{d:g}".replace(".", ",")
        (x1, y1), (x2, y2) = self._v(x1, y1), self._v(x2, y2)
        out = []
        if abs(y1 - y2) < 1e-6:  # horizontal
            yc = y1 + desloca
            s = 1 if desloca > 0 else -1
            out.append(f'<path class="cota" d="M{x1},{y1 + 2 * s} V{yc + 3 * s} M{x2},{y2 + 2 * s} V{yc + 3 * s}"/>')
            out.append(f'<line class="cota" x1="{x1}" y1="{yc}" x2="{x2}" y2="{yc}" marker-start="url(#seta-cota)" marker-end="url(#seta-cota)"/>')
            out.append(_t((x1 + x2) / 2, yc - 3, texto, "cota-txt", "middle"))
        else:  # vertical
            xc = x1 + desloca
            s = 1 if desloca > 0 else -1
            out.append(f'<path class="cota" d="M{x1 + 2 * s},{y1} H{xc + 3 * s} M{x2 + 2 * s},{y2} H{xc + 3 * s}"/>')
            out.append(f'<line class="cota" x1="{xc}" y1="{y1}" x2="{xc}" y2="{y2}" marker-start="url(#seta-cota)" marker-end="url(#seta-cota)"/>')
            my = (y1 + y2) / 2
            out.append(_t(xc - 3, my, texto, "cota-txt", "middle", f' transform="rotate(-90 {xc - 3} {my})"'))
        self.camadas.append("\n".join(out))

    def texto(self, x, y, txt, cls="rot", ancora="start"):
        """Texto livre (px, ou mm dentro de uma vista). cls: rot | chamada | detalhe | titulo | cota-txt."""
        x, y = self._v(x, y)
        self.camadas.append(_t(x, y, txt, cls, ancora))

    def chamada2d(self, alvo, texto_xy, txt):
        """Chamada simples 2D: guia do texto até o alvo [x,y] com ponto."""
        (ax, ay), (tx, ty) = self._v(*alvo), self._v(*texto_xy)
        self.camadas.append(f'<polyline class="guia" points="{tx},{ty - 4} {ax},{ay}"/><circle class="ponto" cx="{ax}" cy="{ay}" r="2"/>')
        self.camadas.append(_t(tx + (4 if tx > ax else -4), ty, txt, "chamada", "start" if tx > ax else "end"))

    def carimbo(self, x, y, linhas, largura=300):
        """Carimbo/legenda: caixa de linha fina com linhas de texto mono (a primeira em azul, maior)."""
        alt = 18 + 15 * len(linhas)
        out = [f'<rect class="moldura" x="{x}" y="{y}" width="{largura}" height="{alt}"/>']
        for i, l in enumerate(linhas):
            out.append(_t(x + 12, y + 20 + 15 * i, l, "chamada" if i == 0 else "detalhe"))
        self.camadas.append("\n".join(out))

    # ---------- chamadas com layout automático ----------
    def _chamadas(self, chamadas, colunas):
        xe, xd = colunas or (self.w * .25, self.w * .75)
        for lado, xcol in (("esq", xe), ("dir", xd)):
            itens = []
            for c in chamadas:
                if c.get("lado", "esq") != lado:
                    continue
                ax, ay = self.p(*c["alvo"])
                det = c.get("detalhe") or []
                det = [det] if isinstance(det, str) else det
                itens.append([ay, ax, c["texto"], det, 14 + 13 * len(det)])
            itens.sort()
            topo, base = 40, self.h - 24
            ys, cursor = [], topo
            for ay, _, _, _, alt in itens:
                y = max(ay + 4, cursor + 12)
                ys.append(y)
                cursor = y + alt - 4
            excesso = cursor - base
            if excesso > 0:  # empurra para cima mantendo a ordem
                for i in range(len(ys) - 1, -1, -1):
                    ys[i] -= excesso
                    if i and ys[i] - 12 >= ys[i - 1] + itens[i - 1][4] - 4:
                        break
                    excesso = max(0, ys[i - 1] + itens[i - 1][4] + 8 - ys[i]) if i else 0
            sentido = 1 if lado == "esq" else -1  # a guia sai do texto em direção ao desenho
            for (ay, ax, txt, det, _), y in zip(itens, ys):
                anc = "end" if lado == "esq" else "start"
                x_txt = xcol
                x_ini = xcol + 6 * sentido
                joelho = x_ini + 18 * sentido
                pts_ = f"{x_ini:.1f},{y - 4:.1f} {joelho:.1f},{y - 4:.1f} {ax:.1f},{ay:.1f}"
                self.camadas.append(f'<polyline class="guia" points="{pts_}"/><circle class="ponto" cx="{ax:.1f}" cy="{ay:.1f}" r="2"/>')
                self.camadas.append(_t(x_txt, y, txt, "chamada", anc))
                for k, linha in enumerate(det):
                    self.camadas.append(_t(x_txt, y + 15 + 13 * k, linha, "detalhe", anc))

    def svg(self, fig="FIG_001", nome="", titulo="", subtitulo="", chamadas=(), colunas=None):
        if chamadas:
            self._chamadas(chamadas, colunas)
        topo = []
        if titulo:
            topo.append(_t(48, 44, titulo, "titulo"))
        if subtitulo:
            topo.append(_t(48, 62, subtitulo, "detalhe"))
        return (f'<svg class="bp" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
                f'height="{self.h}" font-family="{MONO}">\n{DEFS}<style>{CSS}</style>\n'
                f'<rect width="{self.w}" height="{self.h}" fill="#fbfbfb"/>'
                f'<rect x="32" y="24" width="{self.w - 64}" height="{self.h - 48}" fill="url(#grade)"/>\n'
                + _t(18, self.h / 2, fig, "fig", "middle", f' transform="rotate(-90 18 {self.h / 2})"')
                + (_t(self.w - 16, self.h / 2, f"[ {nome} ]", "fig", "middle", f' transform="rotate(90 {self.w - 16} {self.h / 2})"') if nome else "")
                + "\n" + "\n".join(topo) + "\n" + "\n".join(self.camadas) + "\n</svg>")


def de_json(cfg, cls=None):
    w, h, ox, oy, esc = cfg.get("tela", [960, 640, 480, 320, 1.0])
    pr = (cls or Prancha)(w, h, ox, oy, esc)
    for item in cfg.get("pecas", []):
        nome, *args = item
        kw = args.pop() if args and isinstance(args[-1], dict) else {}
        getattr(pr, nome)(*args, **kw)
    return pr, pr.svg(cfg.get("fig", "FIG_001"), cfg.get("nome", ""), cfg.get("titulo", ""), cfg.get("subtitulo", ""),
                      cfg.get("chamadas", []), cfg.get("colunas"))


def salvar(cfg, base, cls=None):
    _, s = de_json(cfg, cls)
    open(base + ".svg", "w", encoding="utf-8").write(s)
    modelo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "pagina-figura.html")
    pag = open(modelo, encoding="utf-8").read()
    pag = pag.replace("<!-- SVG INLINE AQUI -->", s)
    pag = pag.replace("FIG_001 — Nome do objeto", html.escape(f'{cfg.get("fig", "FIG_001")} — {cfg.get("titulo") or cfg.get("nome", "")}'))
    pag = pag.replace("Frase curta sobre o que o desenho mostra.", html.escape(cfg.get("subtitulo", "")))
    pag = pag.replace("<span>FIG_001</span>", f'<span>{html.escape(cfg.get("fig", "FIG_001"))}</span>')
    pag = pag.replace("Legenda em uma ou duas frases.", html.escape(cfg.get("legenda", "")))
    open(base + ".html", "w", encoding="utf-8").write(pag)
    print(base + ".svg", base + ".html")


EXEMPLO = {
    "tela": [960, 600, 470, 250, 1.0], "fig": "FIG_001", "nome": "MÓDULO GENÉRICO, 2026",
    "titulo": "MÓDULO — VISTA EXPLODIDA", "subtitulo": "TRÊS CAMADAS: TAMPA · CHIP · PLACA",
    "legenda": "Exemplo do construtor: placa, chip e tampa afastados no eixo de montagem.",
    "pecas": [
        ["caixa", 0, 0, 0, 220, 90, 6],
        ["plano", [[30, 20], [90, 20], [90, 70], [30, 70]], 6, {"cls": "sombra"}],
        ["listras", 200, 10, 6, 18, 70, 8, {"eixo": "y"}],
        ["guias", 30, 20, 6, 60, 50, 0, 70],
        ["caixa", 30, 20, 70, 60, 50, 8],
        ["guias", 0, 0, 78, 220, 90, 0, 140],
        ["caixa", 0, 0, 140, 220, 90, 2, {"faces": "branco"}],
        ["cota_iso", [0, 90, 0], [220, 90, 0], "220", {"desloca": [0, 24, 0]}],
    ],
    "chamadas": [
        {"texto": "TAMPA", "detalhe": "ALUMÍNIO 0,3 MM", "alvo": [40, 0, 142], "lado": "esq"},
        {"texto": "CHIP", "detalhe": ["O CÉREBRO DO MÓDULO"], "alvo": [30, 50, 78], "lado": "esq"},
        {"texto": "PLACA", "detalhe": "FR-4 · 4 CAMADAS", "alvo": [220, 60, 3], "lado": "dir"},
        {"texto": "CONTATOS", "alvo": [210, 40, 6], "lado": "dir"},
    ],
}


def _api():
    import inspect
    out = []
    for nome, f in inspect.getmembers(Prancha, inspect.isfunction):
        if nome.startswith("_") or nome in ("svg", "p"):
            continue
        doc = (inspect.getdoc(f) or "").split("\n")[0]
        out.append(f"{nome}{inspect.signature(f)}".replace("(self, ", "(") + (f"  # {doc}" if doc else ""))
    return "\n".join(out)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
    elif a[0] == "--api":
        print(_api())
    elif a[0] == "--exemplo-json":
        print(json.dumps(EXEMPLO, ensure_ascii=False, indent=1))
    else:
        cfg = EXEMPLO if a[0] == "--exemplo" else json.load(open(a[0], encoding="utf-8"))
        salvar(cfg, a[1] if len(a) > 1 else "prancha")
