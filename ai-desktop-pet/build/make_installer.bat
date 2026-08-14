@echo off
REM 使用 NSIS 生成安装程序
REM 需先安装 NSIS: https://nsis.sourceforge.io/
chcp 65001 >nul

set DIST=dist\AIDesktopPet
if not exist "%DIST%\AIDesktopPet.exe" (
    echo 未找到打包产物，请先运行 build\build.bat
    exit /b 1
)

makensis /DAPP_DIR="%DIST%" build\installer.nsi
if errorlevel 1 (
    echo 安装程序生成失败，请确认已安装 NSIS 并将 makensis 加入 PATH
    exit /b 1
)

echo 安装程序已生成: dist\AIDesktopPet-Setup.exe
