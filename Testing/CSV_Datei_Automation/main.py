#!/usr/bin/env python3
"""
Shopware CSV Produktsynchronisation - Hauptskript

Dieses Skript automatisiert die Synchronisation von Produktdaten zwischen
einer CSV-Datei und einem Shopware-Shop über die Admin API.

Verwendung:
    python main.py once           # Einmalige Synchronisation
    python main.py watcher        # Kontinuierliche Überwachung der CSV-Datei
    python main.py interval       # Intervallbasierte Prüfung auf Änderungen
"""

import sys
import os

# Pfad zum src-Verzeichnis hinzufügen
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sync_manager import ProductSyncManager

def main():
    """
    Hauptfunktion des Programms
    """
    sync_manager = ProductSyncManager()
    
    # Kommandozeilenargumente verarbeiten
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == 'once':
            print("🔄 Führe einmalige Synchronisation durch...")
            success = sync_manager.run_once()
            if success:
                print("✅ Synchronisation erfolgreich abgeschlossen!")
            else:
                print("❌ Synchronisation fehlgeschlagen!")
                sys.exit(1)
                
        elif mode == 'watcher':
            print("👀 Starte Dateiüberwachung...")
            print("Drücken Sie Ctrl+C zum Beenden")
            sync_manager.run_continuous('watcher')
            
        elif mode == 'interval':
            print("⏱️ Starte intervallbasierte Synchronisation...")
            print("Drücken Sie Ctrl+C zum Beenden")
            sync_manager.run_continuous('interval')
            
        elif mode in ['help', '-h', '--help']:
            print_help()
            
        else:
            print(f"❌ Unbekannter Modus: {mode}")
            print_help()
            sys.exit(1)
    else:
        print_help()

def print_help():
    """
    Gibt die Hilfe aus
    """
    print("""
🛍️ Shopware CSV Produktsynchronisation

Verwendung:
    python main.py <modus>

Modi:
    once        Einmalige Synchronisation aller Produkte
    watcher     Kontinuierliche Überwachung der CSV-Datei auf Änderungen
    interval    Intervallbasierte Prüfung auf CSV-Änderungen
    help        Diese Hilfe anzeigen

Konfiguration:
    Bearbeiten Sie die .env-Datei für Ihre Shopware-Einstellungen.

Beispiele:
    python main.py once         # Sofortige Synchronisation
    python main.py watcher      # Läuft dauerhaft und reagiert auf CSV-Änderungen
    python main.py interval     # Prüft alle X Sekunden auf Änderungen
    """)

if __name__ == "__main__":
    main()
