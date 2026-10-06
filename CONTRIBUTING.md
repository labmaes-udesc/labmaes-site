# Como contribuir

Obrigado pelo interesse no site do LabMAES — Laboratório de Moda, Arte, Ensino e Sociedade
(UDESC/CEART). Este guia vale para a equipe do laboratório, bolsistas e qualquer pessoa de fora
que queira ajudar.

Ao participar, você concorda com o [Código de Conduta](CODE_OF_CONDUCT.md).

## Formas de contribuir

| Quero… | Caminho |
| --- | --- |
| avisar de um erro no site | [abrir issue "Problema no site"](../../issues/new?template=1-bug.yml) |
| corrigir um texto, data, nome ou documento | [abrir issue "Correção de conteúdo"](../../issues/new?template=2-conteudo.yml) — ou editar pelo Pages CMS, se você faz parte da equipe editorial |
| propor uma funcionalidade ou melhoria | [abrir issue "Tarefa ou funcionalidade"](../../issues/new?template=3-tarefa.yml) |
| levantar uma questão de arquitetura ou política editorial | [abrir issue "Decisão"](../../issues/new?template=4-decisao.yml) |
| escrever código | escolher uma issue (as marcadas com `good first issue` são um bom começo) e seguir o fluxo abaixo |
| reportar falha de segurança ou exposição de dados | **não abra issue pública** — veja [SECURITY.md](SECURITY.md) |

## Como o trabalho é organizado

- **Milestones** correspondem às fases do redesign (ver [docs/roadmap.md](docs/roadmap.md)),
  mais uma milestone contínua de manutenção e governança.
- **Issues** são a unidade de trabalho. Toda mudança relevante começa por uma issue.
- **Labels** seguem os prefixos `tipo:`, `área:`, `prioridade:` e `status:` (definidos em
  [.github/labels.json](.github/labels.json); sincronizar com `node tools/github/sync-labels.mjs`).
- **Documentação de decisão** fica em `docs/`, com esta ordem de precedência:
  ADR aceito → spec da fase → plan → documentação operacional → brainstorming
  (ver [docs/architecture/README.md](docs/architecture/README.md)).

## Ambiente local

Pré-requisitos: Node.js na versão do [.nvmrc](.nvmrc) e Git.

```bash
npm ci
npm start                 # preview em http://localhost:8080
npm run build             # gera _site/
npm run validate:content  # valida src/content contra o .pages.yml
```

## Fluxo de mudança

1. **Branch a partir da `main`**, com prefixo pelo tipo de trabalho:
   `feat/…`, `fix/…`, `docs/…`, `chore/…`, `content/…` ou `redesign/fase-N-…`.
2. **Commits no padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/)**,
   em português, no imperativo e com escopo quando ajudar:
   `feat(anais): …`, `fix(submissoes): …`, `docs(plan): …`, `chore(cms): …`.
3. **Pull request para a `main`**, preenchendo o modelo e citando a issue com `Closes #N` (o GitHub só reconhece as palavras-chave em inglês — `Closes`, `Fixes`, `Resolves` — para fechar a issue no merge).
   A CI roda build e validação de conteúdo; o PR só é mesclado com a CI verde e pelo menos
   uma revisão.
4. **Publicação:** todo merge na `main` é publicado automaticamente pelo Cloudflare Pages.
   Por isso a `main` precisa estar sempre publicável.

## Regras do projeto

- **Dados pessoais:** nunca commite documentos com dados pessoais sensíveis (saúde, CPF,
  endereço, notas, avaliações), nem para teste. Para testes, use apenas os fixtures fictícios
  (`slug: fixture-*`). O repositório é público e o histórico do Git é permanente.
- **Links privados:** não publique links, IDs ou senhas de salas de videoconferência.
- **URLs públicas são estáveis:** se uma rota mudar, acrescente o redirect em `_redirects`.
- **Acessibilidade:** WCAG 2.2 AA é requisito mínimo ([ADR 0005](docs/architecture/adr/0005-acessibilidade.md)).
  Interfaces novas devem funcionar por teclado, ter contraste adequado e texto alternativo.
- **Idiomas:** PT-BR na raiz; EN/ES/FR em prefixos. Tradução ausente não gera página mista
  ([ADR 0004](docs/architecture/adr/0004-i18n.md)).
- **Conteúdo estruturado:** registros em `src/content/` seguem o schema do `.pages.yml`
  ([ADR 0003](docs/architecture/adr/0003-modelo-conteudo.md), [ADR 0007](docs/architecture/adr/0007-validacao-conteudo.md)).
  Slugs são identificadores permanentes — não renomeie.
- **Arquivos gerados:** `_data/apoiadores.json` é gerado por `tools/gerar_apoiadores_json.py`;
  não edite à mão.
- **Decisões novas** que afetem a arquitetura viram ADR em `docs/architecture/adr/`.

## Equipe editorial (Pages CMS)

Antes de editar, leia a [política editorial](docs/politica-editorial.md): quem publica, que
documentos podem entrar e o que é traduzido.

Quem edita conteúdo pelo Pages CMS não precisa de Git nem de pull request: o CMS grava direto na
`main`, e um registro só aparece no site quando seu status editorial é "Publicado"
([ADR 0008](docs/architecture/adr/0008-publicacao-direta-cms.md)). A CI valida cada edição e avisa
se algo quebrar. Limite prático de upload pelo CMS: cerca de 2,5 MB por arquivo; arquivos maiores
são incluídos por commit direto.
