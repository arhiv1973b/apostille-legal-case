#!/bin/bash
# ============================================================
# SYNC_MASTER.sh — WSL/Bash синхронизация
# JUS COGENS SITE | Case Macheret 1997-2026
# Запуск: bash /mnt/c/Users/arhiv/apostille-legal-case/SYNC_MASTER.sh
# ============================================================

set -e
CYAN='\033[0;36m'; GREEN='\033[0;32m'; RED='\033[0;31m'
YELLOW='\033[1;33m'; BOLD='\033[1m'; NC='\033[0m'

REPO="/mnt/c/Users/arhiv/apostille-legal-case"
GITHUB_USER="arhiv1973b"
GITHUB_REPO="apostille-legal-case"
NOREPLY_EMAIL="${GITHUB_USER}@users.noreply.github.com"

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  SYNC_MASTER — WSL + Docker + GitHub Pages                  ║"
echo "║  Case Macheret | JUS COGENS | 2026-04-04                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

cd "$REPO" || { echo -e "${RED}[ERR] Папка не найдена: $REPO${NC}"; exit 1; }

# ── 1. Git глобальная настройка ───────────────────────────────────
echo -e "${YELLOW}[1/6] Git config (глобально)...${NC}"
git config --global user.email "$NOREPLY_EMAIL"
git config --global user.name "$GITHUB_USER"
git config --global core.autocrlf input
git config --global push.default current
git config --global pull.rebase true
git config advice.skippedCherryPicks false 2>/dev/null || true
echo -e "  ${GREEN}OK email: $NOREPLY_EMAIL${NC}"
echo -e "  ${GREEN}OK autocrlf: input (LF — WSL)${NC}"

# ── 2. GitHub Pages через gh CLI API (без браузера) ───────────────
echo -e "\n${YELLOW}[2/6] GitHub Pages → GitHub Actions (через API)...${NC}"

if command -v gh &>/dev/null; then
  echo -e "  ${GREEN}OK gh CLI: $(gh --version | head -1)${NC}"
  gh api \
    --method PUT \
    -H "Accept: application/vnd.github+json" \
    "/repos/${GITHUB_USER}/${GITHUB_REPO}/pages" \
    -f "build_type=workflow" \
    2>/dev/null \
    && echo -e "  ${GREEN}OK Pages source = GitHub Actions${NC}" \
    || echo -e "  ${YELLOW}WARN: Уже настроено или нужен: gh auth login --git-protocol ssh${NC}"
else
  echo -e "  ${YELLOW}WARN gh CLI не найден. Устанавливаю...${NC}"
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
    | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg 2>/dev/null
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
  sudo apt update -qq && sudo apt install gh -y -qq
  echo -e "  ${GREEN}OK gh CLI установлен.${NC}"
  echo -e "  ${CYAN}  Авторизуйтесь: gh auth login --git-protocol ssh${NC}"
  echo -e "  ${YELLOW}  Затем перезапустите скрипт.${NC}"
  exit 0
fi

# ── 3. .nojekyll + _config.yml ────────────────────────────────────
echo -e "\n${YELLOW}[3/6] .nojekyll + _config.yml (чистый HTML деплой)...${NC}"

touch .nojekyll
echo -e "  ${GREEN}OK .nojekyll создан${NC}"

cat > _config.yml << 'YMLEOF'
title: "A©tor Maceret: Jus Cogens Portal"
description: "Legal evidence - Case Macheret 1997-2026"
baseurl: "/apostille-legal-case"
url: "https://arhiv1973b.github.io"
exclude:
  - "*.sh"
  - "*.bat"
  - "*.ps1"
  - "*.py"
  - "*.tar.gz"
  - "*.tar"
  - "backups/"
  - "AUDIT_LOGS/"
YMLEOF
echo -e "  ${GREEN}OK _config.yml создан${NC}"

# ── 4. Docker + SSH ───────────────────────────────────────────────
echo -e "\n${YELLOW}[4/6] Docker статус + SSH ключ WSL...${NC}"

if command -v docker &>/dev/null; then
  echo -e "  ${GREEN}OK $(docker --version)${NC}"
  if docker info &>/dev/null 2>&1; then
    echo -e "  ${GREEN}OK Docker daemon запущен${NC}"
    docker image inspect "ghcr.io/${GITHUB_USER}/maceret-case-evidence:latest" &>/dev/null \
      && echo -e "  ${GREEN}OK Образ найден локально${NC}" \
      || echo -e "  ${YELLOW}INFO Образ не найден локально (pull при необходимости)${NC}"
  else
    echo -e "  ${YELLOW}WARN Docker daemon не запущен — запустите Docker Desktop${NC}"
  fi
else
  echo -e "  ${YELLOW}WARN Docker не в PATH WSL${NC}"
  echo -e "  Добавьте в ~/.bashrc:"
  echo -e "  export PATH=\$PATH:/mnt/c/Program\ Files/Docker/resources/bin"
fi

# SSH: Windows ключ → WSL
WIN_KEY="/mnt/c/Users/arhiv/.ssh/id_rsa"
WSL_KEY="$HOME/.ssh/id_rsa"
if [ -f "$WSL_KEY" ]; then
  echo -e "  ${GREEN}OK SSH ключ WSL: $WSL_KEY${NC}"
elif [ -f "$WIN_KEY" ]; then
  mkdir -p ~/.ssh && chmod 700 ~/.ssh
  cp "$WIN_KEY" "$WSL_KEY" && chmod 600 "$WSL_KEY"
  [ -f "${WIN_KEY}.pub" ] && cp "${WIN_KEY}.pub" "${WSL_KEY}.pub" && chmod 644 "${WSL_KEY}.pub" || true
  echo -e "  ${GREEN}OK SSH ключ скопирован Windows -> WSL${NC}"
else
  echo -e "  ${YELLOW}WARN SSH ключ не найден. Создайте:${NC}"
  echo -e "  ssh-keygen -t ed25519 -f ~/.ssh/id_rsa -C 'case@jus-cogens'"
fi

# Тест SSH GitHub
SSH_TEST=$(ssh -o StrictHostKeyChecking=no -T git@github.com 2>&1 || true)
echo "$SSH_TEST" | grep -q "successfully" \
  && echo -e "  ${GREEN}OK SSH -> GitHub: аутентификация успешна${NC}" \
  || echo -e "  ${YELLOW}INFO SSH test: $SSH_TEST${NC}"

# ── 5. Git remote check + commit + push ───────────────────────────
echo -e "\n${YELLOW}[5/6] Git remote + commit + push...${NC}"

REMOTE=$(git remote get-url origin 2>/dev/null || echo "none")
if [[ "$REMOTE" == *"https://"* ]]; then
  git remote set-url origin "git@github.com:${GITHUB_USER}/${GITHUB_REPO}.git"
  echo -e "  ${GREEN}OK Remote переключён на SSH${NC}"
else
  echo -e "  ${GREEN}OK Remote SSH: $REMOTE${NC}"
fi

git add .nojekyll _config.yml 2>/dev/null || true
git add .github/workflows/deploy.yml 2>/dev/null || true
git add SYNC_MASTER.sh 2>/dev/null || true

if ! git diff --cached --quiet; then
  git commit -m "sync: WSL master sync nojekyll+config+pages [$(date '+%Y-%m-%d %H:%M')]"
  echo -e "  ${GREEN}OK Коммит создан${NC}"
else
  echo -e "  ${YELLOW}INFO Нет новых изменений для коммита${NC}"
fi

git pull origin master --rebase --autostash 2>/dev/null || true

if git push origin HEAD; then
  echo -e "  ${GREEN}OK Push успешен!${NC}"
else
  echo -e "  ${RED}ERR Push не удался.${NC}"
  echo -e "  Проверьте ключ на: https://github.com/settings/keys"
fi

# ── 6. Финальный статус ───────────────────────────────────────────
echo -e "\n${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}[OK] СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "  Git log (3):"
git log --oneline -3
echo ""
echo "  Actions:  https://github.com/${GITHUB_USER}/${GITHUB_REPO}/actions"
echo "  Сайт:     https://${GITHUB_USER}.github.io/${GITHUB_REPO}/"
echo ""
echo "  --- Следующий push из WSL ---"
echo "  cd $REPO && git add -A && git commit -m 'update' && git push origin HEAD"
echo ""
echo "  --- Следующий push из PowerShell ---"
echo "  cd C:\Users\arhiv\apostille-legal-case"
echo "  git add -A && git commit -m 'update' && git push origin HEAD"
