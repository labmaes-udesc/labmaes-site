// Sincroniza as labels do repositório com .github/labels.json.
// Uso: node tools/github/sync-labels.mjs   (requer GitHub CLI autenticado)
// Labels com "from" renomeiam a label antiga, preservando as issues já marcadas.
// Labels que existem no GitHub mas não no arquivo são apenas listadas, nunca apagadas.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';

const gh = (...args) => execFileSync('gh', args, { encoding: 'utf8' });
const wanted = JSON.parse(readFileSync(new URL('../../.github/labels.json', import.meta.url), 'utf8'));
const existing = new Set(JSON.parse(gh('label', 'list', '--limit', '200', '--json', 'name')).map((l) => l.name));

for (const { name, from, color, description } of wanted) {
  if (from && existing.has(from) && !existing.has(name)) {
    gh('label', 'edit', from, '--name', name, '--color', color, '--description', description);
    existing.delete(from);
    console.log(`renomeada: ${from} → ${name}`);
  } else {
    gh('label', 'create', name, '--color', color, '--description', description, '--force');
    console.log(`ok: ${name}`);
  }
  existing.delete(name);
}

for (const name of existing) console.log(`fora do arquivo (mantida): ${name}`);
