#!/bin/bash
TOKEN=$(date +%Y%m%d%H%M%S | sha256sum | head -c 10)
DELAY="6363 days (Intentional Sabotage)"
VOID="14.4% (Procedural Nullity)"

# Генерируем ГЛАВНУЮ (Портал Jus Cogens)
cat <<HTML > index.html
<!DOCTYPE html>
<html lang="ro">
<head><meta charset="UTF-8"><title>A©tor: Jus Cogens Portal</title>
<style>
    body{font-family:monospace;background:#000;color:#00ff00;padding:30px;line-height:1.4;}
    .vault{border:3px solid #00ff00;background:#050505;padding:25px;box-shadow:0 0 20px #00ff0033;}
    .critical{color:#ff0000;font-weight:bold;border:1px solid #ff0000;padding:10px;display:block;margin:15px 0;}
    .btn{background:#00ff00;color:#000;padding:15px 25px;border:none;cursor:pointer;font-weight:bold;text-decoration:none;display:inline-block;margin:5px;font-size:1.1em;}
    .btn-red{background:#ff0000;color:#fff;} .btn-gold{background:#ffcc00;color:#000;}
</style></head>
<body><div class="vault">
    <h1>Pârât: Ministerul Finanțelor RM</h1>
    <p>📍 Adresa: mun. Chișinău, str. Constantin Tănase, 8</p>
    <div class="critical">⚖️ LEGEA 1545/1995: НАРУШЕНИЯ ПУНКТОВ A, B, C, F (ПЫТКИ / КОНФИСКАЦИЯ)</div>
    <hr style="border:0;border-top:1px solid #00ff00;">
    <h3>📊 АУДИТ ЦЕЛОСТНОСТИ:</h3>
    <ul>
        <li>🛑 Временной разрыв: <strong>$DELAY</strong></li>
        <li>⚠️ Ничтожные акты: <strong>$VOID</strong></li>
    </ul>
    <hr style="border:0;border-top:1px solid #00ff00;">
    <a href="disability_evidence.html" class="btn btn-red">🚑 ИНВАЛИДНОСТЬ (ART. 3 CEDO)</a>
    <a href="un_petition_evidence.html" class="btn btn-gold">🇺🇳 ООН (ПЕТИЦИЯ)</a>
    <a href="cpt_evidence.html" class="btn">🇪🇺 ЕКПП (СТРАСБУРГ 2012)</a>
    <br><br>
    <a href="apostille_archive_english.html" class="btn" style="background:#fff">🌍 ENGLISH REGISTRY (ART. 17 ICC)</a>
</div><div style="color:#555;margin-top:20px;font-size:0.8em;">Monitoring Token: $TOKEN</div></body></html>
HTML

# Функция генерации страниц улик
gen_ev() {
cat <<HTML > "$1"
<!DOCTYPE html>
<html lang="ro"><head><meta charset="UTF-8"><title>$2</title><style>body{font-family:monospace;background:#000;color:#fff;padding:40px;line-height:1.6;} .box{border:2px solid $3;padding:30px;max-width:900px;margin:auto;}</style></head>
<body><div class="box"><h1 style="color:$3">$2</h1><p>$4</p><hr><a href="index.html" style="color:#00ff00;"><- ВЕРНУТЬСЯ В ПОРТАЛ</a><br><br><embed src="$5" type="application/pdf" width="100%" height="700px"></div></body></html>
HTML
}

gen_ev "disability_evidence.html" "PROBĂ: Dizabilitate Severă (Gr. I)" "#ff0000" "Бессрочная инвалидность. Прямое доказательство по Статье 3 CEDO." "disability_cert_gr1.pdf"
gen_ev "un_petition_evidence.html" "EVIDENCE: UN OHCHR Petition" "#ffcc00" "Регистрация дела в Комитете ООН (Женева)." "un_petition_urgent.pdf"
gen_ev "cpt_evidence.html" "УЛИКА: Ответ ЕКПП (CPT) 2012" "#00ff00" "Официальное признание ситуации Страсбургом более 13 лет назад." "cpt_response_2012.pdf"
