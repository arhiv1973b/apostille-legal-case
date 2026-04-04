#!/bin/bash
# ============================================================
# CLEAN_AND_PUSH.sh — удалить большие файлы из истории + push
# Запуск: bash /mnt/c/Users/arhiv/apostille-legal-case/CLEAN_AND_PUSH.sh
# ============================================================

set -e
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

REPO="/mnt/c/Users/arhiv/apostille-legal-case"
GITHUB_USER="arhiv1973b"
GITHUB_REPO="apostille-legal-case"

echo -e "${CYAN}=== CLEAN_AND_PUSH: удаление больших файлов из истории ===${NC}"
cd "$REPO"

# ── 1. Удалить большие tar.gz из истории git ─────────────────
echo -e "\n${YELLOW}[1/4] Удаление backups/*.tar.gz из git-истории...${NC}"

git filter-repo --force \
  --path "backups/Actor_Backup_20260403_0145.tar.gz" --invert-paths \
  --path "backups/Actor_Backup_20260403_0149.tar.gz" --invert-paths \
  --path "backups/Actor_Backup_20260403_0153.tar.gz" --invert-paths \
  --path "backups/Actor_Backup_20260403_0156.tar.gz" --invert-paths \
  --path "backups/Actor_Backup_20260403_0200.tar.gz" --invert-paths \
  --path "ACTOR_EVIDENCE_BACKUP_2026_03_31.tar.gz" --invert-paths \
  --path "disability_cert_gr1.pdf" --invert-paths \
  2>/dev/null || true

echo -e "  ${GREEN}OK история очищена${NC}"

# ── 2. Восстановить remote (filter-repo его удаляет) ─────────
echo -e "\n${YELLOW}[2/4] Восстановление remote origin...${NC}"
git remote add origin "git@github.com:${GITHUB_USER}/${GITHUB_REPO}.git" 2>/dev/null || \
  git remote set-url origin "git@github.com:${GITHUB_USER}/${GITHUB_REPO}.git"
echo -e "  ${GREEN}OK remote: git@github.com:${GITHUB_USER}/${GITHUB_REPO}.git${NC}"

# ── 3. Добавить .gitignore и закоммитить ─────────────────────
echo -e "\n${YELLOW}[3/4] Commit .gitignore...${NC}"
git add .gitignore 2>/dev/null || true
git add .nojekyll _config.yml SYNC_MASTER.sh 2>/dev/null || true

if ! git diff --cached --quiet; then
  git commit -m "fix: gitignore large files + nojekyll + sync master"
  echo -e "  ${GREEN}OK коммит создан${NC}"
else
  echo -e "  ${YELLOW}  Нет изменений${NC}"
fi

# ── 4. Force push ─────────────────────────────────────────────
echo -e "\n${YELLOW}[4/4] Force push origin master...${NC}"
git push origin master --force \
  && echo -e "  ${GREEN}OK push успешен!${NC}" \
  || echo -e "  ${RED}ERR push не удался${NC}"

echo -e "\n${CYAN}=== ГОТОВО ===${NC}"
git log --oneline -3
echo ""
echo "  Сайт: https://${GITHUB_USER}.github.io/${GITHUB_REPO}/"
echo "  Actions: https://github.com/${GITHUB_USER}/${GITHUB_REPO}/actions"
