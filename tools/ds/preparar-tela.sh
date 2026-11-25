#!/usr/bin/env bash
# Cria ou atualiza a pasta de uma tela-chave (plan v2 da Fase 2, Tarefa A4).
# Uso: tools/ds/preparar-tela.sh <slug>     ex.: tools/ds/preparar-tela.sh 01-home
# Copia o kit da design-taste-frontend (assets/), a camada de marca, as fontes e as texturas
# aprovadas. Nunca sobrescreve o index.html de uma tela que já existe.
set -euo pipefail

slug="${1:?uso: tools/ds/preparar-tela.sh <slug>}"
skill="${SKILL:-$HOME/.claude/skills/design-taste-frontend}"
tela="design-systems/telas/$slug"

[ -f "$skill/assets/starter.html" ] || { echo "kit da skill não encontrado em $skill" >&2; exit 1; }
mkdir -p "$tela/marca/fonts" "$tela/marca/textura"

rm -rf "$tela/assets"
cp -r "$skill/assets" "$tela/assets"

cp design-systems/marca/marca.css "$tela/marca/marca.css"
cp assets/fonts/Poppins-*.woff2 assets/fonts/Thunder-BoldHC.woff2 "$tela/marca/fonts/"
if compgen -G "design-systems/marca/textura/*" > /dev/null; then
  cp design-systems/marca/textura/* "$tela/marca/textura/"
fi

if [ ! -f "$tela/index.html" ]; then
  cp "$skill/assets/starter.html" "$tela/index.html"
  echo "index.html criado a partir do starter da skill"
fi
grep -q 'marca/marca.css' "$tela/index.html" \
  || echo "LEMBRETE: ligar <link rel=\"stylesheet\" href=\"marca/marca.css\"> depois de assets/system.css em $tela/index.html"
echo "tela $slug pronta em $tela"
