/**
 * Regras que cruzam campos ou arquivos e não existem no `.pages.yml`.
 * Operam sobre o registro já normalizado (datas como "AAAA-MM-DD").
 * Ver docs/architecture/adr/0007-validacao-conteudo.md.
 */
const ORCID = /^(https:\/\/orcid\.org\/)?\d{4}-\d{4}-\d{4}-\d{3}[\dX]$/;
const err = (field, message) => ({ level: "error", field, message });
const warn = (field, message) => ({ level: "warning", field, message });

export function filenameFor(template, data) {
  let missing = false;
  const name = template.replace(/\{fields\.([^}]+)\}/g, (_, k) => {
    if (data[k] === undefined || data[k] === null || data[k] === "") missing = true;
    return String(data[k]);
  });
  return missing ? null : name;
}

const order = (a, b, field, la, lb) =>
  a && b && a > b ? [err(field, `${lb} (${b}) não pode ser anterior a ${la} (${a})`)] : [];

function productionRules(d) {
  const out = [];
  const isOther = d.productionType === "other" || d.productionCategory === "other";
  if (isOther && !d.otherTypeLabel) {
    out.push(err("otherTypeLabel", "obrigatório quando a categoria ou o tipo é \"other\""));
  }
  if (!isOther && d.otherTypeLabel) {
    out.push(warn("otherTypeLabel", "preenchido, mas nem a categoria nem o tipo é \"other\"; será ignorado"));
  }
  if (d.date && d.year !== undefined && Number(d.date.slice(0, 4)) !== d.year) {
    out.push(err("year", `ano ${d.year} difere do ano da data (${d.date.slice(0, 4)})`));
  }
  const seen = new Map();
  (d.contributors ?? []).forEach((c, i) => {
    if (c?.kind === "internal" && c.person) {
      if (seen.has(c.person)) {
        out.push(err(`contributors[${i}].person`, `"${c.person}" já consta em contributors[${seen.get(c.person)}]`));
      } else seen.set(c.person, i);
    }
    if (c?.orcid && !ORCID.test(c.orcid)) {
      out.push(warn(`contributors[${i}].orcid`, `"${c.orcid}" não parece um ORCID (0000-0000-0000-0000)`));
    }
  });
  return out;
}

const RULES = {
  productions: productionRules,
  projects: (d) => order(d.startDate, d.endDate, "endDate", "startDate", "endDate"),
  people: (d) => [
    ...order(d.membershipStart, d.membershipEnd, "membershipEnd", "membershipStart", "membershipEnd"),
    ...(d.orcid && !ORCID.test(d.orcid) ? [warn("orcid", `"${d.orcid}" não parece um ORCID (0000-0000-0000-0000)`)] : []),
  ],
  event_editions: (d) => [
    ...order(d.startDate, d.endDate, "endDate", "startDate", "endDate"),
    ...(d.startDate && d.year !== undefined && Number(d.startDate.slice(0, 4)) !== d.year
      ? [err("year", `ano ${d.year} difere do ano de startDate (${d.startDate.slice(0, 4)})`)]
      : []),
  ],
};

export const recordRules = (collection, data) => (RULES[collection]?.(data) ?? []);
