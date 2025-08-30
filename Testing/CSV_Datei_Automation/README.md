# Shopware CSV Produktsynchronisation

Dieses System automatisiert die Synchronisation von Produktdaten zwischen einer CSV-Datei und Ihrem Shopware-Shop über die Admin API.

## 🚀 Features

- **Automatische Erkennung von CSV-Änderungen** - Das System überwacht Ihre CSV-Datei und synchronisiert automatisch bei Änderungen
- **Flexible Synchronisationsmodi** - Wählen Sie zwischen einmaliger Synchronisation, Dateiüberwachung oder intervallbasierter Prüfung
- **Vollständige Shopware Integration** - Nutzt die offizielle Shopware Admin API
- **Robuste Fehlerbehandlung** - Ausführliches Logging und Fehlerbehandlung
- **Einfache Konfiguration** - Alle Einstellungen über .env-Datei

## 📋 Voraussetzungen

- Python 3.7 oder höher
- Shopware 6 mit aktivierter Admin API
- API-Benutzer mit entsprechenden Berechtigungen

## 🛠️ Installation

1. **Repository klonen oder Dateien herunterladen**

2. **Dependencies installieren:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Konfiguration anpassen:**
   Bearbeiten Sie die `.env`-Datei mit Ihren Shopware-Zugangsdaten:
   ```
   SHOPWARE_URL=https://ihr-shop.de
   SHOPWARE_API_USERNAME=ihr_api_username
   SHOPWARE_API_PASSWORD=ihr_api_password
   CSV_FILE_PATH=./data/products.csv
   ```

## 📊 CSV-Format

Ihre CSV-Datei sollte mindestens folgende Spalten enthalten:

| Spalte | Beschreibung | Erforderlich |
|--------|-------------|--------------|
| product_number | Eindeutige Produktnummer | ✅ |
| name | Produktname | ✅ |
| price | Preis (brutto) | ✅ |
| stock | Lagerbestand | ✅ |
| description | Produktbeschreibung | ❌ |
| weight | Gewicht in kg | ❌ |
| ean | EAN-Code | ❌ |
| active | Aktiv (true/false) | ❌ |

**Beispiel CSV:**
```csv
product_number,name,description,price,stock,weight,ean,active
SW001,Beispielprodukt 1,Dies ist ein Beispielprodukt,29.99,100,0.5,1234567890123,true
SW002,Beispielprodukt 2,Ein weiteres Produkt,49.99,50,1.2,2345678901234,true
```

## 🎮 Verwendung

### Einmalige Synchronisation
Führt eine sofortige Synchronisation aller Produkte durch:
```bash
python main.py once
```

### Dateiüberwachung (Empfohlen)
Überwacht die CSV-Datei kontinuierlich und synchronisiert automatisch bei Änderungen:
```bash
python main.py watcher
```

### Intervallbasierte Prüfung
Prüft in regelmäßigen Abständen auf CSV-Änderungen:
```bash
python main.py interval
```

## ⚙️ Konfiguration

### .env-Datei Optionen

```env
# Shopware API Konfiguration
SHOPWARE_URL=https://ihr-shop.de
SHOPWARE_API_USERNAME=ihr_api_username  
SHOPWARE_API_PASSWORD=ihr_api_password

# CSV-Datei Pfad
CSV_FILE_PATH=./data/products.csv

# Logging Konfiguration
LOG_LEVEL=INFO
LOG_FILE=./logs/shopware_sync.log

# Update Intervall (in Sekunden, nur für interval-Modus)
CHECK_INTERVAL=60
```

### Shopware API-Benutzer einrichten

1. **Admin-Panel öffnen:** Melden Sie sich in Ihrem Shopware Admin-Panel an
2. **Benutzer erstellen:** Gehen Sie zu "Einstellungen" > "System" > "Benutzer & Berechtigungen"
3. **API-Zugang aktivieren:** Erstellen Sie einen neuen Benutzer oder bearbeiten Sie einen bestehenden
4. **Berechtigungen setzen:** Der Benutzer benötigt mindestens Lese- und Schreibzugriff auf Produkte

## 📝 Logging

Das System protokolliert alle Aktivitäten in:
- **Konsole:** Für direktes Feedback
- **Log-Datei:** `./logs/shopware_sync.log` für detaillierte Protokolle

Log-Level können in der .env-Datei angepasst werden (DEBUG, INFO, WARNING, ERROR).

## 🔧 Erweiterte Konfiguration

### Zusätzliche CSV-Spalten

Um zusätzliche CSV-Spalten zu verarbeiten, bearbeiten Sie die `_prepare_product_data` Methode in `src/shopware_api.py`:

```python
def _prepare_product_data(self, csv_row: Dict) -> Dict:
    product_data = {
        # ... bestehende Felder ...
        "manufacturerNumber": csv_row.get('manufacturer_number'),
        "keywords": csv_row.get('keywords'),
        # Weitere Felder hinzufügen...
    }
    return product_data
```

### Währung und Steuern anpassen

Die Standard-Konfiguration verwendet EUR und 19% MwSt. Diese können in der `_prepare_product_data` Methode angepasst werden.

## 🚨 Troubleshooting

### Häufige Probleme

**Authentication Failed:**
- Prüfen Sie Ihre Shopware-URL und API-Zugangsdaten
- Stellen Sie sicher, dass der API-Benutzer die erforderlichen Berechtigungen hat

**CSV-Datei nicht gefunden:**
- Überprüfen Sie den Pfad in der .env-Datei
- Stellen Sie sicher, dass die Datei existiert und lesbar ist

**Produkt wird nicht aktualisiert:**
- Prüfen Sie, ob die product_number eindeutig ist
- Überprüfen Sie die Log-Datei für detaillierte Fehlermeldungen

### Debug-Modus aktivieren

Setzen Sie in der .env-Datei:
```env
LOG_LEVEL=DEBUG
```

## 🔄 Automatisierung

### Als Service ausführen (Linux)

Erstellen Sie eine systemd-Service-Datei:

```ini
[Unit]
Description=Shopware CSV Sync
After=network.target

[Service]
Type=simple
User=ihr-benutzer
WorkingDirectory=/pfad/zu/ihrem/projekt
ExecStart=/usr/bin/python3 main.py watcher
Restart=always

[Install]
WantedBy=multi-user.target
```

### Mit Cron-Job (für interval-Modus)

```bash
# Läuft alle 5 Minuten
*/5 * * * * cd /pfad/zu/ihrem/projekt && python3 main.py once
```

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## 🤝 Support

Bei Fragen oder Problemen:
1. Überprüfen Sie die Log-Dateien
2. Stellen Sie sicher, dass alle Voraussetzungen erfüllt sind
3. Testen Sie die Shopware API-Verbindung manuell
