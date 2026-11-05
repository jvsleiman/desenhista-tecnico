# desenhista-tecnico

Skill do Claude para desenho técnico em dois estilos:

- **Blueprint** — tinta azul sobre papel, estilo livro técnico (vista explodida, corte, diagrama, planta com cotas ABNT, página explicativa).
- **UI** — ilustração isométrica escura com um acento ciano, animada e interativa (landing, app, Mostruário).

A cena é descrita em JSON e os scripts geram o `.svg` e o `.html`:

```bash
python3 scripts/cena_blueprint.py --exemplo-json > cena.json && python3 scripts/cena_blueprint.py cena.json saida
python3 scripts/cena_ui.py --exemplo saida
python3 scripts/verifica.py saida.svg --estilo ui --png render.png
```

O `SKILL.md` é o ponto de entrada para o Claude; `references/` traz as regras de cada estilo e modo; `evals/` os casos de teste.
