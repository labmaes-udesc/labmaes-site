#!/usr/bin/env node
/**
 * Validador do conteúdo editorial (src/content), derivado do .pages.yml.
 * Ver docs/architecture/adr/0007-validacao-conteudo.md.
 */
import { runValidation } from "./validate-content/run.mjs";

let result;
try {
  result = runValidation();
} catch (e) {
  console.error(`ERRO: ${e.message}`);
  process.exit(1);
}

const line = ({ file, field, message }) => `  ${file} › ${field}: ${message}`;
for (const w of result.warnings) console.warn(`AVISO${line(w).slice(1)}`);
for (const e of result.errors) console.error(`ERRO${line(e).slice(1)}`);

if (result.errors.length) {
  console.error(`\n${result.errors.length} erro(s), ${result.warnings.length} aviso(s).`);
  process.exit(1);
}
console.log(`Conteúdo OK (${result.warnings.length} aviso(s)).`);
