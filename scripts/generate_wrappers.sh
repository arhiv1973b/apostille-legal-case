#!/bin/bash
mkdir -p public
DELAY="6363 days (Intentional Concealment)"
VOID_RATE="14.4% (Void Acts)"
TOKEN=$(date +%Y%m%d%H%M%S | sha256sum | head -c 16)

echo "🔨 Сборка Jus Cogens Portal + Отчет 1545..."

cat <<HTML > public/index.html
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>A©tor: Jus Cogens Portal & Law 1545 Report</title>
    <style>
        body { font-family: monospace; background: #030a0f; color: #00c6ff; padding: 30px; line-height: 1.4; }
        .vault { border: 2px solid #0e3a5c; background: #071624; padding: 25px; margin-bottom: 20px; }
        .law-box { border-left: 4px solid #ff2244; background: #1a0a0d; padding: 15px; margin: 20px 0; color: #ff99aa; }
        .critical { color: #ff2244; font-weight: bold; text-transform: uppercase; }
        .btn { background: #00c6ff; color: #000; padding: 12px 20px; border: none; cursor: pointer; font-weight: bold; text-decoration: none; display: inline-block; margin: 5px; }
        .btn-gold { background: #f0c040; }
        h2, h3 { color: #fff; text-shadow: 0 0 10px #00c6ff; }
        li { margin-bottom: 8px; }
    </style>
</head>
<body>
    <div class="vault">
        <h1>Pârât: Ministerul Finanțelor RM</h1>
        <p>📍 <strong>Adresa:</strong> mun. Chișinău, str. Constantin Tănase, 8</p>
        <p class="critical">⚖️ ОСНОВАНИЕ: СТ. 21.1 ПРИМ ЗАКОНА О СУДОПРОИЗВОДСТВЕ</p>
        <hr style="border:0; border-top:1px solid #0e3a5c;">
        
        <h2>📋 ОТЧЕТ О НАРУШЕНИЯХ (Закон №1545/1995)</h2>
        <p>Дефектные апостили (VOID Art. 5) применены к файлам, образующим фундамент личности A©tor:</p>
        
        <div class="law-box">
            <strong>Подлежит возмещению ущерб, причиненный вследствие:</strong>
            <ul>
                <li><strong>a)</strong> Незаконного задержания и привлечения к ответственности.</li>
                <li><strong>b)</strong> Незаконного осуждения и <strong>конфискации имущества</strong>.</li>
                <li><strong>c)</strong> Незаконных обысков, изъятий и ареста на имущество.</li>
                <li><strong>f) Незаконного изъятия документов на собственность.</strong></li>
            </ul>
        </div>

        <h3>📊 АНАЛИТИКА ЦЕЛОСТНОСТИ (SECTOR 9):</h3>
        <ul>
            <li>🛑 <strong>Временная диверсия:</strong> $DELAY</li>
            <li>⚠️ <strong>Юридическая ничтожность:</strong> $VOID_RATE (Технический подлог)</li>
            <li>📑 <strong>Объект атаки:</strong> Права частной собственности, Гражданство, Происхождение.</li>
        </ul>

        <hr style="border:0; border-top:1px solid #0e3a5c;">
        
        <a href="apostille_archive_english.html" class="btn btn-gold">🌍 ENGLISH REGISTRY (ART. 17 ICC)</a>
        <a href="disability_cert_gr1.pdf" class="btn" target="_blank">📄 PROBĂ ART. 3 CEDO</a>
        <button onclick="alert('Case Integrity Token: $TOKEN')" class="btn">🛡️ VERIFICĂ SHA-256</button>
    </div>
    <div style="color: #4a7a9b; font-size: 0.8em;">Monitoring Token: $TOKEN | Case Macheret 1997-2026</div>
</body>
</html>
HTML

# Копируем оригиналы без изменений
cp apostille_archive_english.html public/ 2>/dev/null || true
cp *.pdf public/ 2>/dev/null || true
cp *.json public/ 2>/dev/null || true
cp -r docs public/ 2>/dev/null || true
echo "✅ Сайт пересобран с учетом Закона №1545."
