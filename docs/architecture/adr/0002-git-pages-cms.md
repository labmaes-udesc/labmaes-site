# ADR 0002 — Git como fonte da verdade e Pages CMS como interface editorial

- Status: Aceito
- Data: 2026-09-04

## Contexto

A atualização direta de Nunjucks/JSON exige conhecimento técnico e reduz a autonomia
das bolsistas. Ao mesmo tempo, o projeto se beneficia de conteúdo versionado no Git.

## Decisão

Manter o GitHub como fonte da verdade do conteúdo e adotar Pages CMS como primeira
interface editorial a ser implementada e validada.

## Consequências

- conteúdo permanece portável e auditável;
- bolsistas não precisam editar Git/YAML diretamente;
- commits gerados pelo CMS continuam acionando o fluxo de deploy;
- o Pages CMS deve ser validado com usuários antes de ser considerado definitivo;
- trocar de CMS não deve exigir migrar o conteúdo para banco proprietário.
