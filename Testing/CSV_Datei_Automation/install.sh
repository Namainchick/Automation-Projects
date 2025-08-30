#!/bin/bash

# Shopware CSV Sync - Installationsskript

echo "🛍️ Shopware CSV Produktsynchronisation - Installation"
echo "=================================================="

# Python-Version prüfen
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Python gefunden: $python_version"
else
    echo "❌ Python 3 ist nicht installiert oder nicht im PATH"
    exit 1
fi

# Virtual Environment erstellen
echo "📦 Erstelle Virtual Environment..."
python3 -m venv venv

# Virtual Environment aktivieren
echo "🔧 Aktiviere Virtual Environment..."
source venv/bin/activate

# Dependencies installieren
echo "📥 Installiere Dependencies..."
pip install -r requirements.txt

if [[ $? -eq 0 ]]; then
    echo "✅ Dependencies erfolgreich installiert"
else
    echo "❌ Fehler beim Installieren der Dependencies"
    exit 1
fi

# .env-Datei prüfen
if [[ ! -f .env ]]; then
    echo "⚠️ Warnung: .env-Datei nicht gefunden"
    echo "📝 Bitte konfigurieren Sie Ihre Shopware-Zugangsdaten in der .env-Datei"
else
    echo "✅ .env-Datei gefunden"
fi

# CSV-Datei prüfen
if [[ ! -f ./data/products.csv ]]; then
    echo "⚠️ Warnung: CSV-Datei nicht gefunden"
    echo "📁 Eine Beispiel-CSV wurde in ./data/products.csv erstellt"
else
    echo "✅ CSV-Datei gefunden"
fi

echo ""
echo "🎉 Installation abgeschlossen!"
echo ""
echo "Nächste Schritte:"
echo "1. Konfigurieren Sie Ihre .env-Datei mit Ihren Shopware-Zugangsdaten"
echo "2. Passen Sie Ihre CSV-Datei an (./data/products.csv)"
echo "3. Testen Sie die Installation mit: python main.py once"
echo "4. Starten Sie die kontinuierliche Überwachung mit: python main.py watcher"
echo ""
echo "Für detaillierte Anweisungen lesen Sie die README.md"
