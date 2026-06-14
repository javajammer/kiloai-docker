#!/usr/bin/env bash
set -euo pipefail

HOME_DIR="${HOME:-/home/kilo}"
mkdir -p \
  "${HOME_DIR}/.config/kilo" \
  "${HOME_DIR}/.local/share/kilo" \
  "${HOME_DIR}/.local/state" \
  "${HOME_DIR}/.local/state/kilo" \
  "${HOME_DIR}/.cache/kilo" \
  "${HOME_DIR}/.nvm" \
  "${HOME_DIR}/.local/share/kilo/sessions" \
  "${HOME_DIR}/.local/share/kilo/logs"

if [ ! -f "${HOME_DIR}/.nvm/kilo.json" ]; then
  cat > "${HOME_DIR}/.nvm/kilo.json" <<'EOF'
{
  "$schema": "https://app.kilo.ai/config.json",
  "skills": {
    "paths": [
      ".kilo/skills"
    ]
  }
}
EOF
fi

if [ ! -f "${HOME_DIR}/.config/kilo/opencode.json" ]; then
  cat > "${HOME_DIR}/.config/kilo/opencode.json" <<'EOF'
{
  "$schema": "https://kilo.ai/config.json",
  "model": "kilo/kilo-auto/free",
  "small_model": "kilo/kilo-auto/free",
  "theme": "catppuccin",
  "autoupdate": true,
  "share": "manual",
  "snapshot": true,
  "logLevel": "INFO",
  "provider": {}
}
EOF
fi

if [ ! -f "${HOME_DIR}/.local/share/kilo/auth.json" ]; then
  printf '%s\n' '{}' > "${HOME_DIR}/.local/share/kilo/auth.json"
fi

if [ ! -f "${HOME_DIR}/.local/share/kilo/mcp-auth.json" ]; then
  printf '%s\n' '{}' > "${HOME_DIR}/.local/share/kilo/mcp-auth.json"
fi

if [ ! -f "${HOME_DIR}/.local/share/kilo/telemetry-id" ]; then
  printf '%s\n' 'local-only' > "${HOME_DIR}/.local/share/kilo/telemetry-id"
fi

if [ $# -eq 0 ]; then
  set -- kilo
fi

if [ "${1#-}" != "${1}" ]; then
  set -- kilo "$@"
fi

exec "$@"
