# Estilo Blueprint — tinta azul sobre papel (Making Software)

Resumo operacional. O guia original, com todos os componentes de página, está em `estilo-making-software.md`.

| Papel | Cor |
|---|---|
| Papel (fundo) | `#fbfbfb` |
| Tinta (texto corrido) | `#000000` |
| Azul Blueprint (rótulos, chamadas, marca) | `#103dff` |
| Azul Esquemático (traços, setas, guias) | `#0043ff` |
| Pervinca (face de sombra) | `#97acff` |
| Centáurea (sombra secundária, hachura de corte) | `#b6c8ff` |
| Gelo (face iluminada) | `#e6ebff` |
| Névoa (corpo do objeto) | `#f4f5f9` |
| Branco (face mais clara, destaque) | `#ffffff` |
| Cinza (FIG_00N, metadados, cotas) | `#7d7d7d` |
| Linha fina (bordas de cartão) | `#e1e1e1` |

- Rótulos, números de figura, cotas: **Departure Mono**, maiúsculas, sem espaçamento extra. Fallback: `'Departure Mono', 'IBM Plex Mono', ui-monospace, monospace`. 10px metadados, 12px chamadas, 14px títulos mono.
- Prosa: **Arizona** → substituto **EB Garamond**, 14px, entrelinha 1.6, justificada. Títulos 16px/500 — nunca tipo grande em serifa.

A identidade inteira vem de uma tinta só. Assim que entra um vermelho de alerta ou um verde de "ok", o desenho deixa de parecer impresso e vira tela de software. Para diferenciar estados, use tom (Pervinca vs. Gelo), tracejado ou hachura.

## Regras de desenho

- Traço padrão `#0043ff`, 1–1.25px, `stroke-linejoin="round"`. Linhas de construção e guias de explosão tracejadas (`3 3`).
- Faces: topo = Gelo ou Branco, lateral esquerda = Névoa, lateral direita = Pervinca (luz do alto à esquerda). Face cortada = hachura Centáurea. Cantos vivos (`iso.py box`).
- **Chamadas**: texto mono maiúsculo `#103dff` com uma linha-guia até a peça terminando num ponto. Guias horizontais ou a 30°, sem cruzar outras guias. Agrupadas em colunas à esquerda e à direita, alinhadas.
- Moldura editorial: `FIG_00N` girado −90° na borda esquerda (cinza 10px); `[ NOME DO OBJETO, ANO ]` girado 90° na direita. Sem borda, sem cantos arredondados, sem sombra.
- Monte com `scripts/cena_blueprint.py` (JSON → SVG + página). `assets/base-figura.svg` é só referência das classes, se precisar de uma peça nova.
- Estático: o Blueprint é uma prancha impressa, não anima.
