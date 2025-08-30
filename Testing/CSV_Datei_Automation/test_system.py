#!/usr/bin/env python3
"""
Test-Skript für die Shopware CSV Synchronisation

Dieses Skript testet die verschiedenen Komponenten des Systems.
"""

import sys
import os

# Pfad zum src-Verzeichnis hinzufügen
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_csv_processor():
    """Test der CSV-Verarbeitung"""
    print("🧪 Teste CSV-Processor...")
    
    try:
        from csv_processor import CSVProcessor
        
        processor = CSVProcessor('./data/products.csv')
        
        # Test: Datei-Hash berechnen
        file_hash = processor.calculate_file_hash()
        if file_hash:
            print(f"✅ Datei-Hash berechnet: {file_hash[:10]}...")
        else:
            print("❌ Konnte Datei-Hash nicht berechnen")
            return False
        
        # Test: CSV-Daten lesen
        data = processor.read_csv_data()
        if data:
            print(f"✅ CSV-Daten gelesen: {len(data)} Zeilen")
        else:
            print("❌ Konnte CSV-Daten nicht lesen")
            return False
        
        # Test: CSV-Struktur validieren
        required_columns = ['product_number', 'name', 'price', 'stock']
        if processor.validate_csv_structure(required_columns):
            print("✅ CSV-Struktur ist gültig")
        else:
            print("❌ CSV-Struktur ist ungültig")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        return False
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        return False

def test_shopware_api():
    """Test der Shopware API (ohne tatsächliche Verbindung)"""
    print("\n🧪 Teste Shopware API...")
    
    try:
        from shopware_api import ShopwareAPI
        
        # API-Objekt erstellen (ohne Authentifizierung)
        api = ShopwareAPI()
        print("✅ ShopwareAPI-Objekt erstellt")
        
        # Test: Produktdaten vorbereiten
        test_data = {
            'product_number': 'TEST001',
            'name': 'Test Produkt',
            'price': '29.99',
            'stock': '100'
        }
        
        product_data = api._prepare_product_data(test_data)
        if product_data and 'productNumber' in product_data:
            print("✅ Produktdaten-Vorbereitung funktioniert")
        else:
            print("❌ Produktdaten-Vorbereitung fehlgeschlagen")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import-Fehler: {e}")
        return False
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")
        return False

def test_configuration():
    """Test der Konfiguration"""
    print("\n🧪 Teste Konfiguration...")
    
    # .env-Datei prüfen
    if os.path.exists('.env'):
        print("✅ .env-Datei gefunden")
        
        with open('.env', 'r') as f:
            content = f.read()
            
        required_vars = ['SHOPWARE_URL', 'SHOPWARE_API_USERNAME', 'SHOPWARE_API_PASSWORD']
        missing_vars = []
        
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️ Fehlende Konfigurationsvariablen: {', '.join(missing_vars)}")
        else:
            print("✅ Alle erforderlichen Konfigurationsvariablen gefunden")
    else:
        print("❌ .env-Datei nicht gefunden")
        return False
    
    # CSV-Datei prüfen
    csv_path = './data/products.csv'
    if os.path.exists(csv_path):
        print("✅ CSV-Datei gefunden")
    else:
        print("❌ CSV-Datei nicht gefunden")
        return False
    
    return True

def test_dependencies():
    """Test der Dependencies"""
    print("\n🧪 Teste Dependencies...")
    
    dependencies = [
        ('pandas', 'CSV-Verarbeitung'),
        ('requests', 'HTTP-Requests'),
        ('watchdog', 'Dateiüberwachung'),
        ('decouple', 'Konfiguration')
    ]
    
    missing_deps = []
    
    for dep, description in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} ({description}) verfügbar")
        except ImportError:
            print(f"❌ {dep} ({description}) nicht verfügbar")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n📦 Fehlende Dependencies installieren mit:")
        print(f"pip install {' '.join(missing_deps)}")
        return False
    
    return True

def main():
    """Hauptfunktion für alle Tests"""
    print("🔍 Shopware CSV Sync - System-Test")
    print("=" * 40)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Konfiguration", test_configuration),
        ("CSV-Processor", test_csv_processor),
        ("Shopware API", test_shopware_api)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test '{test_name}' fehlgeschlagen: {e}")
            results.append((test_name, False))
    
    # Zusammenfassung
    print("\n" + "=" * 40)
    print("📊 Test-Zusammenfassung:")
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        if result:
            print(f"✅ {test_name}")
            passed += 1
        else:
            print(f"❌ {test_name}")
            failed += 1
    
    print(f"\n🎯 Ergebnis: {passed} erfolgreich, {failed} fehlgeschlagen")
    
    if failed == 0:
        print("\n🎉 Alle Tests bestanden! Das System ist einsatzbereit.")
        return True
    else:
        print("\n⚠️ Einige Tests sind fehlgeschlagen. Bitte beheben Sie die Probleme vor der Verwendung.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
