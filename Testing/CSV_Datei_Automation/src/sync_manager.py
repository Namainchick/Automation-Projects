import time
import logging
import os
from datetime import datetime

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("⚠️ Watchdog nicht verfügbar. Dateiüberwachung deaktiviert.")

try:
    from decouple import config
except ImportError:
    print("⚠️ python-decouple nicht verfügbar. Verwende Umgebungsvariablen.")
    import os
    def config(key, default=None):
        return os.getenv(key, default)

from csv_processor import CSVProcessor
from shopware_api import ShopwareAPI

class CSVFileHandler(FileSystemEventHandler):
    """
    Handler für Dateiänderungen (nur verfügbar wenn watchdog installiert ist)
    """
    
    def __init__(self, csv_file_path: str, sync_manager):
        if not WATCHDOG_AVAILABLE:
            raise ImportError("Watchdog ist nicht verfügbar")
        super().__init__()
        self.csv_file_path = csv_file_path
        self.sync_manager = sync_manager
        self.logger = logging.getLogger(__name__)
    
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if event.src_path == self.csv_file_path:
            self.logger.info(f"CSV-Datei geändert: {event.src_path}")
            # Kurze Verzögerung, um sicherzustellen, dass die Datei vollständig geschrieben wurde
            time.sleep(1)
            self.sync_manager.sync_products()

class ProductSyncManager:
    """
    Hauptklasse für die Synchronisation von Produkten
    """
    
    def __init__(self):
        # Konfiguration laden
        self.csv_file_path = config('CSV_FILE_PATH')
        self.check_interval = int(config('CHECK_INTERVAL', 60))
        
        # Komponenten initialisieren
        self.csv_processor = CSVProcessor(self.csv_file_path)
        self.shopware_api = ShopwareAPI()
        
        # Logger konfigurieren
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Erforderliche CSV-Spalten definieren
        self.required_columns = [
            'product_number',
            'name',
            'price',
            'stock'
        ]
        
    def setup_logging(self):
        """
        Konfiguriert das Logging-System
        """
        log_level = config('LOG_LEVEL', 'INFO')
        log_file = config('LOG_FILE', './logs/shopware_sync.log')
        
        # Log-Verzeichnis erstellen falls nicht vorhanden
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def validate_setup(self) -> bool:
        """
        Validiert die Einrichtung vor dem Start
        """
        # CSV-Datei prüfen
        if not os.path.exists(self.csv_file_path):
            self.logger.error(f"CSV-Datei nicht gefunden: {self.csv_file_path}")
            return False
        
        # CSV-Struktur validieren
        if not self.csv_processor.validate_csv_structure(self.required_columns):
            return False
        
        # Shopware API testen
        if not self.shopware_api.authenticate():
            self.logger.error("Shopware API Authentifizierung fehlgeschlagen")
            return False
        
        self.logger.info("Setup-Validierung erfolgreich")
        return True
    
    def sync_products(self) -> bool:
        """
        Synchronisiert alle Produkte aus der CSV-Datei
        """
        self.logger.info("Starte Produktsynchronisation...")
        
        # CSV-Daten lesen
        csv_data = self.csv_processor.read_csv_data()
        if not csv_data:
            self.logger.error("Keine Daten aus CSV-Datei gelesen")
            return False
        
        success_count = 0
        error_count = 0
        
        # Jedes Produkt synchronisieren
        for row in csv_data:
            try:
                if self.shopware_api.sync_product_from_csv_data(row):
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                self.logger.error(f"Fehler beim Synchronisieren des Produkts: {e}")
                error_count += 1
        
        self.logger.info(f"Synchronisation abgeschlossen: {success_count} erfolgreich, {error_count} Fehler")
        return error_count == 0
    
    def start_file_watcher(self):
        """
        Startet die Dateiüberwachung (erfordert watchdog)
        """
        if not WATCHDOG_AVAILABLE:
            self.logger.error("Watchdog ist nicht verfügbar. Verwenden Sie stattdessen den interval-Modus.")
            return False
            
        self.logger.info("Starte Dateiüberwachung...")
        
        try:
            event_handler = CSVFileHandler(self.csv_file_path, self)
            observer = Observer()
            
            # Überwache das Verzeichnis der CSV-Datei
            watch_directory = os.path.dirname(self.csv_file_path)
            observer.schedule(event_handler, watch_directory, recursive=False)
            
            observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("Dateiüberwachung wird beendet...")
                observer.stop()
            
            observer.join()
            return True
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Dateiüberwachung: {e}")
            return False
    
    def start_interval_sync(self):
        """
        Startet die intervallbasierte Synchronisation
        """
        self.logger.info(f"Starte intervallbasierte Synchronisation (alle {self.check_interval} Sekunden)...")
        
        try:
            while True:
                if self.csv_processor.has_file_changed():
                    self.logger.info("CSV-Datei hat sich geändert - starte Synchronisation")
                    self.sync_products()
                else:
                    self.logger.debug("Keine Änderungen in CSV-Datei erkannt")
                
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Intervall-Synchronisation wird beendet...")
    
    def run_once(self):
        """
        Führt eine einmalige Synchronisation durch
        """
        self.logger.info("Führe einmalige Synchronisation durch...")
        
        if not self.validate_setup():
            return False
        
        return self.sync_products()
    
    def run_continuous(self, mode='watcher'):
        """
        Startet die kontinuierliche Synchronisation
        
        Args:
            mode: 'watcher' für Dateiüberwachung oder 'interval' für intervallbasierte Prüfung
        """
        if not self.validate_setup():
            return
        
        # Initiale Synchronisation
        self.sync_products()
        
        if mode == 'watcher':
            self.start_file_watcher()
        elif mode == 'interval':
            self.start_interval_sync()
        else:
            self.logger.error(f"Unbekannter Modus: {mode}")

if __name__ == "__main__":
    sync_manager = ProductSyncManager()
    
    # Kommandozeilenargumente verarbeiten
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'once':
            sync_manager.run_once()
        elif sys.argv[1] == 'watcher':
            sync_manager.run_continuous('watcher')
        elif sys.argv[1] == 'interval':
            sync_manager.run_continuous('interval')
        else:
            print("Verwendung: python sync_manager.py [once|watcher|interval]")
    else:
        # Standard: Dateiüberwachung
        sync_manager.run_continuous('watcher')
