#!/usr/bin/env python3
"""Renderiza um SVG ou HTML para PNG num Chrome headless (lê variáveis CSS, fontes web e animação).

  render.py entrada.svg saida.png                 # quadro parado (prefers-reduced-motion)
  render.py entrada.html saida.png --hover hub    # passa o mouse sobre o elemento #hub antes
  render.py entrada.html saida.png --tempo 1.5    # quadro da animação em 1,5 s
  render.py entrada.svg saida.png --escala 2      # 2x para conferir detalhe

Requer playwright (pip install playwright --break-system-packages && playwright install chromium);
se já houver google-chrome no sistema, ele é usado direto.
"""
import argparse
import os
import shutil
import sys

from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--hover", help="id do elemento para passar o mouse")
    ap.add_argument("--tempo", type=float, help="segundos de animação antes da captura (desliga o reduced-motion)")
    ap.add_argument("--escala", type=float, default=1.0)
    a = ap.parse_args()

    caminho = os.path.abspath(a.entrada)
    exe = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pag = nav.new_page(device_scale_factor=a.escala, viewport={"width": 1000, "height": 800},
                           reduced_motion="no-preference" if a.tempo is not None else "reduce")
        pag.goto("file://" + caminho)
        pag.wait_for_timeout(300)
        if a.hover:
            pag.hover(f"#{a.hover}")
            pag.wait_for_timeout(350)
        if a.tempo is not None:
            pag.wait_for_timeout(int(a.tempo * 1000))
        alvo = pag.query_selector("svg")
        (alvo or pag).screenshot(path=a.saida)
        nav.close()
    print(a.saida)


if __name__ == "__main__":
    sys.exit(main())
