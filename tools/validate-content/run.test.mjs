import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { runValidation } from "./run.mjs";

const YML = `
media: []
components: {}
content:
- name: people
  type: collection
  path: src/content/people
  filename: { template: '{fields.slug}.md' }
  fields:
  - { name: slug, type: string, required: true }
  - { name: name, type: string, required: true }
  - { name: body, type: rich-text, required: true }
- name: projects
  type: collection
  path: src/content/projects
  filename: { template: '{fields.year}-{fields.slug}.md' }
  fields:
  - { name: slug, type: string, required: true }
  - { name: year, type: number, required: true }
  - { name: lead, type: reference, options: { collection: people, value: '{fields.slug}' } }
`;

function fixture(files) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "vc-"));
  fs.writeFileSync(path.join(root, ".pages.yml"), YML);
  for (const d of ["people", "projects"]) fs.mkdirSync(path.join(root, "src/content", d), { recursive: true });
  for (const [f, c] of Object.entries(files)) fs.writeFileSync(path.join(root, "src/content", f), c);
  return root;
}
const run = (files) => {
  const r = runValidation({ root: fixture(files) });
  return { errors: r.errors.map((e) => `${e.file}|${e.field}|${e.message}`), warnings: r.warnings };
};
const OK = { "people/ana.md": "---\nslug: ana\nname: Ana\n---\nTexto.\n" };

test("conteúdo válido passa", () => {
  const r = run({ ...OK, "projects/2026-p.md": "---\nslug: p\nyear: 2026\nlead: ana\n---\n" });
  assert.deepEqual(r.errors, []);
});

test("body vem do corpo do arquivo, não do frontmatter", () => {
  const r = run({ "people/ana.md": "---\nslug: ana\nname: Ana\n---\n" });
  assert.match(r.errors[0], /people\/ana\.md\|body\|obrigatório/);
});

test("referência quebrada é erro com arquivo e campo", () => {
  const r = run({ ...OK, "projects/2026-p.md": "---\nslug: p\nyear: 2026\nlead: zé\n---\n" });
  assert.match(r.errors[0], /projects\/2026-p\.md\|lead\|aponta para "zé", que não existe em people/);
});

test("nome de arquivo diferente do template é erro", () => {
  const r = run({ ...OK, "projects/p.md": "---\nslug: p\nyear: 2026\n---\n" });
  assert.match(r.errors[0], /projects\/p\.md\|\(arquivo\)\|.*2026-p\.md/);
});

test("slug duplicado na mesma coleção é erro", () => {
  const r = run({ ...OK, "projects/2025-p.md": "---\nslug: p\nyear: 2025\n---\n", "projects/2026-p.md": "---\nslug: p\nyear: 2026\n---\n" });
  assert.ok(r.errors.some((e) => /slug\|.*"p".*já é usado/.test(e)), r.errors.join("\n"));
});

test("pasta inesperada e arquivo que não é .md são erros", () => {
  const root = fixture(OK);
  fs.mkdirSync(path.join(root, "src/content/intrusa"));
  fs.writeFileSync(path.join(root, "src/content/people/lixo.txt"), "x");
  const msgs = runValidation({ root }).errors.map((e) => `${e.file}|${e.message}`);
  assert.ok(msgs.some((m) => /intrusa.*não é uma coleção/.test(m)));
  assert.ok(msgs.some((m) => /lixo\.txt.*\.md/.test(m)));
});

test("frontmatter YAML inválido vira erro, não exceção", () => {
  const r = run({ "people/x.md": "---\nslug: [\n---\n" });
  assert.match(r.errors[0], /people\/x\.md\|\(frontmatter\)\|/);
});

test("slug do arquivo difere do slug do frontmatter já cai no template", () => {
  const r = run({ "people/outro.md": "---\nslug: ana\nname: A\n---\nx" });
  assert.match(r.errors[0], /\(arquivo\)/);
});

test("erro traz os nomes do CMS: coleção, título do registro, campo e opção (caso C7, #90)", () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "vc-"));
  fs.writeFileSync(path.join(root, ".pages.yml"), `
media: []
components: {}
content:
- name: productions
  label: Produções
  type: collection
  path: src/content/productions
  filename: { template: '{fields.slug}.md' }
  fields:
  - { name: slug, type: string, required: true }
  - { name: title, label: Título oficial, type: string, required: true }
  - { name: productionType, label: Tipo específico, type: select, options: { values: [{ name: book, label: Livro }, { name: other, label: Outro }] } }
  - { name: otherTypeLabel, label: "Se “Outro”, qual?", type: string }
`);
  fs.mkdirSync(path.join(root, "src/content/productions"), { recursive: true });
  fs.writeFileSync(path.join(root, "src/content/productions/t.md"), "---\nslug: t\ntitle: Teste de Título\nproductionType: other\n---\n");
  const [e] = runValidation({ root }).errors;
  assert.equal(e.collection, "Produções");
  assert.equal(e.record, "Teste de Título");
  assert.equal(e.fieldLabel, "Se “Outro”, qual?");
  assert.equal(e.message, "obrigatório quando “Tipo específico” é “Outro”");
  assert.equal(e.field, "otherTypeLabel");
});
