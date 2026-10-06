import test from "node:test";
import assert from "node:assert/strict";
import { validateFields } from "./fields.mjs";

const ctx = {
  slugs: new Map([["people", new Set(["ana"])], ["projects", new Set()]]),
  media: [{ output: "/assets/uploads/images", input: "src/assets/uploads/images" }],
  fileExists: (p) => p === "src/assets/uploads/images/a.png",
};
const run = (fields, data) => validateFields(fields, data, ctx).map((e) => `${e.field}: ${e.message}`);

test("campo obrigatório ausente, nulo, vazio ou lista vazia", () => {
  const f = [{ name: "t", type: "string", required: true }];
  for (const d of [{}, { t: null }, { t: "" }]) assert.match(run(f, d)[0], /^t: obrigatório/);
  const l = [{ name: "l", type: "string", list: true, required: true }];
  assert.match(run(l, { l: [] })[0], /^l: obrigatório/);
});

test("false e 0 contam como preenchidos", () => {
  assert.deepEqual(run([{ name: "b", type: "boolean", required: true }], { b: false }), []);
  assert.deepEqual(run([{ name: "n", type: "number", required: true }], { n: 0 }), []);
});

test("campo fora do schema é erro", () => {
  assert.match(run([{ name: "a", type: "string" }], { a: "x", typo: 1 })[0], /^typo: .*não existe no schema/);
});

test("tipos escalares", () => {
  assert.match(run([{ name: "s", type: "string" }], { s: 3 })[0], /^s: .*texto/);
  assert.match(run([{ name: "n", type: "number" }], { n: "2020" })[0], /^n: .*número/);
  assert.match(run([{ name: "b", type: "boolean" }], { b: "sim" })[0], /^b: .*verdadeiro/);
});

test("pattern como objeto com regex", () => {
  const f = [{ name: "slug", type: "string", pattern: { regex: "^[a-z0-9-]+$", message: "Slug inválido." } }];
  assert.deepEqual(run(f, { slug: "ok-1" }), []);
  assert.equal(run(f, { slug: "Não OK" })[0], "slug: Slug inválido.");
});

test("data aceita ISO, Date do YAML e vazio; rejeita calendário impossível", () => {
  const f = [{ name: "d", type: "date" }];
  assert.deepEqual(run(f, { d: "2026-09-10" }), []);
  assert.deepEqual(run(f, { d: new Date("2026-09-10T00:00:00Z") }), []);
  assert.deepEqual(run(f, { d: "" }), []);
  assert.match(run(f, { d: "2026-02-31" })[0], /^d: .*data/);
  assert.match(run(f, { d: "10/09/2026" })[0], /^d: .*data/);
});

test("select só aceita valores das opções", () => {
  const f = [{ name: "s", type: "select", options: { values: [{ name: "a" }, { name: "b" }] } }];
  assert.deepEqual(run(f, { s: "a" }), []);
  assert.match(run(f, { s: "c" })[0], /^s: .*"c".*a, b/);
});

test("lista de escalares valida cada item", () => {
  const f = [{ name: "k", type: "string", list: true }];
  assert.deepEqual(run(f, { k: ["a", "b"] }), []);
  assert.match(run(f, { k: "a" })[0], /^k: .*lista/);
  assert.match(run(f, { k: ["a", 2] })[0], /^k\[1\]: /);
});

test("referência simples e múltipla checam existência por slug", () => {
  const one = [{ name: "p", type: "reference", options: { collection: "people", value: "{fields.slug}" } }];
  assert.deepEqual(run(one, { p: "ana" }), []);
  assert.match(run(one, { p: "bia" })[0], /^p: .*"bia".*people/);
  const many = [{ name: "ps", type: "reference", options: { collection: "people", multiple: true, value: "{fields.slug}" } }];
  assert.deepEqual(run(many, { ps: ["ana"] }), []);
  assert.match(run(many, { ps: ["ana", "bia"] })[0], /^ps\[1\]: /);
  assert.match(run(many, { ps: "ana" })[0], /^ps: .*lista/);
});

test("referência com coleção ou value não suportados falha explicitamente", () => {
  const f = [{ name: "p", type: "reference", options: { collection: "nada", value: "{fields.slug}" } }];
  assert.match(run(f, { p: "x" })[0], /coleção "nada" não existe/);
  const g = [{ name: "p", type: "reference", options: { collection: "people", value: "{primary}" } }];
  assert.match(run(g, { p: "ana" })[0], /value.*não suportado/);
});

test("imagem/arquivo: prefixo de mídia conhecido e arquivo existente", () => {
  const f = [{ name: "i", type: "image" }];
  assert.deepEqual(run(f, { i: "/assets/uploads/images/a.png" }), []);
  assert.match(run(f, { i: "/assets/uploads/images/b.png" })[0], /^i: .*não existe/);
  assert.match(run(f, { i: "/outro/a.png" })[0], /^i: .*pasta de mídia/);
});

test("objeto aninhado usa caminho com ponto", () => {
  const f = [{ name: "seo", type: "object", fields: [{ name: "title", type: "string", required: true }] }];
  assert.deepEqual(run(f, { seo: { title: "x" } }), []);
  assert.match(run(f, { seo: {} })[0], /^seo\.title: obrigatório/);
  assert.match(run(f, { seo: "x" })[0], /^seo: .*objeto/);
});

test("bloco: escolhe pela chave, valida campos do bloco e rejeita tipo desconhecido", () => {
  const f = [{
    name: "c", type: "block", list: true, blockKey: "kind",
    blocks: [
      { name: "internal", fields: [{ name: "person", type: "reference", required: true, options: { collection: "people", value: "{fields.slug}" } }] },
      { name: "external", fields: [{ name: "name", type: "string", required: true }] },
    ],
  }];
  assert.deepEqual(run(f, { c: [{ kind: "internal", person: "ana" }, { kind: "external", name: "Z" }] }), []);
  assert.match(run(f, { c: [{ kind: "internal" }] })[0], /^c\[0\]\.person: obrigatório/);
  assert.match(run(f, { c: [{ kind: "x" }] })[0], /^c\[0\]\.kind: .*internal, external/);
  assert.match(run(f, { c: [{ kind: "external", name: "Z", extra: 1 }] })[0], /^c\[0\]\.extra: .*schema/);
});

test("tipo de campo desconhecido falha em vez de passar", () => {
  assert.match(run([{ name: "x", type: "color" }], { x: "red" })[0], /^x: .*tipo "color" não suportado/);
});
