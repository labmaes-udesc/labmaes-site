/**
 * Regras que cruzam campos ou arquivos e não existem no `.pages.yml`.
 * Operam sobre o registro já normalizado (datas como "AAAA-MM-DD").
 * Ver docs/architecture/adr/0007-validacao-conteudo.md.
 */
import { categoriaDe } from "../content-model/categorias-producao.mjs";

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

// Mensagens citam campos e opções por tokens («campo:x», «opção:campo:valor»), que o
// relatório troca pelos nomes que aparecem no CMS (labels.mjs).
const order = (a, b, field, la) =>
  a && b && a > b ? [err(field, `${b} não pode ser anterior a «campo:${la}» (${a})`)] : [];

function productionRules(d) {
  const out = [];
  const isOther = d.productionType === "other";
  if (isOther && !d.otherTypeLabel) {
    out.push(err("otherTypeLabel", "obrigatório quando «campo:productionType» é «opção:productionType:other»"));
  }
  if (!isOther && d.otherTypeLabel) {
    out.push(warn("otherTypeLabel", "preenchido, mas «campo:productionType» não é «opção:productionType:other»; será ignorado"));
  }
  // A macro categoria é derivada do tipo (ADR 0009); um tipo novo precisa entrar na tabela.
  if (d.productionType && !categoriaDe(d.productionType)) {
    out.push(err("productionType", `"${d.productionType}" não tem macro categoria definida (tools/content-model/categorias-producao.mjs)`));
  }
  if (d.date && d.year !== undefined && Number(d.date.slice(0, 4)) !== d.year) {
    out.push(err("year", `${d.year} difere do ano de «campo:date» (${d.date.slice(0, 4)})`));
  }
  const seen = new Map();
  (d.contributors ?? []).forEach((c, i) => {
    if (c?.kind === "internal" && c.person) {
      if (seen.has(c.person)) {
        out.push(err(`contributors[${i}].person`, `"${c.person}" já aparece no ${seen.get(c.person) + 1}º item`));
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
  projects: (d) => order(d.startDate, d.endDate, "endDate", "startDate"),
  people: (d) => [
    ...order(d.membershipStart, d.membershipEnd, "membershipEnd", "membershipStart"),
    ...(d.orcid && !ORCID.test(d.orcid) ? [warn("orcid", `"${d.orcid}" não parece um ORCID (0000-0000-0000-0000)`)] : []),
  ],
  event_editions: (d) => [
    ...order(d.startDate, d.endDate, "endDate", "startDate"),
    ...(d.startDate && d.year !== undefined && Number(d.startDate.slice(0, 4)) !== d.year
      ? [err("year", `${d.year} difere do ano de «campo:startDate» (${d.startDate.slice(0, 4)})`)]
      : []),
  ],
};

export const recordRules = (collection, data) => (RULES[collection]?.(data) ?? []);
