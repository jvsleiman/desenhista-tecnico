#!/usr/bin/env python3
"""Confere um SVG/HTML sem precisar olhar a imagem: textos sobrepostos, texto coberto por peça, texto fora da área e cores fora da paleta.

  verifica.py desenho.svg --estilo blueprint|ui [--png saida.png]

Imprime "OK" ou uma lista curta de problemas (com o texto e as coordenadas). Com --png, também salva o
render (escala 1) — abra a imagem só depois que a verificação passar, uma vez, para o juízo visual final.
"""
import argparse
import os
import re
import shutil
import sys

from playwright.sync_api import sync_playwright

PALETA = {
    "blueprint": {"fbfbfb", "000000", "103dff", "0043ff", "97acff", "b6c8ff", "e6ebff", "f4f5f9", "ffffff", "7d7d7d", "e1e1e1"},
    "ui": {"0f0f0f", "161616", "262626", "1b1b1b", "121212", "3a3a3a", "5a5a5a", "222222", "181818", "6b6b6b",
           "38bdf8", "7dd3fc", "0ea5e9", "0c4a6e", "f472b6", "737373", "8a8a8a", "d4d4d4", "525252"},
}

JS = """() => {
  const svg = document.querySelector('svg'); const R = svg.getBoundingClientRect();
  const out = [];
  for (const t of svg.querySelectorAll('text')) {
    const cs = getComputedStyle(t);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    if (t.closest('.tag, [opacity="0"]')) continue;
    const b = t.getBoundingClientRect();
    if (!b.width) continue;
    // coberto por outra peça? amostra 5 pontos na linha média do texto
    let cobertos = 0;
    for (const f of [.1, .3, .5, .7, .9]) {
      const el = document.elementFromPoint(b.x + b.width * f, b.y + b.height * .55);
      if (el && el !== t && !t.contains(el) && !(el.closest && el.closest('text, .tag-fundo, .rot-fundo')) && parseFloat(getComputedStyle(el).opacity) > 0) cobertos++;
    }
    out.push({t: t.textContent.trim().slice(0, 40), x: b.x - R.x, y: b.y - R.y, w: b.width, h: b.height, cob: cobertos});
  }
  return {W: R.width, H: R.height, textos: out};
}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("arquivo")
    ap.add_argument("--estilo", choices=PALETA, required=True)
    ap.add_argument("--png")
    a = ap.parse_args()

    fonte = open(a.arquivo, encoding="utf-8").read()
    problemas = []
    fora = sorted({c.lower() for c in re.findall(r"#([0-9a-fA-F]{6})\b", fonte)} - PALETA[a.estilo])
    if fora:
        problemas.append("cores fora da paleta: " + ", ".join("#" + c for c in fora))

    exe = shutil.which("google-chrome") or shutil.which("chromium")
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pag = nav.new_page(reduced_motion="reduce", viewport={"width": 1400, "height": 1000})
        pag.goto("file://" + os.path.abspath(a.arquivo))
        pag.wait_for_timeout(250)
        r = pag.evaluate(JS)
        if a.png:
            (pag.query_selector("svg") or pag).screenshot(path=a.png)
        nav.close()

    T, W, H = r["textos"], r["W"], r["H"]
    for t in T:
        if t["x"] < 0 or t["y"] < 0 or t["x"] + t["w"] > W or t["y"] + t["h"] > H:
            problemas.append(f'fora da área: "{t["t"]}" em ({t["x"]:.0f},{t["y"]:.0f})')
    for t in T:
        if t["cob"] >= 2:
            problemas.append(f'texto coberto por uma peça: "{t["t"]}" em ({t["x"]:.0f},{t["y"]:.0f})')
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            A, B = T[i], T[j]
            dx = min(A["x"] + A["w"], B["x"] + B["w"]) - max(A["x"], B["x"])
            dy = min(A["y"] + A["h"], B["y"] + B["h"]) - max(A["y"], B["y"])
            if dx > 2 and dy > 2 and not (A["x"] == B["x"] and A["y"] == B["y"]):
                problemas.append(f'sobreposição: "{A["t"]}" × "{B["t"]}" em ({A["x"]:.0f},{A["y"]:.0f})')
    print("OK" if not problemas else "\n".join(problemas[:15]))
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
