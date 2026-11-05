#!/usr/bin/env python3
"""Construtor de cenas no estilo UI (isométrico escuro, acento ciano, animado e interativo).

Use como biblioteca num gerador próprio:

    import sys; sys.path.insert(0, "<skill>/scripts")
    from cena_ui import Cena
    c = Cena(largura=560, altura=420, origem=(280, 190))
    c.plataforma(-150, -110, 300, 220)
    c.pilha("fila", -130, -95, 56, 56, n=3, rotulo="queue · 3 jobs")
    c.hub("hub", -25, -25, 50, 50, 40, rotulo="hub · 3 workers")
    c.card("ok", 70, -10, 60, 40, icone="check", rotulo="endpoint a · 200")
    c.card("erro", 20, 60, 60, 40, icone="x", erro=True, rotulo="endpoint b · 503")
    c.fio([( 25, 0), (100, 0), (100, 10)], ativo=True)
    c.legenda("producer → hub → endpoints", "retry · 503", estado_erro=True)
    c.salvar("cena.svg", "cena.html", titulo="Entrega de webhooks")

Rode este arquivo direto para gerar a cena de exemplo:
    python3 cena_ui.py <saida.svg> <saida.html>

Coordenadas são do mundo isométrico (x para direita-baixo, y para esquerda-baixo, z para cima),
iguais às de iso.py. Os objetos são desenhados na ordem em que são adicionados: adicione de trás
para frente (menor x+y primeiro).
"""
import html
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iso import proj, pts, rbox, cyl, _round_rect  # noqa: E402

TOKENS = """
  --ui-pagina:#0f0f0f; --ui-cartao:#161616; --ui-cartao-borda:#262626;
  --ui-plat-topo:#1b1b1b; --ui-plat-lado:#121212; --ui-traco:#3a3a3a; --ui-traco-forte:#5a5a5a;
  --ui-obj-topo:#222222; --ui-obj-lado:#181818; --ui-detalhe:#6b6b6b;
  --ui-acento:#38bdf8; --ui-acento-topo:#7dd3fc; --ui-acento-lado:#0ea5e9; --ui-acento-fundo:#0c4a6e;
  --ui-erro:#f472b6; --ui-legenda:#737373;
"""

CSS = """
svg.cena-ui { --ui-pagina:#0f0f0f; %s font-family:'Departure Mono','JetBrains Mono','IBM Plex Mono',ui-monospace,monospace; }
.cena-ui .plat-topo { fill:var(--ui-plat-topo); stroke:var(--ui-traco); stroke-width:1; stroke-linejoin:round; }
.cena-ui .plat-lado { fill:var(--ui-plat-lado); stroke:var(--ui-traco); stroke-width:1; stroke-linejoin:round; }
.cena-ui .trilho { fill:none; stroke:var(--ui-traco); stroke-width:1; opacity:.7; }
.cena-ui .obj-topo { fill:var(--ui-obj-topo); stroke:var(--ui-traco-forte); stroke-width:1; stroke-linejoin:round; transition:stroke .2s; }
.cena-ui .obj-lado { fill:var(--ui-obj-lado); stroke:var(--ui-traco-forte); stroke-width:1; stroke-linejoin:round; transition:stroke .2s; }
.cena-ui .ac-topo { fill:var(--ui-acento-topo); stroke:var(--ui-acento-topo); stroke-width:1; stroke-linejoin:round; }
.cena-ui .ac-lado { fill:var(--ui-acento-lado); stroke:var(--ui-acento-topo); stroke-width:1; stroke-linejoin:round; }
.cena-ui .fantasma { fill:none; stroke:var(--ui-acento); stroke-width:1.25; stroke-dasharray:4 4; animation:ui-gira 6s linear infinite; }
.cena-ui .risco { fill:none; stroke:var(--ui-detalhe); stroke-width:1.2; stroke-linecap:round; }
.cena-ui .risco-ac { fill:none; stroke:var(--ui-acento-fundo); stroke-width:1.6; stroke-linecap:round; }
.cena-ui .icone { fill:none; stroke:var(--ui-acento); stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round; }
.cena-ui .icone.erro { stroke:var(--ui-erro); animation:ui-pisca 4s ease-in-out infinite; }
.cena-ui .fio { fill:none; stroke:var(--ui-traco); stroke-width:1.25; stroke-dasharray:4 4; }
.cena-ui .fio.ativo { stroke:var(--ui-acento); animation:ui-corre 1.2s linear infinite; }
.cena-ui .fio.erro { stroke:var(--ui-erro); }
.cena-ui .no { fill:var(--ui-acento); }
.cena-ui .led-erro { fill:var(--ui-erro); animation:ui-pisca 1.6s ease-in-out infinite; }
.cena-ui .risco-tela-ac { fill:none; stroke:var(--ui-acento); stroke-width:1.6; stroke-linecap:round; }
.cena-ui .rot-fio { font-size:11px; fill:var(--ui-legenda); }
.cena-ui .rot-fio.ativo { fill:var(--ui-acento); }
.cena-ui .rot-fio.erro { fill:var(--ui-erro); }
.cena-ui .pacote { fill:var(--ui-acento-topo); offset-rotate:0deg; animation:ui-viaja var(--dur,3s) cubic-bezier(.4,0,.2,1) infinite; }
.cena-ui .hub { animation:ui-respira 2.4s ease-in-out infinite; }
.cena-ui .legenda { font-size:13px; fill:var(--ui-legenda); }
.cena-ui .estado { font-size:13px; fill:var(--ui-acento); }
.cena-ui .estado.erro { fill:var(--ui-erro); }
.cena-ui .tag { font-size:11px; fill:#d4d4d4; opacity:0; transition:opacity .2s; pointer-events:none; }
.cena-ui .tag-fundo { fill:#0f0f0f; stroke:var(--ui-traco-forte); stroke-width:1; opacity:0; transition:opacity .2s; pointer-events:none; }
.cena-ui .rot-fundo { fill:#1b1b1b; }
.cena-ui .obj { transition:transform .25s cubic-bezier(.4,0,.2,1), opacity .25s; outline:none; }
.cena-ui.focando .obj:not(.ativo) { opacity:.55; }
.cena-ui .obj.ativo { transform:translateY(-3px); }
.cena-ui .obj.ativo .obj-topo, .cena-ui .obj.ativo .obj-lado { stroke:#8a8a8a; }
.cena-ui .obj.ativo .tag, .cena-ui .obj.ativo .tag-fundo { opacity:1; }

.cena-ui .alt-a { animation:ui-alt-a 6s steps(1) infinite; }
.cena-ui .alt-b { opacity:0; animation:ui-alt-b 6s steps(1) infinite; }
@keyframes ui-alt-a { 0%%{opacity:1} 50%%{opacity:0} }
@keyframes ui-alt-b { 0%%{opacity:0} 50%%{opacity:1} }
@keyframes ui-corre { to { stroke-dashoffset:-16; } }
@keyframes ui-gira { to { stroke-dashoffset:-32; } }
@keyframes ui-viaja { 0%%{offset-distance:0%%;opacity:0} 10%%{opacity:1} 90%%{opacity:1} 100%%{offset-distance:100%%;opacity:0} }
@keyframes ui-respira { 0%%,100%%{filter:drop-shadow(0 0 4px rgb(56 189 248 / .22))} 50%%{filter:drop-shadow(0 0 10px rgb(56 189 248 / .45))} }
@keyframes ui-pisca { 0%%,55%%,100%%{opacity:.35} 65%%,85%%{opacity:1} }
@media (prefers-reduced-motion: reduce) { .cena-ui * { animation:none !important; transition:none !important; } .cena-ui .pacote { display:none; } }
""" % TOKENS.strip()

ICONES = {
    # "tela": desenhados em pixels de tela, achatados na vertical (lidos como símbolo: ✓ × +).
    # "plano": desenhados no plano do topo, em unidades do mundo (lidos como objeto deitado: envelope, riscos).
    "check": ("tela", [[(-7, 0), (-2, 5), (8, -6)]]),
    "x": ("tela", [[(-6, -6), (6, 6)], [(-6, 6), (6, -6)]]),
    "mais": ("tela", [[(-7, 0), (7, 0)], [(0, -7), (0, 7)]]),
    "envelope": ("plano", [[(-10, -7), (10, -7), (10, 7), (-10, 7), (-10, -7)], [(-10, -7), (0, 1), (10, -7)]]),
    "cadeado": ("tela", [[(-6, -1), (6, -1), (6, 8), (-6, 8), (-6, -1)], [(-3.5, -1), (-3.5, -6), (3.5, -6), (3.5, -1)]]),
    "riscos": ("plano", [[(-10, -4), (6, -4)], [(-10, 1), (2, 1)], [(-10, 6), (8, 6)]]),
}


class Cena:
    def __init__(self, largura=560, altura=420, origem=(280, 190), escala=1.0):
        self.w, self.h = largura, altura
        self.ox, self.oy = origem
        self.s = escala
        self.camadas = []  # strings SVG em ordem de pintura
        self.legendas = ""

    # ---- utilidades ----
    def p(self, x, y, z):
        return proj(x, y, z, self.ox, self.oy, self.s)

    def _rbox(self, x, y, z, w, d, h, r, topo, lado):
        return rbox(x, y, z, w, d, h, r, self.ox, self.oy, self.s, topo, lado)

    def _icone(self, nome, cx, cy, z, erro=False, escala=1.0):
        modo, linhas = ICONES[nome]
        out = []
        cxp, cyp = self.p(cx, cy, z)
        for linha in linhas:
            if modo == "plano":
                pp = [self.p(cx + a * escala, cy + b * escala, z) for a, b in linha]
            else:  # tela: achata 0.62 na vertical para parecer deitado no topo
                pp = [(round(cxp + a * escala * self.s, 2), round(cyp + b * escala * .62 * self.s, 2)) for a, b in linha]
            out.append(f'<polyline class="{"icone erro" if erro else "icone"}" points="{pts(pp)}"/>')
        return "\n".join(out)

    def _tag(self, texto, x, y, z):
        """Rótulo do hover. Passe o ponto mais alto do objeto na tela — o canto de trás do topo (x, y, z_topo)."""
        if not texto:
            return ""
        tx, ty = self.p(x, y, z)
        ty -= 6
        larg = 7 * len(texto) + 14
        t = html.escape(texto)
        return (f'<rect class="tag-fundo" x="{tx - larg / 2:.1f}" y="{ty - 30:.1f}" width="{larg}" height="20" rx="4"/>'
                f'<text class="tag" x="{tx:.1f}" y="{ty - 16:.1f}" text-anchor="middle">{t}</text>')

    def _grupo(self, id_, rotulo, corpo, extra_cls=""):
        aria = html.escape(rotulo or id_)
        return (f'<g class="obj {extra_cls}" id="{id_}" tabindex="0" role="img" aria-label="{aria}" '
                f'data-rotulo="{aria}">{corpo}</g>')

    # ---- peças ----
    def plataforma(self, x, y, w, d, h=6, r=16, trilho=12):
        corpo = self._rbox(x, y, 0, w, d, h, r, "plat-topo", "plat-lado")
        anel = _round_rect(x + trilho, y + trilho, w - 2 * trilho, d - 2 * trilho, max(4, r - trilho / 2))
        corpo += f'\n<polygon class="trilho" points="{pts([self.p(a, b, h) for a, b in anel])}"/>'
        self.z0 = h
        self.camadas.append(f'<g class="plataforma">{corpo}</g>')

    def placa(self, id_, x, y, w, d, h=8, r=8, z=None, icone=None, rotulo="", erro=False, acento=False):
        z = self.z0 if z is None else z
        cls = ("ac-topo", "ac-lado") if acento else ("obj-topo", "obj-lado")
        corpo = self._rbox(x, y, z, w, d, h, r, *cls)
        if icone:
            corpo += "\n" + self._icone(icone, x + w / 2, y + d / 2, z + h, erro)
        corpo += self._tag(rotulo, x, y, z + h)
        self.camadas.append(self._grupo(id_, rotulo, corpo))

    def card(self, id_, x, y, w=60, d=40, icone="check", rotulo="", erro=False):
        self.placa(id_, x, y, w, d, h=8, r=8, icone=icone, rotulo=rotulo, erro=erro)

    def pilha(self, id_, x, y, w, d, n=3, h=12, gap=4, z=None, rotulo=""):
        """Servidor/fila: n placas empilhadas com riscos e LED."""
        z = self.z0 if z is None else z
        corpo = []
        for i in range(n):
            zi = z + i * (h + gap)
            corpo.append(self._rbox(x, y, zi, w, d, h, 6, "obj-topo", "obj-lado"))
            # riscos e LED na face frontal-direita (plano x = x+w)
            a, b = self.p(x + w, y + d * .25, zi + h * .5), self.p(x + w, y + d * .6, zi + h * .5)
            corpo.append(f'<line class="risco" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
            led = self.p(x + w, y + d * .8, zi + h * .5)
            corpo.append(f'<circle cx="{led[0]}" cy="{led[1]}" r="1.6" fill="var(--ui-acento)"/>' if i == n - 1
                         else f'<circle cx="{led[0]}" cy="{led[1]}" r="1.4" fill="var(--ui-detalhe)"/>')
        corpo.append(self._icone("riscos", x + w / 2, y + d / 2, z + (n - 1) * (h + gap) + h, escala=1.1)
                     .replace('class="icone"', 'class="risco"'))
        corpo.append(self._tag(rotulo, x, y, z + (n - 1) * (h + gap) + h))
        self.camadas.append(self._grupo(id_, rotulo, "\n".join(corpo)))

    def hub(self, id_, x, y, w=50, d=50, h=40, r=12, rotulo=""):
        """O protagonista em ciano. Use um por cena."""
        z = self.z0
        corpo = self._rbox(x, y, z, w, d, h, r, "ac-topo", "ac-lado")
        # três riscos verticais na face frontal-direita
        for k in (.35, .5, .65):
            a, b = self.p(x + w, y + d * k, z + h * .3), self.p(x + w, y + d * k, z + h * .62)
            corpo += f'\n<line class="risco-ac" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>'
        corpo += self._tag(rotulo, x, y, z + h)
        self.camadas.append(self._grupo(id_, rotulo, f'<g class="hub">{corpo}</g>'))

    def fantasma(self, id_, x, y, w=60, d=40, h=8, r=8, icone="mais", rotulo=""):
        z = self.z0
        topo = _round_rect(x, y, w, d, r)
        corpo = f'<polygon class="fantasma" points="{pts([self.p(a, b, z + h) for a, b in topo])}"/>'
        corpo += "\n" + self._icone(icone, x + w / 2, y + d / 2, z + h)
        corpo += self._tag(rotulo, x, y, z + h)
        self.camadas.append(self._grupo(id_, rotulo, corpo))

    def chips(self, id_, x, y, n=3, lado=12, passo=18, eixo="x", rotulo=""):
        corpo = []
        for i in range(n):
            xi, yi = (x + i * passo, y) if eixo == "x" else (x, y + i * passo)
            corpo.append(self._rbox(xi, yi, self.z0, lado, lado, 5, 3, "obj-topo", "obj-lado"))
        corpo.append(self._tag(rotulo, x, y, self.z0 + 5))
        self.camadas.append(self._grupo(id_, rotulo, "\n".join(corpo)))

    def fio(self, caminho, ativo=True, erro=False, pacote=True, dur=3.0, z=None, pacotes=1):
        """Conector no plano da plataforma. caminho = [(x,y), ...] seguindo os eixos X/Y (cotovelos isométricos)."""
        z = self.z0 if z is None else z
        pp = [self.p(a, b, z) for a, b in caminho]
        d = "M" + " L".join(f"{a},{b}" for a, b in pp)
        cls = "fio" + (" ativo" if ativo else "") + (" erro" if erro else "")
        out = f'<path class="{cls}" d="{d}"/>'
        out += f'<circle class="no" cx="{pp[0][0]}" cy="{pp[0][1]}" r="2"/><circle class="no" cx="{pp[-1][0]}" cy="{pp[-1][1]}" r="2"/>'
        if ativo and pacote and not erro:
            for k in range(pacotes):  # vários pacotes defasados no mesmo fio
                out += (f'<rect class="pacote" x="-3" y="-3" width="6" height="6" transform="rotate(45)" '
                        f'style="offset-path:path(\'{d}\');--dur:{dur}s;animation-delay:-{dur * k / pacotes:.2f}s"/>')
        self.camadas.append(f'<g class="fios">{out}</g>')

    def legenda(self, fluxo, estado="", estado_erro=False, estado_alt=""):
        """Legenda mono embaixo. estado_alt: texto que alterna com `estado` no ciclo da animação."""
        y = self.h - 22
        out = f'<text class="legenda" x="24" y="{y}">{html.escape(fluxo)}</text>'
        if estado:
            cls = "estado erro" if estado_erro else "estado"
            alt = " alt-a" if estado_alt else ""
            out += f'<text class="{cls}{alt}" id="estado" x="{self.w - 24}" y="{y}" text-anchor="end">{html.escape(estado)}</text>'
            if estado_alt:
                out += f'<text class="estado alt-b" x="{self.w - 24}" y="{y}" text-anchor="end">{html.escape(estado_alt)}</text>'
        self.legendas = out

    def rotulo_fio(self, texto, x, y, ativo=False, erro=False, ancora="middle", dx=0, dy=-12):
        """Rótulo curto deitado sobre um fio (ex.: 'hit · 2ms'), para a figura parada se explicar sozinha."""
        px, py = self.p(x, y, self.z0)
        px, py = px + dx, py + dy
        cls = "rot-fio" + (" ativo" if ativo else "") + (" erro" if erro else "")
        larg = 6.7 * len(texto) + 8
        x0 = {"start": px - 4, "end": px - larg + 4}.get(ancora, px - larg / 2)
        # fundo da cor da plataforma: o tracejado que passa por baixo não risca o texto
        self.camadas.append(f'<rect class="rot-fundo" x="{x0:.1f}" y="{py - 10:.1f}" width="{larg:.1f}" height="14" rx="3"/>'
                            f'<text class="{cls}" x="{px:.1f}" y="{py:.1f}" text-anchor="{ancora}">{html.escape(texto)}</text>')

    def monitor(self, id_, x, y, rotulo=""):
        """PC/estação: base, pescoço e tela voltada para +x, com linhas de 'arquivos' na tela."""
        z = self.z0
        c = [self._rbox(x, y, z, 34, 40, 4, 6, "obj-topo", "obj-lado"),
             self._rbox(x + 12, y + 16, z + 4, 6, 8, 10, 2, "obj-topo", "obj-lado")]
        mx, my, mz, mw, md, mh = x + 14, y - 14, z + 12, 5, 68, 46
        c.append(self._rbox(mx, my, mz, mw, md, mh, 4, "obj-topo", "obj-lado"))
        fx = mx + mw
        moldura = [self.p(fx, my + 6, mz + 6), self.p(fx, my + md - 6, mz + 6),
                   self.p(fx, my + md - 6, mz + mh - 6), self.p(fx, my + 6, mz + mh - 6)]
        c.append(f'<polygon class="trilho" points="{pts(moldura)}"/>')
        for i, (comp, ac) in enumerate([(30, True), (22, False), (34, False), (18, False)]):
            zz = mz + mh - 14 - i * 8
            a, b = self.p(fx, my + 14, zz), self.p(fx, my + 14 + comp, zz)
            c.append(f'<line class="{"risco-tela-ac" if ac else "risco"}" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
        c.append(self._tag(rotulo, mx, my, mz + mh))
        self.camadas.append(self._grupo(id_, rotulo, "\n".join(c)))

    def disco(self, id_, x, y, w=64, d=44, falhou=False, rotulo=""):
        """Disco/volume: duas placas com riscos e LED de estado; ✓ ciano ou × rosa no topo."""
        z = self.z0
        c = [self._rbox(x, y, z, w, d, 7, 8, "obj-topo", "obj-lado"),
             self._rbox(x, y, z + 10, w, d, 7, 8, "obj-topo", "obj-lado")]
        topo = z + 17
        c.append(self._icone("x" if falhou else "check", x + w / 2, y + d / 2, topo, erro=falhou))
        for zi in (z + 3.5, z + 13.5):
            a, b = self.p(x + w * .2, y + d, zi), self.p(x + w * .55, y + d, zi)
            c.append(f'<line class="risco" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
            led = self.p(x + w * .8, y + d, zi)
            c.append(f'<circle class="led-erro" cx="{led[0]}" cy="{led[1]}" r="1.6"/>' if falhou
                     else f'<circle cx="{led[0]}" cy="{led[1]}" r="1.6" fill="var(--ui-acento)"/>')
        c.append(self._tag(rotulo, x, y, topo))
        self.camadas.append(self._grupo(id_, rotulo, "\n".join(c)))

    def banco(self, id_, cx, cy, r=26, n=3, h=12, gap=5, rotulo=""):
        """Banco de dados: n cilindros empilhados com risco e LED na frente."""
        z = self.z0
        c = []
        for i in range(n):
            zi = z + i * (h + gap)
            c.append(cyl(cx, cy, zi, r, h, self.ox, self.oy, self.s)
                     .replace('class="dir"', 'class="obj-lado"').replace('class="topo"', 'class="obj-topo"'))
            a, b = self.p(cx + r * .2, cy + r * .95, zi + h * .5), self.p(cx + r * .55, cy + r * .78, zi + h * .5)
            c.append(f'<line class="risco" x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>')
            led = self.p(cx + r * .8, cy + r * .55, zi + h * .5)
            c.append(f'<circle cx="{led[0]}" cy="{led[1]}" r="1.4" fill="var(--ui-detalhe)"/>')
        c.append(self._tag(rotulo, cx - r * .7, cy - r * .7, z + (n - 1) * (h + gap) + h))
        self.camadas.append(self._grupo(id_, rotulo, "\n".join(c)))

    # ---- saída ----
    def svg(self):
        corpo = "\n".join(self.camadas)
        return (f'<svg class="cena-ui" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}" role="img">\n<style>{CSS}</style>\n'
                f'<rect width="{self.w}" height="{self.h}" rx="16" fill="#161616" stroke="#262626"/>\n'
                f'{corpo}\n{self.legendas}\n</svg>')

    def salvar(self, caminho_svg, caminho_html=None, titulo="Ilustração", script_extra="", dica=None):
        s = self.svg()
        with open(caminho_svg, "w", encoding="utf-8") as f:
            f.write(s)
        if caminho_html:
            modelo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "pagina-ui.html")
            pagina = open(modelo, encoding="utf-8").read()
            pagina = pagina.replace("{{TITULO}}", html.escape(titulo)).replace("{{SVG}}", s)
            pagina = pagina.replace("/*{{SCRIPT_EXTRA}}*/", script_extra)
            if dica is None:
                dica = "passe o mouse ou use Tab para destacar as peças"
                if "icone erro" in s:
                    dica += " · clique na peça com erro para tentar de novo"
            pagina = pagina.replace("{{DICA}}", html.escape(dica))
            with open(caminho_html, "w", encoding="utf-8") as f:
                f.write(pagina)


def _api(cls):
    import inspect
    linhas = []
    for nome, f in inspect.getmembers(cls, inspect.isfunction):
        if nome.startswith("_") or nome in ("svg", "salvar", "p"):
            continue
        doc = (inspect.getdoc(f) or "").split("\n")[0]
        linhas.append(f"{nome}{inspect.signature(f)}".replace("(self, ", "(").replace("(self)", "()") + (f"  # {doc}" if doc else ""))
    return "\n".join(linhas)


def de_json(cfg, cls=None):
    """Monta a cena a partir de um dict:
    {"tela": [largura, altura, ox, oy, escala],
     "pecas": [["plataforma", -170, -130, 330, 260], ["hub", "srv", -25, -25, 50, 50, 42, {"rotulo": "..."}], ...],
     "legenda": ["fluxo", "estado", {"estado_erro": true}], "titulo": "...", "dica": null}
    Cada peça é [método, *args posicionais, {kwargs opcionais}], na ordem de pintura (de trás para frente)."""
    cls = cls or Cena
    w, h, ox, oy, esc = (cfg.get("tela") or [560, 420, 280, 205, 0.9]) + [None] * 0
    c = cls(largura=w, altura=h, origem=(ox, oy), escala=esc)
    for item in cfg.get("pecas", []):
        nome, *args = item
        kw = args.pop() if args and isinstance(args[-1], dict) else {}
        if nome == "fio" and args:  # caminho como lista de pares
            args[0] = [tuple(p) for p in args[0]]
        getattr(c, nome)(*args, **kw)
    if cfg.get("legenda"):
        args = list(cfg["legenda"])
        kw = args.pop() if isinstance(args[-1], dict) else {}
        c.legenda(*args, **kw)
    return c


USO = """uso:
  cena_ui.py --api                 lista as peças e seus parâmetros (não precisa ler este arquivo)
  cena_ui.py cena.json saida       gera saida.svg e saida.html a partir da descrição em JSON
  cena_ui.py --exemplo saida       gera a cena de exemplo (e --exemplo-json mostra o JSON dela)"""

EXEMPLO_JSON = {
    "tela": [560, 420, 280, 205, 0.9], "titulo": "Entrega de webhooks",
    "pecas": [
        ["plataforma", -165, -130, 320, 280],
        ["pilha", "produtor", -150, -118, 56, 56, {"n": 3, "rotulo": "producer · 3 apps"}],
        ["chips", "fila", -72, -112, {"n": 3, "rotulo": "queue · 3 eventos"}],
        ["fio", [[-30, -100], [-30, -25]], {"dur": 2.2}],
        ["fio", [[15, -25], [15, -62], [70, -62]], {"ativo": False}],
        ["placa", "assinatura", 70, -80, 40, 34, {"h": 6, "r": 6, "icone": "envelope", "rotulo": "payload assinado"}],
        ["fio", [[25, 0], [70, 0]], {"dur": 2.6}],
        ["fio", [[-25, 10], [-90, 10], [-90, 62]], {"pacote": False}],
        ["fio", [[5, 25], [5, 72]], {"erro": True}],
        ["hub", "hub", -25, -25, 50, 50, 40, {"rotulo": "hub · 4 workers"}],
        ["card", "ok", 70, -20, 60, 40, {"icone": "check", "rotulo": "endpoint a · 200"}],
        ["fantasma", "novo", -120, 62, 60, 40, {"rotulo": "novo endpoint"}],
        ["card", "erro", -25, 72, 60, 40, {"icone": "x", "erro": True, "rotulo": "endpoint b · 503"}],
    ],
    "legenda": ["producer → hub → endpoints", "retry · 503", {"estado_erro": True}],
}


if __name__ == "__main__":
    import json
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(USO)
    elif a[0] == "--api":
        print(_api(Cena))
        print("\nícones:", ", ".join(ICONES))
    elif a[0] == "--exemplo-json":
        print(json.dumps(EXEMPLO_JSON, ensure_ascii=False, indent=1))
    else:
        cfg = EXEMPLO_JSON if a[0] == "--exemplo" else json.load(open(a[0], encoding="utf-8"))
        base = a[1] if len(a) > 1 else "cena"
        de_json(cfg).salvar(base + ".svg", base + ".html", titulo=cfg.get("titulo", "Ilustração"), dica=cfg.get("dica"))
        print(base + ".svg", base + ".html")
