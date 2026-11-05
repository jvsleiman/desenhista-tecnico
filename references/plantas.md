# Planta / desenho técnico com cotas

Monte com as peças 2D de `scripts/cena_blueprint.py` (`ret`, `circ`, `linha2d` com `oculta`/`centro`, `cota`, `chamada2d`, `texto`, `carimbo`) e, para a perspectiva pequena, `caixa`. Coordenadas 2D em pixels: escolha uma escala (ex. 1 mm = 0,8 px) e mantenha em todas as vistas.

Para peças, suportes, móveis, gabinetes, racks — qualquer coisa que alguém vá fabricar, cortar ou imprimir em 3D. Aqui a precisão vale mais que a beleza, mas o visual continua o do livro.

## Medidas primeiro

Desenho com cota inventada é perigoso: a pessoa corta a madeira errada. Se o usuário não deu as medidas que definem a peça, pergunte. Se der só algumas, derive as outras e marque-as como assumidas na legenda (`* MEDIDA ASSUMIDA`). Unidade padrão: **milímetros**, sem escrever "mm" em cada cota — indique `COTAS EM MM` no carimbo.

## Vistas (1º diedro, padrão brasileiro ABNT)

No 1º diedro, usado no Brasil (NBR 10067):

- **Vista frontal** no centro.
- **Vista superior** abaixo da frontal.
- **Vista lateral esquerda** à direita da frontal.

Alinhe as vistas entre si (mesma altura na horizontal, mesma largura na vertical) com linhas de chamada finas tracejadas. Adicione uma **perspectiva isométrica** pequena no canto superior direito para quem não lê vistas ortográficas — use `scripts/iso.py`.

## Linhas (NBR 8403, adaptada à paleta)

| Tipo | Uso | Estilo |
|---|---|---|
| Contorno visível | arestas | `#0043ff` 1.5px contínua |
| Aresta oculta | atrás da face | `#0043ff` 1px, `stroke-dasharray="4 2"` |
| Linha de centro | eixos, furos | `#0043ff` 0.75px, `stroke-dasharray="10 2 2 2"` |
| Cota e chamada | dimensões | `#7d7d7d` 0.75px contínua |
| Hachura | corte | padrão `#hachura` |

## Cotas (NBR 10126)

- Linha de cota paralela à aresta, afastada ~10px do desenho, com setas finas ou traços oblíquos nas pontas.
- Linhas de extensão saem ~2px da peça e passam ~3px da linha de cota.
- Número em mono 10px `#103dff`, centralizado acima da linha de cota, legível de baixo ou da direita.
- Furos: `Ø8` e, se repetidos, `4× Ø8`. Raios: `R5`.
- Cote cada medida uma vez só; prefira cotas em cadeia a partir de uma referência.

## Carimbo (legenda)

Canto inferior direito, retângulo de linha `#e1e1e1`, texto mono:

```
TÍTULO DA PEÇA
MATERIAL: MDF 15        ESCALA: 1:5
COTAS EM MM             FOLHA 01/01
DESENHO: CLAUDE · DATA
```

Escala é a real se a pessoa for imprimir a folha; senão escreva `SEM ESCALA`.
