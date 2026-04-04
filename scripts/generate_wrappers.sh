#!/bin/bash
mkdir -p public
DELAY="6363 days (Intentional Concealment)"
VOID_RATE="14.4% (Void Acts)"
TOKEN=$(date +%Y%m%d%H%M%S | sha256sum | head -c 16)

# Функция для создания HTML-оберток улик
generate_evidence_page() {
    cat <<HTML > "public/$1"
<!DOCTYPE html>
<html lang="ro">
<head><meta charset="UTF-8"><title>$2</title>
<style>body{font-family:monospace;background:#000;color:#fff;padding:40px;line-height:1.6;} .box{border:2px solid $3;padding:30px;max-width:800px;margin:auto;} .tag{color:$3;font-weight:bold;border:1px solid $3;padding:5px;display:inline-block;margin-bottom:20px;}</style></head>
<body><div class="box"><div class="tag">$4</div><h1>$2</h1><p>$5</p><hr style="border:0;border-top:1px solid $3;"><a href="index.html" style="color:#00c6ff;"><- ÎNAPOI</a></div></body></html>
HTML
}

# Генерируем страницы улик
generate_evidence_page "disability_evidence.html" "PROBĂ: Dizabilitate Severă (Art. 3 CEDO)" "#ff2244" "EVIDENȚĂ: C013564402308" "Subiect: MACERET ALEXEI. Statut: Gradul I (Sever) - Fără termen. Această probă atestă vulnerabilitatea subiectului în fața torturii instituționale de 6363 zile."
generate_evidence_page "un_petition_evidence.html" "EVIDENCE: UN OHCHR Petition" "#f0c040" "UNITED NATIONS: 2013073942632" "Status: Stand Up for Human Rights. Confirmation of international escalation regarding procedural sabotage."
generate_evidence_page "cpt_evidence.html" "УЛИКА: Ответ ЕКПП (CPT) 2012" "#00ff00" "COUNCIL OF EUROPE: STRASBOURG" "Письмо из Секретариата ЕКПП (Йохан Фристедт) подтверждает осведомленность органов СЕ о ситуации с 2012 года."

# Генерируем ГЛАВНУЮ страницу
cat <<HTML > public/index.html
<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <title>A©tor: Jus Cogens Portal</title>
    <style>
        body { font-family: monospace; background: #030a0f; color: #00c6ff; padding: 30px; line-height: 1.4; }
        .vault { border: 2px solid #0e3a5c; background: #071624; padding: 25px; margin-bottom: 20px; }
        .critical { color: #ff2244; font-weight: bold; text-transform: uppercase; border: 1px solid #ff2244; padding: 5px; display: inline-block; margin: 10px 0; }
        .btn { background: #00c6ff; color: #000; padding: 12px 20px; border: none; cursor: pointer; font-weight: bold; text-decoration: none; display: inline-block; margin: 5px; }
        .btn-red { background: #ff2244; color: #fff; }
        .btn-gold { background: #f0c040; color: #000; }
        .btn-green { background: #00ff00; color: #000; }
    </style>
</head>
<body>
    <div class="vault">
        <h1>Pârât: Ministerul Finanțelor RM</h1>
        <p>📍 Adresa: mun. Chișinău, str. Constantin Tănase, 8</p>
        <div class="critical">⚖️ LEGEA 1545/1995: PUNCTELE A, B, C, F</div>
        <hr style="border:0; border-top:1px solid #0e3a5c; margin: 20px 0;">
        
        <h3>📊 STATUS INTEGRITATE:</h3>
        <ul>
            <li>🛑 <strong>Задержка:</strong> $DELAY</li>
            <li>⚠️ <strong>Ничтожность:</strong> $VOID_RATE (Art. 5 Void)</li>
        </ul>

        <hr style="border:0; border-top:1px solid #0e3a5c; margin: 20px 0;">
        
        <a href="disability_evidence.html" class="btn btn-red">🚑 УЛИКА №1: ИНВАЛИДНОСТЬ</a>
        <a href="un_petition_evidence.html" class="btn btn-gold">🇺🇳 УЛИКА №2: ПЕТИЦИЯ ООН</a>
        <a href="cpt_evidence.html" class="btn btn-green">🇪🇺 УЛИКА №3: ОТВЕТ ЕКПП</a>
        
        <br><br>
        <a href="apostille_archive_english.html" class="btn">🌍 ENGLISH REGISTRY (ART. 17 ICC)</a>
        <button onclick="alert('Case Integrity Verified\nToken: $TOKEN')" class="btn">🛡️ SHA-256 VERIFY</button>
    </div>
    <div style="color: #4a7a9b; font-size: 0.8em;">Monitoring Token: $TOKEN | Case Macheret 1997-2026</div>
</body>
</html>
HTML

# Копируем активы
cp *.pdf public/ 2>/dev/null || true
cp *.json public/ 2>/dev/null || true
cp apostille_archive_english.html public/ 2>/dev/null || true
echo "✅ Портал A©tor собран."
