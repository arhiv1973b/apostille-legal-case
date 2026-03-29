#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_DIR="AUDIT_LOGS"
LOG_FILE="$LOG_DIR/AI_EXPERT_OPINION_$TIMESTAMP.md"

mkdir -p $LOG_DIR

echo "# AI EXPERT OPINION: CASE-MACHERET-1997-2026" > "$LOG_FILE"
echo "Date: $(date)" >> "$LOG_FILE"
echo "Status: A©tor Forensic Analysis" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"

# Запуск модели и запись диалога
ollama run actor-expert-v2 2>&1 | tee -a "$LOG_FILE"

# Синхронизация с GitHub
echo "📦 Копирование лога в репозиторий..."
cp "$LOG_FILE" ~/legal-sync-work/docs/verification/
cd ~/legal-sync-work
git add docs/verification/*.md
git commit -m "legal: add AI expert forensic opinion $TIMESTAMP"
git push origin master
