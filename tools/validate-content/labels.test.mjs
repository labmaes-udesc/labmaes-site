import test from "node:test";
import assert from "node:assert/strict";
import { fieldLabel, resolveTokens, recordTitle } from "./labels.mjs";

const FIELDS = [
  { name: "title", label: "Título oficial", type: "string" },
  { name: "productionType", label: "Tipo específico", type: "select", options: { values: [{ name: "book", label: "Livro" }, { name: "other", label: "Outro" }] } },
  { name: "otherTypeLabel", label: "Se “Outro”, qual?", type: "string" },
  { name: "seo", label: "SEO e compartilhamento", type: "object", fields: [{ name: "title", label: "Título para buscadores", type: "string" }] },
  {
    name: "contributors", label: "Pessoas autoras / colaboradoras", type: "block", list: true, blockKey: "kind",
    blocks: [
      { name: "internal", fields: [{ name: "person", label: "Integrante cadastrado", type: "reference" }] },
      { name: "external", fields: [{ name: "name", label: "Nome", type: "string" }] },
    ],
  },
  { name: "keywords", label: "Palavras-chave", type: "string", list: true },
];
const DATA = { contributors: [{ kind: "external", name: "Z" }, { kind: "internal", person: "ana" }] };

test("campo simples, objeto, lista e bloco viram o caminho que aparece no CMS", () => {
  assert.equal(fieldLabel(FIELDS, "otherTypeLabel", DATA), "Se “Outro”, qual?");
  assert.equal(fieldLabel(FIELDS, "seo.title", DATA), "SEO e compartilhamento › Título para buscadores");
  assert.equal(fieldLabel(FIELDS, "keywords[2]", DATA), "Palavras-chave › 3º item");
  assert.equal(fieldLabel(FIELDS, "contributors[1].person", DATA), "Pessoas autoras / colaboradoras › 2º item › Integrante cadastrado");
});

test("campo fora do schema e pseudo-campos continuam legíveis", () => {
  assert.equal(fieldLabel(FIELDS, "typo", DATA), "typo");
  assert.equal(fieldLabel(FIELDS, "(arquivo)", DATA), "nome do arquivo");
  assert.equal(fieldLabel(FIELDS, "(frontmatter)", DATA), "cabeçalho do arquivo");
});

test("tokens de campo e de opção nas mensagens viram os nomes do CMS", () => {
  assert.equal(
    resolveTokens("obrigatório quando «opção:productionType:other» em «campo:productionType»", FIELDS),
    "obrigatório quando “Outro” em “Tipo específico”",
  );
  assert.equal(resolveTokens("sem tokens", FIELDS), "sem tokens");
});

test("título do registro: título, nome ou slug", () => {
  assert.equal(recordTitle({ title: "Teste de Título", slug: "t" }), "Teste de Título");
  assert.equal(recordTitle({ name: "Ana Teste", slug: "a" }), "Ana Teste");
  assert.equal(recordTitle({ slug: "s" }), "s");
  assert.equal(recordTitle({}), null);
});
