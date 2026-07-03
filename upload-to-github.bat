@echo off
chcp 65001 >nul
echo ========================================
echo   桌面文档清理 - 上传到 GitHub
echo ========================================
echo.

where git >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Git，请先安装：
    echo   https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

where gh >nul 2>&1
if errorlevel 1 (
    echo [提示] 未检测到 GitHub CLI，将使用 git 手动推送。
    echo   建议安装 gh：https://cli.github.com/
    echo.
)

cd /d "%~dp0"

if not exist .git (
    echo [1/4] 初始化 Git 仓库...
    git init
    git branch -M main
) else (
    echo [1/4] Git 仓库已存在
)

echo [2/4] 添加文件...
git add cleaner.pyw setup.py run.bat requirements.txt README.md .gitignore icon.ico 2>nul
git add .

echo [3/4] 提交...
git commit -m "Initial commit: desktop document cleaner tool" 2>nul
if errorlevel 1 (
    echo 没有新改动，或已提交过。
)

echo [4/4] 创建 GitHub 仓库并推送...
where gh >nul 2>&1
if not errorlevel 1 (
    gh repo create desktop-doc-cleaner --public --source=. --remote=origin --push
    if not errorlevel 1 (
        echo.
        echo 上传成功！
        gh repo view --web
        pause
        exit /b 0
    )
)

echo.
echo 若 gh 不可用，请手动操作：
echo   1. 打开 https://github.com/new
echo   2. 仓库名填 desktop-doc-cleaner，选 Public，创建
echo   3. 执行以下命令：
echo.
echo   git remote add origin https://github.com/nememene/desktop-doc-cleaner.git
echo   git push -u origin main
echo.
echo 仓库地址: https://github.com/nememene/desktop-doc-cleaner
pause
