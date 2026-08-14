@echo off
REM ============================================
REM  AI Desktop Pet - Windows 打包脚本
REM  需要先安装 Python 3.10+，再执行：
REM    pip install -r requirements.txt pyinstaller
REM ============================================
chcp 65001 >nul
setlocal

echo [1/3] 安装打包依赖...
pip install -r requirements.txt pyinstaller || goto :error

echo [2/3] 使用 PyInstaller 打包...
pyinstaller --clean --noconfirm build\desktop-pet.spec || goto :error

echo [3/3] 打包完成！
echo 产物目录: dist\AIDesktopPet\
echo 单文件入口: dist\AIDesktopPet\AIDesktopPet.exe
echo 如需生成安装程序，请安装 NSIS 后运行 build\make_installer.bat
goto :eof

:error
echo 打包失败，请检查上方错误信息。
exit /b 1
