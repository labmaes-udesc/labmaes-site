import test from "node:test";
import assert from "node:assert/strict";
import { parseSchema } from "./schema.mjs";

const YML = `
media:
- name: images
  input: src/assets/uploads/images
  output: /assets/uploads/images
components:
  seo:
    type: object
    label: SEO
    fields:
    - name: title
      type: string
content:
- name: grupo
  type: group
  items:
  - name: pages
    type: collection
    path: src/content/pages
    filename:
      template: '{fields.slug}.md'
    fields:
    - name: slug
      type: string
    - name: seo
      component: seo
      label: SEO da página
`;

test("achata grupos e expõe coleções por nome", () => {
  const s = parseSchema(YML);
  assert.deepEqual([...s.collections.keys()], ["pages"]);
  assert.equal(s.collections.get("pages").dir, "src/content/pages");
  assert.equal(s.collections.get("pages").filenameTemplate, "{fields.slug}.md");
});

test("expande componentes mesclando as chaves do próprio campo", () => {
  const f = parseSchema(YML).collections.get("pages").fields[1];
  assert.equal(f.type, "object");
  assert.equal(f.label, "SEO da página");
  assert.equal(f.fields[0].name, "title");
});

test("expõe as pastas de mídia", () => {
  assert.deepEqual(parseSchema(YML).media, [{ output: "/assets/uploads/images", input: "src/assets/uploads/images" }]);
});

test("componente inexistente é erro", () => {
  assert.throws(() => parseSchema(YML.replace("component: seo", "component: nada")), /componente "nada"/);
});

test("coleção sem filename.template é erro", () => {
  assert.throws(() => parseSchema(YML.replace("template: '{fields.slug}.md'", "x: 1")), /filename\.template/);
});

// Sem nenhum registro preenchendo o campo: o schema sozinho precisa falhar (ADR 0007).
const withField = (field) => YML.replace("    - name: seo\n", `${field}    - name: seo\n`);

test("tipo de campo não suportado é erro mesmo sem conteúdo", () => {
  assert.throws(() => parseSchema(withField("    - name: notas\n      type: code\n")), /pages\.notas: tipo "code" não suportado/);
});

test("tipo não suportado dentro de objeto ou bloco também é erro", () => {
  const obj = "    - name: o\n      type: object\n      fields:\n      - name: c\n        type: color\n";
  assert.throws(() => parseSchema(withField(obj)), /pages\.o\.c: tipo "color"/);
  const blk = "    - name: b\n      type: block\n      blockKey: kind\n      blocks:\n      - name: x\n        fields:\n        - name: c\n          type: color\n";
  assert.throws(() => parseSchema(withField(blk)), /pages\.b\.x\.c: tipo "color"/);
});

test("referência para coleção inexistente ou com value não suportado é erro", () => {
  const ref = (opts) => `    - name: r\n      type: reference\n      options:\n${opts}`;
  assert.throws(() => parseSchema(withField(ref("        collection: nada\n        value: '{fields.slug}'\n"))), /pages\.r: .*coleção "nada"/);
  assert.throws(() => parseSchema(withField(ref("        collection: pages\n        value: '{fields.title}'\n"))), /pages\.r: .*value/);
});

test("bloco sem blockKey é erro", () => {
  const blk = "    - name: b\n      type: block\n      blocks:\n      - name: x\n        fields: []\n";
  assert.throws(() => parseSchema(withField(blk)), /pages\.b: .*blockKey/);
});
