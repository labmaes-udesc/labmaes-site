import test from "node:test";
import assert from "node:assert/strict";
import { recordRules, filenameFor } from "./rules.mjs";

const msgs = (c, d) => recordRules(c, d).map((e) => `${e.level}|${e.field}: ${e.message}`);

test("other exige otherTypeLabel, em tipo ou categoria", () => {
  assert.match(msgs("productions", { productionType: "other" })[0], /^error\|otherTypeLabel: .*obrigatório/);
  assert.match(msgs("productions", { productionCategory: "other" })[0], /^error\|otherTypeLabel/);
  assert.deepEqual(msgs("productions", { productionType: "other", otherTypeLabel: "X" }), []);
});

test("otherTypeLabel sem other gera aviso, não erro", () => {
  assert.match(msgs("productions", { productionType: "book", productionCategory: "bibliographic", otherTypeLabel: "X" })[0], /^warning\|otherTypeLabel/);
});

test("ano da produção confere com o ano da data, quando há data", () => {
  assert.deepEqual(msgs("productions", { year: 2025, date: "2025-03-01" }), []);
  assert.match(msgs("productions", { year: 2024, date: "2025-03-01" })[0], /^error\|year: .*2025/);
  assert.deepEqual(msgs("productions", { year: 2024, date: "" }), []);
});

test("intervalos de datas: início não pode ser depois do fim", () => {
  assert.match(msgs("projects", { startDate: "2026-02-01", endDate: "2026-01-01" })[0], /^error\|endDate/);
  assert.deepEqual(msgs("projects", { startDate: "2026-01-01", endDate: "" }), []);
  assert.match(msgs("people", { membershipStart: "2026-02-01", membershipEnd: "2026-01-01" })[0], /^error\|membershipEnd/);
  assert.match(msgs("event_editions", { startDate: "2026-08-23", endDate: "2026-08-18" })[0], /^error\|endDate/);
});

test("edição de evento: ano confere com startDate", () => {
  assert.match(msgs("event_editions", { year: 2025, startDate: "2026-08-18" })[0], /^error\|year/);
  assert.deepEqual(msgs("event_editions", { year: 2026, startDate: "2026-08-18" }), []);
});

test("contributors: mesma pessoa interna repetida é erro; externos podem repetir nome com aviso", () => {
  const dup = { contributors: [{ kind: "internal", person: "ana" }, { kind: "internal", person: "ana", role: "Revisão" }] };
  assert.match(msgs("productions", dup)[0], /^error\|contributors\[1\]\.person: .*"ana".*contributors\[0\]/);
  const ok = { contributors: [{ kind: "internal", person: "ana" }, { kind: "external", name: "Z" }] };
  assert.deepEqual(msgs("productions", ok), []);
});

test("ORCID malformado gera aviso (id puro ou URL são aceitos)", () => {
  const c = (orcid) => ({ contributors: [{ kind: "external", name: "Z", orcid }] });
  assert.deepEqual(msgs("productions", c("0000-0002-1825-0097")), []);
  assert.deepEqual(msgs("productions", c("https://orcid.org/0000-0002-1825-009X")), []);
  assert.match(msgs("productions", c("123"))[0], /^warning\|contributors\[0\]\.orcid/);
  assert.match(msgs("people", { orcid: "abc" })[0], /^warning\|orcid/);
});

test("filenameFor renderiza o template com os campos", () => {
  assert.equal(filenameFor("{fields.year}-{fields.slug}.md", { year: 2025, slug: "a" }), "2025-a.md");
  assert.equal(filenameFor("{fields.date}-{fields.slug}.md", { date: "2026-01-02", slug: "n" }), "2026-01-02-n.md");
  assert.equal(filenameFor("{fields.x}.md", {}), null);
});
