# design-systems/

Design system do novo site do LabMAES (Fase 2 do redesign). Spec:
`docs/superpowers/specs/2026-10-07-redesign-fase-2-design-system-design.md`.

| Pasta | O que é | Fonte ou saída |
|---|---|---|
| `marca/` | Camada de marca (`marca.css`), exceções à skill, guia e log da IA, texturas aprovadas | Fonte |
| `telas/0N-*/` | Telas-chave construídas com a skill design-taste-frontend 2.5.1 | Fonte (só `index.html`, capturas, `verificacao.md` e `waivers.json` vão para o git) |
| `telas/index.html` | Hub que liga as telas; entrada do `/extract-ds` | Fonte |
| `labmaes/` | Catálogo extraído: `design-system.html`, `styles.css`, `interactions.js`, `assets/` | Saída do `/extract-ds`; fonte da verdade do site |

## Como regenerar

- Recriar a pasta local de uma tela (kit, marca, fontes, texturas): `tools/ds/preparar-tela.sh 01-home`.
- Verificar uma tela: os comandos da Tarefa B0 do plan da Fase 2.
- Regerar o catálogo: o usuário invoca o `/extract-ds` com o texto da Tarefa E1 do plan.

O site publica só `labmaes/`, em `/design-system/`. As telas nunca vão para o site.
