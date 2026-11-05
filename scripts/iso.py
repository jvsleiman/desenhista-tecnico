#!/usr/bin/env python3
"""Ajudante de projeção isométrica para a skill desenhista-tecnico.

Converte coordenadas 3D (x, y, z) em pontos 2D de SVG e gera polígonos prontos.
Eixo X vai para a direita-baixo, Y para a esquerda-baixo, Z para cima.

Exemplos:
  iso.py point --x 120 --y 0 --z 40 --origin 400,300
  iso.py box --x 0 --y 0 --z 0 --w 120 --d 80 --h 12 --origin 400,300
  iso.py rbox --x 0 --y 0 --z 0 --w 200 --d 140 --h 6 --r 14 --origin 400,300   (placa arredondada, estilo UI)
  iso.py cyl --cx 60 --cy 40 --z 12 --r 30 --h 4 --origin 400,300
  iso.py explode --x 0 --y 0 --z 0 --w 120 --d 80 --h 12 --gap 60 --origin 400,300
"""
import argparse
import math

COS30 = math.cos(math.radians(30))
SIN30 = 0.5


def proj(x, y, z, ox, oy, s=1.0):
    """Ponto 3D -> 2D isométrico."""
    px = ox + (x - y) * COS30 * s
    py = oy + (x + y) * SIN30 * s - z * s
    return round(px, 1), round(py, 1)


def pts(points):
    return " ".join(f"{x},{y}" for x, y in points)


def box(x, y, z, w, d, h, ox, oy, s):
    """Caixa com canto de trás em (x,y,z), largura w em X, profundidade d em Y, altura h em Z.
    Retorna as três faces visíveis: topo, esquerda (frente em Y), direita (frente em X)."""
    P = lambda a, b, c: proj(a, b, c, ox, oy, s)
    top = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]
    left = [P(x, y + d, z + h), P(x + w, y + d, z + h), P(x + w, y + d, z), P(x, y + d, z)]
    right = [P(x + w, y, z + h), P(x + w, y + d, z + h), P(x + w, y + d, z), P(x + w, y, z)]
    return (
        f'<polygon class="esq" points="{pts(left)}"/>\n'
        f'<polygon class="dir" points="{pts(right)}"/>\n'
        f'<polygon class="topo" points="{pts(top)}"/>'
    )


def cyl(cx, cy, z, r, h, ox, oy, s):
    """Cilindro vertical com centro da base em (cx,cy,z). Elipses isométricas."""
    rx = r * math.sqrt(2) * COS30 * s
    ry = r * math.sqrt(2) * SIN30 * s
    bx, by = proj(cx, cy, z, ox, oy, s)
    tx, ty = proj(cx, cy, z + h, ox, oy, s)
    rx, ry = round(rx, 1), round(ry, 1)
    side = (
        f'M{bx - rx},{by} L{tx - rx},{ty} '
        f'A{rx},{ry} 0 0 0 {tx + rx},{ty} '
        f'L{bx + rx},{by} A{rx},{ry} 0 0 1 {bx - rx},{by} Z'
    )
    return (
        f'<path class="dir" d="{side}"/>\n'
        f'<ellipse class="topo" cx="{tx}" cy="{ty}" rx="{rx}" ry="{ry}"/>'
    )


def _round_rect(x, y, w, d, r, steps=4):
    """Pontos (x, y) de um retângulo de cantos arredondados no plano do chão."""
    r = max(0.0, min(r, w / 2, d / 2))
    pts_ = []
    corners = [(x + w - r, y + r, -90), (x + w - r, y + d - r, 0), (x + r, y + d - r, 90), (x + r, y + r, 180)]
    for cx, cy, a0 in corners:
        for i in range(steps + 1):
            a = math.radians(a0 + 90 * i / steps)
            pts_.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts_


def _hull(points):
    pts_ = sorted(set(points))
    if len(pts_) < 3:
        return pts_
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts_:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts_):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def rbox(x, y, z, w, d, h, r, ox, oy, s, top_cls="topo", side_cls="dir"):
    """Placa isométrica de cantos arredondados (estilo UI). Retorna lateral + topo.
    A lateral é o contorno convexo do topo e da base projetados, então fecha sem frestas."""
    base2d = _round_rect(x, y, w, d, r)
    top = [proj(a, b, z + h, ox, oy, s) for a, b in base2d]
    bot = [proj(a, b, z, ox, oy, s) for a, b in base2d]
    side = _hull(top + bot)
    return (
        f'<polygon class="{side_cls}" points="{pts(side)}"/>\n'
        f'<polygon class="{top_cls}" points="{pts(top)}"/>'
    )


def explode(x, y, z, w, d, h, gap, ox, oy, s):
    """Guias tracejadas verticais nos 4 cantos, ligando a peça (em z) à posição z+gap."""
    out = []
    for a, b in [(x, y), (x + w, y), (x + w, y + d), (x, y + d)]:
        x1, y1 = proj(a, b, z + h, ox, oy, s)
        x2, y2 = proj(a, b, z + gap, ox, oy, s)
        out.append(f'<line class="construcao" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>')
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=["point", "box", "rbox", "cyl", "explode"])
    for k in ["x", "y", "z", "w", "d", "h", "r", "cx", "cy", "gap"]:
        ap.add_argument(f"--{k}", type=float, default=0)
    ap.add_argument("--top-class", default="topo", help="classe CSS do topo (rbox)")
    ap.add_argument("--side-class", default="dir", help="classe CSS da lateral (rbox)")
    ap.add_argument("--origin", default="0,0", help="origem 2D no SVG, ex.: 400,300")
    ap.add_argument("--scale", type=float, default=1.0)
    a = ap.parse_args()
    ox, oy = (float(v) for v in a.origin.split(","))
    if a.kind == "point":
        print("%s,%s" % proj(a.x, a.y, a.z, ox, oy, a.scale))
    elif a.kind == "box":
        print(box(a.x, a.y, a.z, a.w, a.d, a.h, ox, oy, a.scale))
    elif a.kind == "rbox":
        print(rbox(a.x, a.y, a.z, a.w, a.d, a.h, a.r, ox, oy, a.scale, a.top_class, a.side_class))
    elif a.kind == "cyl":
        print(cyl(a.cx, a.cy, a.z, a.r, a.h, ox, oy, a.scale))
    else:
        print(explode(a.x, a.y, a.z, a.w, a.d, a.h, a.gap, ox, oy, a.scale))


if __name__ == "__main__":
    main()
