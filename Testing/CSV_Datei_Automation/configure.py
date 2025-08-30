#!/usr/bin/env python3
"""
Konfigurationsassistent für Shopware CSV Sync

Dieses Skript hilft beim Einrichten der Konfiguration.
"""

import os
import sys

def create_env_file():
    """Erstellt eine .env-Datei mit Benutzerangaben"""
    
    print("🔧 Shopware CSV Sync - Konfigurationsassistent")
    print("=" * 50)
    print()
    
    # Shopware-URL
    shopware_url = input("Shopware Shop URL (z.B. https://ihr-shop.de): ").strip()
    if not shopware_url.startswith(('http://', 'https://')):
        shopware_url = 'https://' + shopware_url
    
    # API-Zugangsdaten
    api_username = input("API Benutzername: ").strip()
    api_password = input("API Passwort: ").strip()
    
    # CSV-Pfad
    default_csv_path = "./data/products.csv"
    csv_path = input(f"CSV-Datei Pfad (Standard: {default_csv_path}): ").strip()
    if not csv_path:
        csv_path = default_csv_path
    
    # Prüfintervall
    default_interval = "60"
    check_interval = input(f"Prüfintervall in Sekunden (Standard: {default_interval}): ").strip()
    if not check_interval:
        check_interval = default_interval
    
    # Log-Level
    log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
    print(f"Verfügbare Log-Level: {', '.join(log_levels)}")
    log_level = input("Log-Level (Standard: INFO): ").strip().upper()
    if log_level not in log_levels:
        log_level = "INFO"
    
    # .env-Datei erstellen
    env_content = f"""# Shopware API Konfiguration
SHOPWARE_URL={shopware_url}
SHOPWARE_API_USERNAME={api_username}
SHOPWARE_API_PASSWORD={api_password}

# CSV-Datei Pfad
CSV_FILE_PATH={csv_path}

# Logging Konfiguration
LOG_LEVEL={log_level}
LOG_FILE=./logs/shopware_sync.log

# Update Intervall (in Sekunden)
CHECK_INTERVAL={check_interval}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env-Datei erfolgreich erstellt!")
        
        # Sicherheitshinweis
        print("\n🔒 Sicherheitshinweis:")
        print("Die .env-Datei enthält sensible Daten (Passwörter).")
        print("Stellen Sie sicher, dass diese Datei nicht in die Versionskontrolle (Git) gelangt.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Fehler beim Erstellen der .env-Datei: {e}")
        return False

def create_sample_csv():
    """Erstellt eine Beispiel-CSV-Datei"""
    
    # Verzeichnis erstellen falls nicht vorhanden
    os.makedirs('./data', exist_ok=True)
    
    csv_path = './data/products.csv'
    
    if os.path.exists(csv_path):
        overwrite = input(f"\nCSV-Datei {csv_path} existiert bereits. Überschreiben? (j/N): ").strip().lower()
        if overwrite not in ['j', 'ja', 'y', 'yes']:
            print("CSV-Datei nicht überschrieben.")
            return True
    
    sample_content = """product_number,name,description,price,stock,weight,ean,active
SW001,Beispielprodukt 1,Dies ist ein Beispielprodukt mit vielen tollen Eigenschaften,29.99,100,0.5,1234567890123,true
SW002,Beispielprodukt 2,Ein weiteres tolles Produkt für Ihren Shop,49.99,50,1.2,2345678901234,true
SW003,Beispielprodukt 3,Premium Produkt mit besonderen Features,99.99,25,2.1,3456789012345,false
SW004,Testprodukt,Ein Produkt zum Testen der Synchronisation,19.99,200,0.3,4567890123456,true"""
    
    try:
        with open(csv_path, 'w') as f:
            f.write(sample_content)
        
        print(f"\n✅ Beispiel-CSV-Datei erstellt: {csv_path}")
        print("Sie können diese Datei nach Ihren Bedürfnissen anpassen.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Fehler beim Erstellen der CSV-Datei: {e}")
        return False

def test_configuration():
    """Testet die Konfiguration"""
    
    print("\n🧪 Teste Konfiguration...")
    
    # .env-Datei prüfen
    if not os.path.exists('.env'):
        print("❌ .env-Datei nicht gefunden")
        return False
    
    # CSV-Datei prüfen
    csv_path = './data/products.csv'
    if not os.path.exists(csv_path):
        print(f"❌ CSV-Datei nicht gefunden: {csv_path}")
        return False
    
    print("✅ Grundkonfiguration ist vorhanden")
    
    # Optional: API-Verbindung testen
    test_api = input("API-Verbindung testen? (j/N): ").strip().lower()
    if test_api in ['j', 'ja', 'y', 'yes']:
        try:
            # Hier könnte ein einfacher API-Test implementiert werden
            print("⚠️ API-Test nicht implementiert. Führen Sie 'python main.py once' für einen vollständigen Test aus.")
        except Exception as e:
            print(f"❌ API-Test fehlgeschlagen: {e}")
            return False
    
    return True

def main():
    """Hauptfunktion"""
    
    print("Willkommen beim Shopware CSV Sync Konfigurationsassistenten!")
    print()
    
    # Schritt 1: .env-Datei
    if os.path.exists('.env'):
        recreate = input(".env-Datei existiert bereits. Neu erstellen? (j/N): ").strip().lower()
        if recreate in ['j', 'ja', 'y', 'yes']:
            if not create_env_file():
                return False
    else:
        if not create_env_file():
            return False
    
    # Schritt 2: CSV-Datei
    if not create_sample_csv():
        return False
    
    # Schritt 3: Test
    if not test_configuration():
        return False
    
    print("\n🎉 Konfiguration abgeschlossen!")
    print("\nNächste Schritte:")
    print("1. Passen Sie die CSV-Datei an Ihre Produkte an")
    print("2. Testen Sie die Verbindung mit: python main.py once")
    print("3. Starten Sie die Überwachung mit: python main.py watcher")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
