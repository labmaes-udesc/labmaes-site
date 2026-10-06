import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import { loadSchema } from "./schema.mjs";
import { validateFields, normalizeDate } from "./fields.mjs";
import { recordRules, filenameFor } from "./rules.mjs";
import { fieldLabel, resolveTokens, recordTitle } from "./labels.mjs";

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
  // Cada problema guarda o caminho técnico (file, field) e a versão com os nomes do CMS
  // (collection, record, fieldLabel, message), usada no relatório (issue #90).
  const add = (level, file, field, message, rec) => {
    const fields = rec?.col.fields ?? [];
    (level === "error" ? errors : warnings).push({
      file,
      field,
      message: resolveTokens(message, fields),
      collection: rec?.col.label ?? null,
      record: rec ? recordTitle(rec.data) : null,
      fieldLabel: fieldLabel(fields, field, rec?.data ?? {}),
    });
  };
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
        add("error", rel, "(arquivo)", "esperado arquivo .md", { col, data: {} });
        continue;
      }
      try {
        const parsed = matter(fs.readFileSync(path.join(dir, name), "utf8"));
        records.push({ col, name, rel, data: normalize(parsed.data), body: parsed.content.trim() });
      } catch (e) {
        add("error", rel, "(frontmatter)", `YAML inválido: ${e.reason ?? e.message}`, { col, data: {} });
      }
    }
  }

  // Índice de slugs (para referências e unicidade).
  const slugs = new Map([...schema.collections.keys()].map((n) => [n, new Set()]));
  for (const r of records) {
    const slug = r.data.slug;
    if (typeof slug !== "string" || !slug) continue;
    if (slugs.get(r.col.name).has(slug)) {
      add("error", r.rel, "slug", `"${slug}" já é usado por outro registro de ${r.col.label}`, r);
    }
    slugs.get(r.col.name).add(slug);
  }

  const ctx = {
    slugs,
    collectionLabels: new Map([...schema.collections.values()].map((c) => [c.name, c.label])),
    media: schema.media,
    fileExists: (p) => fs.existsSync(path.join(root, p)),
  };

  // 2ª passada: campos, nome de arquivo, regras.
  for (const r of records) {
    const hasBodyField = r.col.fields.some((f) => f.name === "body" && f.type === "rich-text");
    const data = hasBodyField && !("body" in r.data) ? { ...r.data, body: r.body } : r.data;
    for (const e of validateFields(r.col.fields, data, ctx)) add("error", r.rel, e.field, e.message, r);

    const expected = filenameFor(r.col.filenameTemplate, r.data);
    if (expected && expected !== r.name) {
      add("error", r.rel, "(arquivo)", `deveria ser "${expected}" (montado a partir de ${r.col.filenameTemplate}); o CMS não renomeia arquivos, peça a quem administra o site`, r);
    }
    for (const e of recordRules(r.col.name, r.data)) add(e.level, r.rel, e.field, e.message, r);
  }

  return { errors, warnings };
}
