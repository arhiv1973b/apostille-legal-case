#!/bin/bash
TOKEN=$(date +%Y%m%d%H%M%S | sha256sum | head -c 10)

# Функция для страниц улик (ВЫСОКИЙ КОНТРАСТ)
gen_ev() {
cat <<HTML > "$1"
<!DOCTYPE html>
<html lang="ro"><head><meta charset="UTF-8"><title>$2</title><style>body{font-family:monospace;background:#000;color:#fff;padding:40px;line-height:1.6;} .box{border:2px solid $3;padding:30px;max-width:900px;margin:auto;}</style></head>
<body><div class="box"><h1 style="color:$3">$2</h1><p>$4</p><hr><a href="index.html" style="color:#00ff00;"><- ВЕРНУТЬСЯ</a><br><br><embed src="$5" type="application/pdf" width="100%" height="700px"></div></body></html>
HTML
}

# Генерация всех узлов
gen_ev "origin_1997_evidence.html" "🛡️ №0: КОРЕНЬ (1997)" "#ff00ff" "Подмена пыток на хулиганство." "torture_substitution_1997.pdf"
gen_ev "disability_evidence.html" "🚑 ИНВАЛИДНОСТЬ" "#ff0000" "Art. 3 CEDO: Группа I Бессрочно." "disability_cert_gr1.pdf"
gen_ev "un_petition_evidence.html" "🇺🇳 ООН" "#ffcc00" "Escalation to Geneva." "un_petition_urgent.pdf"
gen_ev "cpt_evidence.html" "🇪🇺 ЕКПП" "#00ff00" "Страсбург (2012)." "cpt_response_2012.pdf"

# ГЛАВНАЯ (БЕЗ ПАПКИ PUBLIC)
cat <<HTML > index.html
<!DOCTYPE html>
<html lang="ro"><head><meta charset="UTF-8"><title>A©tor: Jus Cogens Portal</title>
<style>body{font-family:monospace;background:#030a0f;color:#00ff00;padding:30px;} .vault{border:3px solid #00ff00;background:#050505;padding:25px;} .critical{color:#ff0000;font-weight:bold;border:1px solid #ff0000;padding:10px;display:block;margin:15px 0;} .btn{background:#00ff00;color:#000;padding:15px 25px;border:none;cursor:pointer;font-weight:bold;text-decoration:none;display:inline-block;margin:5px;font-size:1.1em;} .btn-red{background:#ff0000;color:#fff;} .btn-gold{background:#ffcc00;color:#000;} .btn-root{background:#ff00ff;color:#fff;} .btn-alt{background:#fff;color:#000;}</style></head>
<body><div class="vault"><h1>Pârât: Ministerul Finanțelor RM</h1><p>📍 Tănase, 8</p><div class="critical">⚖️ LEGEA 1545/1995: ПУНКТЫ A, B, C, F</div><hr style="border:0;border-top:1px solid #00ff00;margin:20px 0;">
<a href="origin_1997_evidence.html" class="btn btn-root">🛡️ №0: КОРЕНЬ (1997)</a>
<a href="disability_evidence.html" class="btn btn-red">🚑 ИНВАЛИДНОСТЬ</a>
<a href="un_petition_evidence.html" class="btn btn-gold">🇺🇳 ООН</a>
<a href="cpt_evidence.html" class="btn">🇪🇺 ЕКПП</a>
<br><br><a href="apostille_archive_english.html" class="btn btn-alt">🌍 ENGLISH REGISTRY (ART. 17 ICC)</a></div>
<div style="color:#555;margin-top:20px;font-size:0.8em;">Monitoring Token: $TOKEN</div></body></html>
HTML
