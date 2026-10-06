/**
 * Traduz os nomes técnicos do frontmatter para os nomes que aparecem no Pages CMS,
 * lidos do próprio `.pages.yml`, para que quem edita pelo CMS entenda a mensagem.
 * Ver docs/architecture/adr/0007-validacao-conteudo.md e a issue #90.
 */

const PSEUDO = {
  "(arquivo)": "nome do arquivo",
  "(frontmatter)": "cabeçalho do arquivo",
  "(pasta)": "pasta",
};

const label = (f) => f.label ?? f.name;
const optionLabel = (f, value) => {
  const opt = (f.options?.values ?? []).find((v) => (typeof v === "string" ? v : v.name) === value);
  return typeof opt === "object" && opt.label ? opt.label : value;
};

// Procura um campo pelo nome em qualquer nível (objetos e blocos), para os tokens das regras.
function findField(fields, name) {
  for (const f of fields ?? []) {
    if (f.name === name) return f;
    const inner = findField(f.fields, name) ?? (f.blocks ?? []).reduce((acc, b) => acc ?? findField(b.fields, name), null);
    if (inner) return inner;
  }
  return null;
}

/**
 * "contributors[1].person" → "Pessoas autoras / colaboradoras › 2º item › Integrante cadastrado".
 * Para blocos, o tipo do item (blockKey) vem do próprio registro.
 */
export function fieldLabel(fields, path, data) {
  if (PSEUDO[path]) return PSEUDO[path];
  const parts = [];
  let current = fields;
  let value = data;
  let field = null;
  for (const token of path.match(/[^.[\]]+|\[\d+\]/g) ?? []) {
    if (token.startsWith("[")) {
      const i = Number(token.slice(1, -1));
      parts.push(`${i + 1}º item`);
      value = Array.isArray(value) ? value[i] : undefined;
      if (field?.type === "block") {
        const block = field.blocks.find((b) => b.name === value?.[field.blockKey]);
        current = block?.fields ?? [];
      }
      continue;
    }
    field = (current ?? []).find((f) => f.name === token);
    if (!field) return [...parts, token].join(" › ");
    parts.push(label(field));
    value = value?.[token];
    current = field.type === "object" ? field.fields : field.type === "block" ? [] : null;
  }
  return parts.join(" › ");
}

/** «campo:nome» → “Rótulo do campo”; «opção:campo:valor» → “Rótulo da opção”. */
export function resolveTokens(message, fields) {
  return message
    .replace(/«campo:([^»]+)»/g, (_, name) => `“${label(findField(fields, name) ?? { name })}”`)
    .replace(/«opção:([^:»]+):([^»]+)»/g, (_, name, value) => {
      const f = findField(fields, name);
      return `“${f ? optionLabel(f, value) : value}”`;
    });
}

export const recordTitle = (data) => data?.title || data?.name || data?.slug || null;
