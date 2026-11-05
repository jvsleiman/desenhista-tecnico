# Estilo UI — ilustração isométrica escura para produto

Ilustração de produto para landing page, tela de app, card de feature, demo do Mostruário. Explica um conceito de software (fila, webhook, cache, deploy, sincronização) com objetos isométricos simples sobre uma plataforma escura. Pense em "peça de hardware fosca numa mesa escura, com uma única coisa acesa em ciano".

A diferença para o Blueprint: lá tudo é tinta sobre papel e a ideia é documentar; aqui o fundo é escuro, quase tudo é cinza discreto e **um** elemento brilha, e a ideia é mostrar o comportamento — por isso o estilo é animado e interativo.

Ferramentas: `scripts/cena_ui.py` monta a cena a partir de um JSON (`--api`, `--exemplo-json`) com tudo abaixo já aplicado; `scripts/render.py` renderiza quadro parado e hover. Resultado de referência: `assets/exemplo-ui.png`.

## Tokens

```css
--ui-pagina:      #0f0f0f;  /* fundo atrás do cartão */
--ui-cartao:      #161616;  /* fundo do cartão */
--ui-cartao-borda:#262626;  /* borda 1px do cartão, raio 16px */
--ui-plat-topo:   #1b1b1b;  /* topo da plataforma */
--ui-plat-lado:   #121212;  /* lateral da plataforma */
--ui-traco:       #3a3a3a;  /* traço padrão de tudo */
--ui-traco-forte: #5a5a5a;  /* contornos de objetos em primeiro plano */
--ui-obj-topo:    #222222;  /* topo de objetos neutros */
--ui-obj-lado:    #181818;  /* lateral de objetos neutros */
--ui-detalhe:     #6b6b6b;  /* riscos, LEDs apagados, ícones neutros */
--ui-acento:      #38bdf8;  /* ciano: o elemento principal, conectores ativos */
--ui-acento-topo: #7dd3fc;  /* topo iluminado do elemento principal */
--ui-acento-lado: #0ea5e9;  /* lateral do elemento principal */
--ui-acento-fundo:#0c4a6e;  /* sombra do elemento principal, fundos de ícone */
--ui-erro:        #f472b6;  /* rosa: erro, retry, status de falha */
--ui-legenda:     #737373;  /* legenda mono */
```

Regras de cor:
- **Um acento por figura.** O ciano marca o protagonista (o "hub", o serviço que a figura explica) e os caminhos ativos. Todo o resto é cinza.
- O **rosa** é só para estado de falha (um card com ×, um `retry · 503`). Não use rosa decorativo.
- Sem verde de sucesso: sucesso é o ciano (um ✓ ciano). Mantém a figura em duas cores de sinal no máximo.
- Brilho sutil só no acento: `filter: drop-shadow(0 0 6px rgb(56 189 248 / .35))`. Nada de glow em cinza.

## Geometria

- Isométrico verdadeiro, com `scripts/iso.py rbox` para placas de **cantos arredondados** (raio 8–16 em unidades do mundo). É o arredondado que dá o ar de UI; caixas de canto vivo ficam com cara de Blueprint.
- **Plataforma**: uma placa grande e baixa (`h` 4–8) que segura tudo, com uma segunda borda interna em traço fino (o "trilho") a ~12 unidades da borda. Outras placas menores podem flutuar acima dela.
- **Objetos**: placas empilhadas (servidor = 3 placas com riscos e LED), cubo arredondado (o hub, sempre em ciano), cards baixos com um ícone no topo (✓, ×, +, envelope, cadeado), chips quadrados pequenos alinhados (fila).
- Peças prontas em `cena_ui.py`: `plataforma`, `pilha` (servidor/fila), `hub` (protagonista), `card`, `placa`, `fantasma`, `chips`, `monitor` (PC), `disco` (com LED e estado de falha), `banco` (cilindros), `fio` (com vários `pacotes` defasados) e `rotulo_fio`. Se a cena pedir uma peça que não existe, crie-a no seu gerador seguindo o mesmo padrão (`_rbox` + riscos + `_tag` no canto de trás do topo).
- **Card fantasma**: contorno tracejado ciano sem preenchimento = algo que vai ser criado, um slot vazio, um endpoint pendente.
- Traço 1px em tudo, `stroke-linejoin="round"`. Ícones-símbolo (✓ × + cadeado) desenhados em espaço de tela achatado na vertical — no plano isométrico um × vira um +; objetos deitados (envelope, riscos) desenhados no plano. `cena_ui.py` já faz isso.
- Luz: topo mais claro que a lateral. Sem a terceira face pervinca do Blueprint — a lateral visível é uma só faixa contínua, porque o `rbox` gera o contorno arredondado.

## Conectores

- Linhas tracejadas ciano (`stroke-dasharray="4 4"`, 1.25px) correndo no plano da plataforma, com cotovelos em ângulo reto isométrico (seguem os eixos X e Y projetados, nunca diagonal livre).
- Pontinho ou chip pequeno onde o conector toca o objeto.
- Conector inativo: mesmo tracejado em `--ui-traco`.

## Legenda

Dentro do cartão, embaixo, em mono 13px:
- à esquerda, o fluxo em `--ui-legenda`: `producer → hub → endpoints`
- à direita, o estado em `--ui-erro` ou `--ui-acento`: `retry · 503`, `synced · 12ms`

Texto em minúsculas, como log de terminal. Quando a figura parada precisa distinguir caminhos (hit × miss, ida × volta), use rótulos curtos deitados sobre os fios (`rotulo_fio`, ex. `hit · 2ms`) — no máximo três, ao lado do tracejado, nunca sobre ele, e no fim da lista de peças para ficarem por cima. Termos de software ficam em inglês quando são o vocabulário real (`retry`, `hub`, `queue`); conceitos gerais em português se o pedido for em português (`fila → processador → destinos`). Siga o idioma do pedido para a legenda descritiva.

## Animação (sutil)

Tudo em CSS dentro do SVG/HTML, sem biblioteca. A animação conta a história do fluxo, em loop de 3–6 s:

- **Fluxo**: `stroke-dashoffset` animado nos conectores ativos (o tracejado "anda" na direção do fluxo).
- **Pacote**: um pequeno losango ciano percorrendo o conector com `offset-path: path(...)` + `offset-distance` de 0% a 100%.
- **Hub respirando**: `filter: drop-shadow` oscilando entre .25 e .45 de opacidade, 2,4 s.
- **Falha**: o card de erro pisca o × em rosa uma vez por ciclo; a legenda de estado troca de `delivered` para `retry · 503` no mesmo instante (dois `<tspan>` alternando opacidade com o mesmo `animation-delay`).
- Peças prontas em `cena_ui.py`: `plataforma`, `pilha` (servidor/fila), `hub` (protagonista), `card`, `placa`, `fantasma`, `chips`, `monitor` (PC), `disco` (com LED e estado de falha), `banco` (cilindros), `fio` (com vários `pacotes` defasados) e `rotulo_fio`. Se a cena pedir uma peça que não existe, crie-a no seu gerador seguindo o mesmo padrão (`_rbox` + riscos + `_tag` no canto de trás do topo).
- **Card fantasma**: tracejado girando devagar (`stroke-dashoffset` lento).

Amplitude pequena: nada salta mais que 2–3px, nada muda de escala mais que 3%. Ease `cubic-bezier(.4,0,.2,1)`.

Obrigatório: `@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }` — a figura parada tem que fazer sentido sozinha.

## Interação

- **Hover em um objeto**: ele sobe 3px (`transform: translateY(-3px)`), o traço vai para `--ui-traco-forte` (ou o acento fica mais claro), e aparece um rótulo mono pequeno flutuando acima dele (`hub · 3 workers`). Os outros objetos baixam a opacidade para .55.
- **Hover em um conector**: o tracejado fica sólido e mais claro, o pacote acelera.
- **Clique** (opcional, quando a figura explica estados): alterna o cenário — ex. clicar no endpoint com erro dispara o "retry" e o card vira ✓ ciano.
- Cada objeto interativo é um `<g class="obj" tabindex="0" data-rotulo="...">` com `aria-label`; `:focus-visible` faz o mesmo que o hover, para funcionar no teclado.
- Todo o JS cabe num `<script>` curto no HTML; o `.svg` solto mantém só a animação CSS (sem JS), para continuar funcionando como imagem.

## Cartão

O desenho mora num cartão: fundo `--ui-cartao`, borda 1px `--ui-cartao-borda`, raio 16px, padding 24px, proporção ~4:3. No HTML, a página em volta é `--ui-pagina`. Sem título grande — se precisar, um rótulo mono 12px em `--ui-legenda` no canto superior esquerdo.
