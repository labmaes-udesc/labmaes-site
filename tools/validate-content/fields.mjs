/**
 * Checagens por campo, derivadas da definição de campos do `.pages.yml`.
 * Ver docs/architecture/adr/0007-validacao-conteudo.md.
 *
 * `ctx`: { slugs: Map<coleção, Set<slug>>, media: [{output, input}], fileExists(path) }
 */

const isEmpty = (v) =>
  v === undefined || v === null || v === "" || (Array.isArray(v) && v.length === 0);
const isObject = (v) => v !== null && typeof v === "object" && !Array.isArray(v) && !(v instanceof Date);

export function normalizeDate(v) {
  const iso = v instanceof Date ? v.toISOString().slice(0, 10) : v;
  if (typeof iso !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(iso)) return null;
  const d = new Date(`${iso}T00:00:00Z`);
  return Number.isNaN(d.getTime()) || d.toISOString().slice(0, 10) !== iso ? null : iso;
}

const optionNames = (f) => (f.options?.values ?? []).map((v) => (typeof v === "string" ? v : v.name));

const error = (field, message) => ({ field, message });

function validateScalar(f, v, ctx, at) {
  switch (f.type) {
    case "string":
    case "text":
    case "rich-text": {
      if (typeof v !== "string") return [error(at, "deve ser texto")];
      const rx = typeof f.pattern === "string" ? f.pattern : f.pattern?.regex;
      if (rx && !new RegExp(rx).test(v)) {
        return [error(at, f.pattern?.message ?? `não casa com o padrão ${rx}`)];
      }
      return [];
    }
    case "number":
      return typeof v === "number" && Number.isFinite(v) ? [] : [error(at, "deve ser número")];
    case "boolean":
      return typeof v === "boolean" ? [] : [error(at, "deve ser verdadeiro ou falso")];
    case "date":
      return normalizeDate(v) ? [] : [error(at, "deve ser uma data válida no formato AAAA-MM-DD")];
    case "select": {
      const names = optionNames(f);
      return names.includes(v)
        ? []
        : [error(at, `valor "${v}" inválido; opções: ${names.join(", ")}`)];
    }
    case "image":
    case "file": {
      if (typeof v !== "string") return [error(at, "deve ser caminho de arquivo (texto)")];
      const m = ctx.media.find((x) => v.startsWith(`${x.output}/`));
      if (!m) {
        return [error(at, `"${v}" não está em uma pasta de mídia conhecida (${ctx.media.map((x) => x.output).join(", ")})`)];
      }
      const disk = `${m.input}/${v.slice(m.output.length + 1)}`;
      return ctx.fileExists(disk) ? [] : [error(at, `arquivo "${v}" não existe em ${disk}`)];
    }
    case "reference": {
      const target = f.options?.collection;
      if (!ctx.slugs.has(target)) return [error(at, `schema: coleção "${target}" não existe`)];
      if (f.options?.value !== "{fields.slug}") {
        return [error(at, `schema: options.value "${f.options?.value}" não suportado (use {fields.slug})`)];
      }
      if (typeof v !== "string") return [error(at, "deve ser um slug (texto)")];
      return ctx.slugs.get(target).has(v)
        ? []
        : [error(at, `referência "${v}" não existe na coleção ${target}`)];
    }
    case "object":
      if (!isObject(v)) return [error(at, "deve ser um objeto")];
      return validateFields(f.fields ?? [], v, ctx, `${at}.`);
    case "block": {
      if (!isObject(v)) return [error(at, "deve ser um objeto")];
      const key = f.blockKey;
      const block = f.blocks.find((b) => b.name === v[key]);
      if (!block) {
        return [error(`${at}.${key}`, `tipo "${v[key] ?? ""}" inválido; opções: ${f.blocks.map((b) => b.name).join(", ")}`)];
      }
      return validateFields(block.fields ?? [], v, ctx, `${at}.`, [key]);
    }
    default:
      return [error(at, `schema: tipo "${f.type}" não suportado pelo validador`)];
  }
}

function validateValue(f, v, ctx, at) {
  const multiple = f.list === true || (f.type === "reference" && f.options?.multiple === true);
  if (!multiple) return validateScalar(f, v, ctx, at);
  if (!Array.isArray(v)) return [error(at, "deve ser uma lista")];
  return v.flatMap((item, i) =>
    isEmpty(item) ? [error(`${at}[${i}]`, "item vazio")] : validateScalar(f, item, ctx, `${at}[${i}]`),
  );
}

export function validateFields(fields, data, ctx, at = "", extraKnown = []) {
  const errors = [];
  const known = new Set([...fields.map((f) => f.name), ...extraKnown]);
  for (const k of Object.keys(data)) {
    if (!known.has(k)) errors.push(error(`${at}${k}`, "campo não existe no schema (.pages.yml)"));
  }
  for (const f of fields) {
    const v = data[f.name];
    if (isEmpty(v)) {
      if (f.required) errors.push(error(`${at}${f.name}`, "obrigatório"));
      continue;
    }
    errors.push(...validateValue(f, v, ctx, `${at}${f.name}`));
  }
  return errors;
}
