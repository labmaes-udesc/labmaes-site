#!/usr/bin/env node
/**
 * Validador mínimo da nova camada editorial do LabMAES.
 *
 * Fase 1: validações que não exigem parser externo de frontmatter.
 * A validação completa por schema entra após definirmos a biblioteca
 * de frontmatter/validação no ADR correspondente.
 */
import fs from "node:fs";
import path from "node:path";

const ROOT = path.resolve("src/content");
const ALLOWED = new Set([
  "pages", "people", "institutions", "projects", "productions",
  "documents", "collections", "events", "event-editions", "news"
]);

let failed = false;

if (!fs.existsSync(ROOT)) {
  console.error("ERRO: src/content não existe.");
  process.exit(1);
}

for (const entry of fs.readdirSync(ROOT, { withFileTypes: true })) {
  if (entry.isDirectory() && !ALLOWED.has(entry.name)) {
    console.error(`ERRO: coleção inesperada em src/content: ${entry.name}`);
    failed = true;
  }
}

if (failed) process.exit(1);
console.log("Content foundation OK.");
