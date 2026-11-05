# Ilustração isométrica (vista explodida e corte)

Para objetos físicos: aparelhos, componentes, peças, mecanismos. É o coração do estilo Making Software — o disquete explodido, o tubo de raios catódicos em corte, o switch mecânico desmontado.

## Projeção

Isométrico verdadeiro: X e Y a 30° da horizontal, Z vertical. Tudo em `cena_blueprint.py`: `caixa`, `cilindro`, `plano` (pegadas no topo), `listras` (contatos, ventilação), `linha3d`, `guias` (explosão) e `cota_iso`. Desenhe de trás para frente (menor `x+y`, menor `z` primeiro).

## Vista explodida

- Separe as peças **ao longo do eixo de montagem** (quase sempre Z para cima). Espaçamento constante entre camadas, grande o bastante para cada face de topo ficar visível.
- Ligue cada peça à posição de montagem com guias tracejadas finas verticais nos cantos ou no eixo central. São elas que fazem o leitor "remontar" o objeto mentalmente.
- Parafusos e peças pequenas: desenhe um ou dois e indique `×4` na chamada, em vez de desenhar todos.
- Ordem das camadas igual à real (tampa, rótulo, PCB, chip, base). Se não souber, pesquise.

## Corte

- Remova um quarto (ou meio) do objeto com um plano de corte; a face cortada usa `faces: "corte"` (hachura).
- Mostre o que está dentro com o mesmo sombreamento chapado das faces externas.
- Rotule a face cortada só se o material importar (`CARCAÇA ABS`, `VIDRO`).

## Sombreamento

Três tons por volume, luz sempre do alto à esquerda:

| Face | Cor |
|---|---|
| Topo | `#e6ebff` (Gelo) ou `#ffffff` em superfícies polidas (prato, lente) |
| Esquerda | `#f4f5f9` (Névoa) |
| Direita | `#97acff` (Pervinca) |
| Sombra interna, rebaixo | `#b6c8ff` (Centáurea) |
| Peça de destaque (a que a figura explica) | traço e preenchimento um tom mais forte, ou preenchimento sólido `#0043ff` em área pequena |

Detalhes finos (trilhas de PCB, pinos, ranhuras): só traço `#0043ff` a 0.75px, sem preenchimento.

## Chamadas

Entre 5 e 12 chamadas por figura. Mais do que isso polui; menos raramente ensina. Cada chamada nomeia a peça e, quando ajuda, diz a função em 2–4 palavras: `CABEÇA DE LEITURA — LÊ O CAMPO MAGNÉTICO`. Uma informação numérica marcante vale ouro: `7200 RPM`, `ESPESSURA 0,1 MM`.

## Exemplo

`python3 scripts/cena_blueprint.py --exemplo-json` mostra uma vista explodida completa (placa, chip, tampa, guias, cota e chamadas) para usar de molde.
