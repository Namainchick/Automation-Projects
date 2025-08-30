import os
import hashlib
import logging
from typing import Dict, List, Optional
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    print("❌ pandas nicht installiert. Installieren Sie es mit: pip install pandas")
    raise

class CSVProcessor:
    """
    Klasse für die Verarbeitung der CSV-Datei
    """
    
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.last_hash = None
        self.logger = logging.getLogger(__name__)
        
    def calculate_file_hash(self) -> Optional[str]:
        """
        Berechnet den Hash der CSV-Datei für Änderungserkennung
        """
        try:
            if not os.path.exists(self.csv_file_path):
                self.logger.warning(f"CSV-Datei nicht gefunden: {self.csv_file_path}")
                return None
                
            with open(self.csv_file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
                
        except Exception as e:
            self.logger.error(f"Fehler beim Berechnen des Datei-Hash: {e}")
            return None
    
    def has_file_changed(self) -> bool:
        """
        Prüft, ob sich die CSV-Datei geändert hat
        """
        current_hash = self.calculate_file_hash()
        
        if current_hash is None:
            return False
            
        if self.last_hash is None:
            self.last_hash = current_hash
            return True  # Erste Ausführung - behandeln als Änderung
            
        if current_hash != self.last_hash:
            self.last_hash = current_hash
            return True
            
        return False
    
    def read_csv_data(self) -> Optional[List[Dict]]:
        """
        Liest die CSV-Datei und gibt die Daten als Liste von Dictionaries zurück
        """
        try:
            if not os.path.exists(self.csv_file_path):
                self.logger.error(f"CSV-Datei nicht gefunden: {self.csv_file_path}")
                return None
                
            df = pd.read_csv(self.csv_file_path)
            
            # Leere Zeilen entfernen
            df = df.dropna(how='all')
            
            # DataFrame zu Liste von Dictionaries konvertieren
            data = df.to_dict('records')
            
            self.logger.info(f"CSV-Datei gelesen: {len(data)} Zeilen")
            return data
            
        except Exception as e:
            self.logger.error(f"Fehler beim Lesen der CSV-Datei: {e}")
            return None
    
    def validate_csv_structure(self, required_columns: List[str]) -> bool:
        """
        Validiert die Struktur der CSV-Datei
        """
        try:
            df = pd.read_csv(self.csv_file_path)
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                self.logger.error(f"Fehlende Spalten in CSV: {missing_columns}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Fehler bei der CSV-Validierung: {e}")
            return False
    
    def get_file_modification_time(self) -> Optional[datetime]:
        """
        Gibt die letzte Änderungszeit der Datei zurück
        """
        try:
            if os.path.exists(self.csv_file_path):
                timestamp = os.path.getmtime(self.csv_file_path)
                return datetime.fromtimestamp(timestamp)
            return None
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen der Änderungszeit: {e}")
            return None
