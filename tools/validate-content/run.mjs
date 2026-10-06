import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { loadSchema } from "./schema.mjs";
import { validateFields, normalizeDate } from "./fields.mjs";
import { recordRules, filenameFor } from "./rules.mjs";

const CONTENT = "src/content";
const IGNORED = new Set([".gitkeep"]);

function normalize(value) {
  if (value instanceof Date) return normalizeDate(value) ?? value;
  if (Array.isArray(value)) return value.map(normalize);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, normalize(v)]));
  }
  return value;
}

export function runValidation({ root = process.cwd() } = {}) {
  const errors = [];
  const warnings = [];
  const add = (level, file, field, message) => (level === "error" ? errors : warnings).push({ file, field, message });
  const schema = loadSchema(path.join(root, ".pages.yml"));
  const contentDir = path.join(root, CONTENT);

  if (!fs.existsSync(contentDir)) {
    add("error", CONTENT, "(pasta)", "src/content não existe");
    return { errors, warnings };
  }

  const byDir = new Map([...schema.collections.values()].map((c) => [path.posix.basename(c.dir), c]));
  for (const e of fs.readdirSync(contentDir, { withFileTypes: true })) {
    if (e.isDirectory() && !byDir.has(e.name)) {
      add("error", `${CONTENT}/${e.name}`, "(pasta)", "não é uma coleção definida no .pages.yml");
    }
  }

  // 1ª passada: ler registros.
  const records = [];
  for (const col of schema.collections.values()) {
    const dir = path.join(root, col.dir);
    if (!fs.existsSync(dir)) continue;
    for (const name of fs.readdirSync(dir)) {
      if (IGNORED.has(name)) continue;
      const rel = `${col.dir}/${name}`;
      if (!name.endsWith(".md")) {
        add("error", rel, "(arquivo)", "esperado arquivo .md");
        continue;
      }
      try {
        const parsed = matter(fs.readFileSync(path.join(dir, name), "utf8"));
        records.push({ col, name, rel, data: normalize(parsed.data), body: parsed.content.trim() });
      } catch (e) {
        add("error", rel, "(frontmatter)", `YAML inválido: ${e.reason ?? e.message}`);
      }
    }
  }

  // Índice de slugs (para referências e unicidade).
  const slugs = new Map([...schema.collections.keys()].map((n) => [n, new Set()]));
  for (const r of records) {
    const slug = r.data.slug;
    if (typeof slug !== "string" || !slug) continue;
    if (slugs.get(r.col.name).has(slug)) {
      add("error", r.rel, "slug", `"${slug}" já usado por outro registro de ${r.col.name}`);
    }
    slugs.get(r.col.name).add(slug);
  }

  const ctx = {
    slugs,
    media: schema.media,
    fileExists: (p) => fs.existsSync(path.join(root, p)),
  };

  // 2ª passada: campos, nome de arquivo, regras.
  for (const r of records) {
    const hasBodyField = r.col.fields.some((f) => f.name === "body" && f.type === "rich-text");
    const data = hasBodyField && !("body" in r.data) ? { ...r.data, body: r.body } : r.data;
    for (const e of validateFields(r.col.fields, data, ctx)) add("error", r.rel, e.field, e.message);

    const expected = filenameFor(r.col.filenameTemplate, r.data);
    if (expected && expected !== r.name) {
      add("error", r.rel, "(arquivo)", `nome deve ser "${expected}" (template ${r.col.filenameTemplate})`);
    }
    for (const e of recordRules(r.col.name, r.data)) add(e.level, r.rel, e.field, e.message);
  }

  return { errors, warnings };
}
