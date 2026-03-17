#!/bin/bash
set -e
REPO=$(pwd)
info() { echo -e "\033[0;36m[→]\033[0m $1"; }
log() { echo -e "\033[0;32m[✓]\033[0m $1"; }
info "Синхронизация в: $REPO"
git add .
git commit -m "fix(legal-logic): repair jus cogens evidence integrity & dynamic paths" || echo "Изменений нет"
git push origin master
log "ДЕПЛОЙ ЗАВЕРШЕН"
