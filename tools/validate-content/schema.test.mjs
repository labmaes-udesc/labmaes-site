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
