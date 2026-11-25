#!/usr/bin/env bash
# Gera uma textura ou imagem de apoio com os parâmetros fixos (spec da Fase 2, seção 3).
# Uso: tools/ds/gerar-imagem.sh <saida.png> <arquivo-de-prompt> [proporcao]
set -euo pipefail

saida="$1"; arquivo_prompt="$2"; proporcao="${3:-1:1}"
script="$HOME/.agents/skills/openrouter-img/scripts/generate_image.py"
fixo="design-systems/marca/ia/prompt-fixo.md"
log="design-systems/marca/ia/log.md"

# Contorno do Avast (intercepta HTTPS) e do bug OPENSSL_Uplink do Python no Windows
unset SSLKEYLOGFILE
if [ -n "${NODE_EXTRA_CA_CERTS:-}" ]; then
  export SSL_CERT_FILE="$NODE_EXTRA_CA_CERTS" REQUESTS_CA_BUNDLE="$NODE_EXTRA_CA_CERTS"
fi

# O prompt final é o bloco "prompt" do arquivo fixo + o prompt específico
prompt="$(tr -d '\r' < "$fixo" | sed -n '/^```prompt$/,/^```$/p' | sed '1d;$d') $(tr -d '\r' < "$arquivo_prompt")"

mkdir -p "$(dirname "$saida")"
status=0
resultado="$(uv run --system-certs "$script" --model pro --resolution 1K --aspect-ratio "$proporcao" \
  --filename "$saida" --prompt "$prompt" 2>&1)" || status=$?
printf '%s\n' "$resultado" | tail -3
if [ "$status" -ne 0 ]; then
  echo "geração falhou (código $status); nada foi registrado no log" >&2
  exit "$status"
fi

custo="$(printf '%s\n' "$resultado" | sed -n 's/.*usage.cost): \(.*\)$/\1/p')"
printf '| %s | `%s` | `%s` | %s | %s |\n' \
  "$(date +%Y-%m-%d)" "$saida" "$arquivo_prompt" "$proporcao" "${custo:-?}" >> "$log"
