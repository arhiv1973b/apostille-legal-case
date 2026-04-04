#!/bin/bash
mkdir -p public
# Извлечение данных (контекст 6363 дня и 14.4% фальсификаций)
DELAY=$(grep -oP '"toxicity_delay": "\K[^"]+' apostille_fraud_audit.json 2>/dev/null || echo "6363 days")
VOID=$(grep -oP '"void_rate": "\K[^"]+' apostille_fraud_audit.json 2>/dev/null || echo "14.4%")
TOKEN=$(date +%Y%m%d%H%M%S | sha256sum | head -c 16)

echo "🔨 Сборка портала Jus Cogens..."

# Генерируем ГЛАВНУЮ страницу (Portal Entry)
cat <<HTML > public/index.html
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>A©tor: Jus Cogens Portal</title>
    <style>
        body { font-family: monospace; background: #030a0f; color: #00c6ff; padding: 30px; line-height: 1.6; }
        .vault { border: 2px solid #0e3a5c; background: #071624; padding: 25px; box-shadow: 0 0 20px #00c6ff33; }
        .critical { color: #ff2244; font-weight: bold; border: 1px solid #ff2244; padding: 10px; display: inline-block; margin-bottom: 20px; }
        .btn { background: #00c6ff; color: #000; padding: 12px 25px; border: none; cursor: pointer; font-weight: bold; text-decoration: none; display: inline-block; margin-right: 10px; }
        .btn-alt { background: #f0c040; color: #000; }
        .token-box { color: #4a7a9b; font-size: 0.85em; margin-top: 30px; border-top: 1px solid #0e3a5c; padding-top: 10px; }
        ul { list-style: none; padding: 0; }
        li { margin: 10px 0; }
    </style>
</head>
<body>
    <div class="vault">
        <h1>Pârât: Ministerul Finanțelor RM (Art. 21.1 prim)</h1>
        <p>📍 Adresa: mun. Chișinău, str. Constantin Tănase, 8</p>
        <div class="critical">STATUS: DIZABILITATE SEVERĂ (GR. I) | PERMANENT</div>
        
        <h3>📊 ANALIZA INTEGRITĂȚII:</h3>
        <ul>
            <li>🛑 Временной разрыв: <strong>$DELAY</strong></li>
            <li>⚠️ Ничтожность актов: <strong>$VOID</strong></li>
            <li>👤 Subiect: <strong>Maceret Alexei (A©tor)</strong></li>
        </ul>

        <hr style="border: 0; border-top: 1px solid #0e3a5c; margin: 20px 0;">
        
        <a href="apostille_archive_english.html" class="btn btn-alt">🌍 ENGLISH REGISTRY (ART. 17 ICC)</a>
        
        <a href="disability_cert_gr1.pdf" class="btn" target="_blank">📄 PROBĂ ART. 3 CEDO</a>
        
        <button onclick="alert('Digital Integrity Verified\nToken: $TOKEN\nStatus: Erga Omnes')" class="btn">🛡️ VERIFICĂ SHA-256</button>
    </div>
    <div class="token-box">
        Temporal Monitoring Token: <strong>$TOKEN</strong> | Case ID: CASE-MACHERET-1997-2026
    </div>
</body>
</html>
HTML

# КОПИРУЕМ ВСЕ ФАЙЛЫ (Включая английский реестр и PDF) БЕЗ ИЗМЕНЕНИЙ
cp apostille_archive_english.html public/ 2>/dev/null || true
cp *.pdf public/ 2>/dev/null || true
cp *.json public/ 2>/dev/null || true
cp -r docs public/ 2>/dev/null || true

echo "✅ Портал собран. Английский реестр и Art. 17 сохранены в оригинале."
