import fs from "node:fs";
import yaml from "js-yaml";

function expand(fields, components) {
  return (fields ?? []).map((f) => {
    if (f.component) {
      const base = components[f.component];
      if (!base) throw new Error(`.pages.yml: componente "${f.component}" não existe (campo "${f.name}")`);
      const { component, ...own } = f;
      f = { ...base, ...own };
    }
    const out = { ...f };
    if (f.fields) out.fields = expand(f.fields, components);
    if (f.blocks) out.blocks = f.blocks.map((b) => ({ ...b, fields: expand(b.fields, components) }));
    return out;
  });
}

function flatten(items) {
  return items.flatMap((i) => (i.type === "group" ? flatten(i.items ?? []) : [i]));
}

export function parseSchema(text) {
  const doc = yaml.load(text);
  const components = doc.components ?? {};
  const collections = new Map();
  for (const c of flatten(doc.content ?? []).filter((i) => i.type === "collection")) {
    const template = c.filename?.template;
    if (!template) throw new Error(`.pages.yml: coleção "${c.name}" sem filename.template`);
    collections.set(c.name, {
      name: c.name,
      dir: c.path,
      filenameTemplate: template,
      fields: expand(c.fields, components),
    });
  }
  const media = (doc.media ?? []).map((m) => ({ output: m.output, input: m.input }));
  return { collections, media };
}

export const loadSchema = (file = ".pages.yml") => parseSchema(fs.readFileSync(file, "utf8"));
