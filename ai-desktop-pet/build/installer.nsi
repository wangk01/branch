; NSIS 安装脚本 - AI Desktop Pet
!include "MUI2.nsh"

!define APP_NAME "AI Desktop Pet"
!define APP_VERSION "1.0.0"
!define APP_EXE "AIDesktopPet.exe"
!define INSTALL_DIR "$PROGRAMFILES\AIDesktopPet"
!define UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\AIDesktopPet"

; 输出文件名
OutFile "..\dist\AIDesktopPet-Setup.exe"
InstallDir "${INSTALL_DIR}"
RequestExecutionLevel admin

; 界面
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "SimpChinese"

Section "Install"
  SetOutPath "${INSTALL_DIR}"
  File /r "${APP_DIR}\*.*"

  ; 创建开始菜单快捷方式
  CreateDirectory "$SMPROGRAMS\AI Desktop Pet"
  CreateShortcut "$SMPROGRAMS\AI Desktop Pet\${APP_NAME}.lnk" "${INSTALL_DIR}\${APP_EXE}"
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "${INSTALL_DIR}\${APP_EXE}"

  ; 写卸载信息
  WriteUninstaller "${INSTALL_DIR}\Uninstall.exe"
  WriteRegStr HKLM "${UNINST_KEY}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "${UNINST_KEY}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "${UNINST_KEY}" "UninstallString" "${INSTALL_DIR}\Uninstall.exe"
  WriteRegDWORD HKLM "${UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKLM "${UNINST_KEY}" "NoRepair" 1
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\AI Desktop Pet\${APP_NAME}.lnk"
  RMDir "$SMPROGRAMS\AI Desktop Pet"
  RMDir /r "${INSTALL_DIR}"
  DeleteRegKey HKLM "${UNINST_KEY}"
SectionEnd
