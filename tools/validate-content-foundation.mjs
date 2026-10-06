#!/usr/bin/env node
/**
 * Validador do conteúdo editorial (src/content), derivado do .pages.yml.
 * Ver docs/architecture/adr/0007-validacao-conteudo.md.
 *
 * O relatório usa os nomes que aparecem no Pages CMS (coleção, título do registro, campo),
 * porque quem recebe o aviso de falha da CI é, em geral, quem editou pelo CMS (ADR 0008).
 */
import fs from "node:fs";
import { runValidation } from "./validate-content/run.mjs";

let result;
try {
  result = runValidation();
} catch (e) {
  console.error(`ERRO: ${e.message}`);
  process.exit(1);
}

const items = [
  ...result.errors.map((p) => ({ ...p, level: "error" })),
  ...result.warnings.map((p) => ({ ...p, level: "warning" })),
];

// Agrupa por arquivo, para listar todos os problemas de um registro juntos.
const byFile = new Map();
for (const p of items) byFile.set(p.file, [...(byFile.get(p.file) ?? []), p]);

const where = (p) =>
  p.collection ? `${p.collection} › ${p.record ? `“${p.record}”` : p.file}` : p.file;

for (const [file, problems] of byFile) {
  const out = problems.some((p) => p.level === "error") ? console.error : console.warn;
  out(`\n${problems.some((p) => p.level === "error") ? "ERRO" : "AVISO"} · ${where(problems[0])}`);
  for (const p of problems) {
    out(`  ${p.level === "error" ? "✗" : "!"} ${p.fieldLabel}: ${p.message}`);
  }
  out(`    arquivo: ${file} · campos técnicos: ${problems.map((p) => p.field).join(", ")}`);
}

// Na CI do GitHub: anotações no arquivo e um resumo legível na página da execução.
if (process.env.GITHUB_ACTIONS === "true") {
  const esc = (s) => String(s).replace(/%/g, "%25").replace(/\r/g, "%0D").replace(/\n/g, "%0A");
  for (const p of items) {
    const kind = p.level === "error" ? "error" : "warning";
    console.log(`::${kind} file=${esc(p.file)},title=${esc(where(p))}::${esc(`${p.fieldLabel}: ${p.message}`)}`);
  }
  if (process.env.GITHUB_STEP_SUMMARY && items.length) {
    const linhas = [
      "## Conteúdo do site: problemas encontrados",
      "",
      "Corrija pelo Pages CMS: abra o registro indicado e ajuste o campo. A verificação roda de novo a cada salvamento.",
      "",
      "| | Registro | Campo | O que corrigir |",
      "| --- | --- | --- | --- |",
      ...items.map((p) =>
        `| ${p.level === "error" ? "Erro" : "Aviso"} | ${where(p)} | ${p.fieldLabel} | ${p.message.replace(/\|/g, "\\|")} |`,
      ),
    ];
    fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, `${linhas.join("\n")}\n`);
  }
}

if (result.errors.length) {
  console.error(`\n${result.errors.length} erro(s), ${result.warnings.length} aviso(s).`);
  process.exit(1);
}
console.log(`Conteúdo OK (${result.warnings.length} aviso(s)).`);
