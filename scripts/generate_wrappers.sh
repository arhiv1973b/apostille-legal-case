#!/bin/bash
TOKEN=$(date +%Y%m%d%H%M%S | sha256sum | head -c 10)
DELAY="6363 days (Intentional Sabotage)"
VOID="14.4% (Procedural Nullity)"

# Функция генерации страниц улик
gen_ev() {
cat <<HTML > "$1"
<!DOCTYPE html>
<html lang="ro"><head><meta charset="UTF-8"><title>$2</title><style>body{font-family:monospace;background:#000;color:#fff;padding:40px;line-height:1.6;} .box{border:2px solid $3;padding:30px;max-width:900px;margin:auto;}</style></head>
<body><div class="box"><h1 style="color:$3">$2</h1><p>$4</p><hr><a href="index.html" style="color:#00ff00;"><- ВЕРНУТЬСЯ</a><br><br>$5</div></body></html>
HTML
}

# Регистрация всех страниц
gen_ev "disability_evidence.html" "PROBĂ: Dizabilitate Severă" "#ff0000" "Бессрочная инвалидность. Art. 3 CEDO." '<embed src="disability_cert_gr1.pdf" type="application/pdf" width="100%" height="700px">'
gen_ev "un_petition_evidence.html" "EVIDENCE: UN OHCHR Petition" "#ffcc00" "Регистрация в ООН (Женева)." '<embed src="un_petition_urgent.pdf" type="application/pdf" width="100%" height="700px">'
gen_ev "cpt_evidence.html" "УЛИКА: Ответ ЕКПП (2012)" "#00ff00" "Признание Страсбурга." '<embed src="cpt_response_2012.pdf" type="application/pdf" width="100%" height="700px">'
gen_ev "audit_audio.html" "УЛИКА: Аудио-протокол 9600" "#00c6ff" "Звуковая фиксация процесса аудита." '<audio controls style="width:100%;"><source src="audit_9600.mp3" type="audio/mpeg"></audio>'

# НОВАЯ КОРНЕВАЯ УЛИКА (1997)
gen_ev "origin_1997_evidence.html" "УЛИКА: Подмена пыток (1997)" "#ff00ff" "Доказательство исходного подлога квалификации со ст. 219 на хулиганство." '<embed src="torture_substitution_1997.pdf" type="application/pdf" width="100%" height="700px">'

# ГЛАВНАЯ (Обновленная с 5 кнопками)
cat <<HTML > index.html
<!DOCTYPE html>
<html lang="ro">
<head><meta charset="UTF-8"><title>A©tor: Jus Cogens Portal</title>
<style>
    body{font-family:monospace;background:#030a0f;color:#00ff00;padding:30px;line-height:1.4;}
    .vault{border:3px solid #00ff00;background:#050505;padding:25px;box-shadow:0 0 20px #00ff0033;}
    .critical{color:#ff0000;font-weight:bold;border:1px solid #ff0000;padding:10px;display:block;margin:15px 0;}
    .btn{background:#00ff00;color:#000;padding:15px 25px;border:none;cursor:pointer;font-weight:bold;text-decoration:none;display:inline-block;margin:5px;font-size:1.1em;}
    .btn-red{background:#ff0000;color:#fff;} .btn-gold{background:#ffcc00;color:#000;} .btn-blue{background:#00c6ff;color:#000;} .btn-root{background:#ff00ff;color:#fff;}
</style></head>
<body><div class="vault">
    <h1>Pârât: Ministerul Finanțelor RM</h1>
    <div class="critical">⚖️ LEGEA 1545/1995: НАРУШЕНИЯ A, B, C, F</div>
    <hr style="border:0;border-top:1px solid #00ff00;">
    
    <a href="origin_1997_evidence.html" class="btn btn-root">🛡️ УЛИКА №0: КОРЕНЬ (1997)</a>
    <a href="disability_evidence.html" class="btn btn-red">🚑 ИНВАЛИДНОСТЬ</a>
    <a href="un_petition_evidence.html" class="btn btn-gold">🇺🇳 ООН</a>
    <a href="cpt_evidence.html" class="btn">🇪🇺 ЕКПП</a>
    <a href="audit_audio.html" class="btn btn-blue">🎙️ АУДИО-АУДИТ</a>
    
    <br><br>
    <a href="apostille_archive_english.html" class="btn" style="background:#fff">🌍 ENGLISH REGISTRY (ART. 17 ICC)</a>
</div><div style="color:#555;margin-top:20px;font-size:0.8em;">Monitoring Token: $TOKEN</div></body></html>
HTML
