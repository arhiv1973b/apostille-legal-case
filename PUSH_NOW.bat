@echo off
chcp 65001 >nul 2>&1
title A©tor — Git Push → GitHub Pages

cd /d "%~dp0"

echo.
echo  ╔═══════════════════════════════════════╗
echo  ║  PUSH → GITHUB PAGES DEPLOY          ║
echo  ║  apostille-legal-case                 ║
echo  ╚═══════════════════════════════════════╝
echo.

:: Проверка git
where git >nul 2>&1
if errorlevel 1 (
    echo [!] Git не найден. Скачайте: https://git-scm.com/download/win
    pause & exit /b
)

:: Показываем статус
echo [1] Текущая ветка и статус:
git branch --show-current
git status --short
echo.

:: Добавляем ВСЕ файлы
echo [2] git add -A
git add -A

:: Коммит
echo [3] git commit
git commit -m "fix: navigator + DULCHA + 404-tunnel + _config.yml plugin fix [%date% %time%]"

:: Push — пробуем все варианты ветки
echo [4] git push
git push 2>nul
if errorlevel 1 (
    for %%B in (master main) do (
        git push origin %%B 2>nul && goto :ok
    )
    echo.
    echo [!] Push не удался. Проверьте интернет и доступ к GitHub.
    pause & exit /b
)

:ok
echo.
echo  ╔═══════════════════════════════════════╗
echo  ║  PUSH ВЫПОЛНЕН                        ║
echo  ║  GitHub деплоит ~60 сек               ║
echo  ╚═══════════════════════════════════════╝
echo.
echo  Навигатор будет доступен по адресу:
echo  https://arhiv1973b.github.io/apostille-legal-case/docs-agent-navigator.html
echo.
echo  Открываю через 10 секунд...
timeout /t 10 /nobreak >nul
start "" "https://arhiv1973b.github.io/apostille-legal-case/docs-agent-navigator.html"
echo.
echo  Готово. Нажмите любую клавишу для выхода.
pause >nul
