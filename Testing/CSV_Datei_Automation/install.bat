@echo off
echo 🛍️ Shopware CSV Produktsynchronisation - Installation (Windows)
echo ==============================================================

REM Python-Version prüfen
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python ist nicht installiert oder nicht im PATH
    echo Bitte installieren Sie Python von https://python.org
    pause
    exit /b 1
)

python --version
echo ✅ Python gefunden

REM Virtual Environment erstellen
echo 📦 Erstelle Virtual Environment...
python -m venv venv

REM Virtual Environment aktivieren
echo 🔧 Aktiviere Virtual Environment...
call venv\Scripts\activate.bat

REM Dependencies installieren
echo 📥 Installiere Dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Fehler beim Installieren der Dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies erfolgreich installiert

REM .env-Datei prüfen
if not exist .env (
    echo ⚠️ Warnung: .env-Datei nicht gefunden
    echo 📝 Bitte konfigurieren Sie Ihre Shopware-Zugangsdaten in der .env-Datei
) else (
    echo ✅ .env-Datei gefunden
)

REM CSV-Datei prüfen
if not exist "data\products.csv" (
    echo ⚠️ Warnung: CSV-Datei nicht gefunden
    echo 📁 Eine Beispiel-CSV wurde in .\data\products.csv erstellt
) else (
    echo ✅ CSV-Datei gefunden
)

echo.
echo 🎉 Installation abgeschlossen!
echo.
echo Nächste Schritte:
echo 1. Konfigurieren Sie Ihre .env-Datei mit Ihren Shopware-Zugangsdaten
echo 2. Passen Sie Ihre CSV-Datei an (.\data\products.csv)
echo 3. Testen Sie die Installation mit: python main.py once
echo 4. Starten Sie die kontinuierliche Überwachung mit: python main.py watcher
echo.
echo Für detaillierte Anweisungen lesen Sie die README.md
pause
