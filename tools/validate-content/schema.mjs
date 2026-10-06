import fs from "node:fs";
import yaml from "js-yaml";
import { SUPPORTED_TYPES } from "./fields.mjs";

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

// Confere o schema inteiro, e não só os campos que algum registro preenche:
// um tipo ou opção que o validador não entende precisa falhar já (ADR 0007).
function checkFields(fields, collections, at) {
  for (const f of fields) {
    const here = `${at}.${f.name}`;
    if (!SUPPORTED_TYPES.has(f.type)) {
      throw new Error(`.pages.yml: ${here}: tipo "${f.type}" não suportado pelo validador`);
    }
    if (f.type === "reference") {
      if (!collections.has(f.options?.collection)) {
        throw new Error(`.pages.yml: ${here}: referência para coleção "${f.options?.collection}" inexistente`);
      }
      if (f.options?.value !== "{fields.slug}") {
        throw new Error(`.pages.yml: ${here}: options.value "${f.options?.value}" não suportado (use {fields.slug})`);
      }
    }
    if (f.type === "object") checkFields(f.fields ?? [], collections, here);
    if (f.type === "block") {
      if (!f.blockKey) throw new Error(`.pages.yml: ${here}: bloco sem blockKey`);
      for (const b of f.blocks ?? []) checkFields(b.fields ?? [], collections, `${here}.${b.name}`);
    }
  }
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
      label: c.label ?? c.name,
      dir: c.path,
      filenameTemplate: template,
      fields: expand(c.fields, components),
    });
  }
  for (const c of collections.values()) checkFields(c.fields, collections, c.name);
  const media = (doc.media ?? []).map((m) => ({ output: m.output, input: m.input }));
  return { collections, media };
}

export const loadSchema = (file = ".pages.yml") => parseSchema(fs.readFileSync(file, "utf8"));
