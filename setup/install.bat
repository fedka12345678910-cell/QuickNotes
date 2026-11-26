@echo off
chcp 65001 >nul
set "INSTALL_DIR=%USERPROFILE%\QuickNotes"
set "DESKTOP_BAT=%USERPROFILE%\Desktop\QuickNotes.bat"

echo [1/5] Проверка наличия Python...
python --version >nul 2>&1 || (echo Ошибка: Python не установлен! & pause & exit /b 1)

echo [2/5] Создание каталога установки "%INSTALL_DIR%"...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [3/5] Копирование файлов приложения QuickNotes...
xcopy /E /I /Y "%~dp0..\*" "%INSTALL_DIR%\" >nul

echo [4/5] Установка зависимостей Python...
pip install -r "%INSTALL_DIR%\requirements.txt"

echo [5/5] Создание ярлыка запуска на рабочем столе...
(
  echo @echo off
  echo cd /d "%INSTALL_DIR%"
  echo start "" http://127.0.0.1:5000
  echo python app.py
) > "%DESKTOP_BAT%"

echo ============================================
echo  Установка QuickNotes успешно завершена!
echo ============================================
pause
