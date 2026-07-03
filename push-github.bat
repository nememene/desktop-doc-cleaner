@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo 正在上传到 github.com/nememene/desktop-doc-cleaner ...
echo.

where git >nul 2>&1
if errorlevel 1 (
    echo [错误] 请先安装 Git: https://git-scm.com/download/win
    pause
    exit /b 1
)

if not exist .git git init
git branch -M main 2>nul
git add cleaner.pyw setup.py run.bat requirements.txt README.md .gitignore upload-to-github.bat push-github.bat icon.ico 2>nul
git add .
git commit -m "Initial commit: desktop document cleaner tool" 2>nul

git remote remove origin 2>nul
git remote add origin https://github.com/nememene/desktop-doc-cleaner.git
git push -u origin main

if errorlevel 1 (
    echo.
    echo 推送失败。请确认：
    echo   1. 已在 https://github.com/new 创建仓库 desktop-doc-cleaner
    echo   2. 已登录 GitHub（git config 或 GitHub Desktop）
    echo.
) else (
    echo.
    echo 上传成功！
    echo https://github.com/nememene/desktop-doc-cleaner
)

pause
