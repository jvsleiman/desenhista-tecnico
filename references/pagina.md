# Página explicativa (estilo livro técnico)

Um artigo longo que explica como algo funciona, com prosa serifada e figuras azuis, montado como uma página de livro. É o formato do próprio site Making Software. Os componentes detalhados (masthead, divisor de glifos, sumário, FAQ IN/OUT, rodapé datilografado) estão em `estilo-making-software.md`; use os que a página pedir, não todos.

## Estrutura

1. **Masthead** (128px): título do assunto em mono grande Azul Blueprint à esquerda (o único tipo grande da página — pode ser em "pixel", letras maiúsculas espaçadas na Departure Mono a ~40px); à direita, duas linhas serifadas de 16px: a frase de abertura e o autor.
2. **Divisor de glifos**: uma linha de `-- -- -- --` em cinza ocupando a largura, com o nome do assunto em mono 12px no centro.
3. **Abertura assimétrica**: coluna estreita (~430px) de prosa justificada com capitular de duas linhas à esquerda, e a figura principal ocupando os dois terços da direita.
4. **Seções**: alternam figura larga e coluna curta de texto, separadas por bastante espaço vazio (~160–256px). Títulos de seção em mono 14px maiúsculo numerado (`02 · O PRATO MAGNÉTICO`).
5. **Fecho**: um FAQ IN/OUT curto se houver dúvidas comuns, e o rodapé datilografado (`***` centralizado e linhas mono com pipes).

## Texto

- Escreva em português claro, como um bom livro de divulgação técnica: começa pelo que a pessoa já conhece, chega ao mecanismo, termina na consequência prática.
- Prosa EB Garamond 14px, entrelinha 22.4px, justificada com `hyphens: auto` e `lang="pt-BR"` no `<html>`, para a justificação não abrir buracos.
- Referencie as figuras no texto (`como se vê na FIG_002`).

## Técnica

- Um único arquivo HTML autocontido: SVGs inline, CSS no `<style>`. Cada figura também é salva como `.svg` separado.
- Fontes: EB Garamond pelo Google Fonts; Departure Mono por `https://cdn.jsdelivr.net/npm/@fontsource/departure-mono/index.css` se carregar, com a pilha de fallback mono. A página tem que ficar bonita mesmo se nenhuma fonte externa carregar.
- Largura máxima 1536px, margens laterais 72px; abaixo de 900px tudo vira uma coluna e as figuras ocupam 100%.
- Nada de sombras, cartões preenchidos ou faixas coloridas. Separação vem de espaço vazio, linhas finas `#e1e1e1` e réguas de 1px em tinta.
