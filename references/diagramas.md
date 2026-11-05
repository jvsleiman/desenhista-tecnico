# Diagrama de sistema

Arquitetura de software, rede, homelab, fluxo de dados, pipeline, processo. A tentação aqui é cair no visual genérico de "caixinhas com cantos arredondados e ícones coloridos". Resista: o diagrama deve parecer uma prancha do mesmo livro que as ilustrações.

## Duas formas de desenhar

1. **Isométrico** (preferido quando há hardware ou camadas físicas — rack, rede de casa, servidores): cada componente vira um bloco isométrico simples (caixa com as três faces), sobre uma "mesa" de grade pontilhada. Cabos e fluxos correm no plano do chão, em ângulos de 30°.
2. **Plano** (para software puro, fluxos lógicos, sequência): retângulos de canto vivo (`rx="0"`), traço `#0043ff`, preenchimento Névoa; o componente principal em Gelo com traço mais grosso.

Escolha uma e mantenha na figura inteira.

## Elementos

- **Nó**: rótulo mono maiúsculo dentro ou abaixo do bloco (`PROXMOX`, `ROTEADOR`, `API`). Uma segunda linha em cinza 10px para o detalhe técnico (`192.168.1.10`, `PORTA 8080`, `POSTGRES 16`).
- **Ligação**: linha `#0043ff` 1.25px com ponta de seta (`marker-end="url(#seta)"`). Ortogonal ou em 30°, nunca curva livre. Rótulo da ligação em mono 10px Azul Blueprint, sobre um retângulo de fundo `#fbfbfb` para não cruzar o traço.
- **Fluxo assíncrono / opcional / sem fio**: linha tracejada.
- **Agrupamento** (VLAN, rede, cluster, máquina física): retângulo tracejado em cinza `#7d7d7d` com o nome no canto superior esquerdo em mono 10px. Não use fundos coloridos para grupos.
- **Numeração de passos**: quando o diagrama conta uma sequência, marque cada ligação com `01`, `02`... em mono e explique os passos numa legenda curta ao lado, como num livro.

## Sem ícones

Não use conjuntos de ícones (nuvem, banco de dados cilíndrico colorido, logos). Se um tipo de nó precisar de forma própria, desenhe-a em linha azul: um cilindro isométrico para banco de dados, uma pilha de placas para disco, um retângulo com "tela" para monitor. Logos de produto ficam de fora — o nome em texto basta.

## Legibilidade

- Fluxo principal da esquerda para a direita ou de cima para baixo.
- No máximo ~15 nós por figura. Mais do que isso, divida em duas figuras (FIG_001 visão geral, FIG_002 detalhe).
- Alinhe os nós numa grade de 8px.

## No estilo UI

Quando o diagrama é para produto (landing, app, Mostruário), siga `estilo-ui.md` em vez das regras acima: plataforma escura, um protagonista ciano, conectores tracejados animados, rótulos no hover e legenda mono embaixo — sem chamadas com guias nem FIG_00N. Monte com `scripts/cena_ui.py`.
