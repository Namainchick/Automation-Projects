import json
import logging
from typing import Dict, List, Optional

try:
    import requests
except ImportError:
    print("❌ requests nicht installiert. Installieren Sie es mit: pip install requests")
    raise

try:
    from decouple import config
except ImportError:
    print("⚠️ python-decouple nicht verfügbar. Verwende Umgebungsvariablen.")
    import os
    def config(key, default=None):
        return os.getenv(key, default)

class ShopwareAPI:
    """
    Klasse für die Kommunikation mit der Shopware API
    """
    
    def __init__(self):
        self.base_url = config('SHOPWARE_URL')
        self.username = config('SHOPWARE_API_USERNAME')
        self.password = config('SHOPWARE_API_PASSWORD')
        self.access_token = None
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Logger konfigurieren
        self.logger = logging.getLogger(__name__)
        
    def authenticate(self) -> bool:
        """
        Authentifizierung bei der Shopware API
        """
        auth_url = f"{self.base_url}/api/oauth/token"
        auth_data = {
            "grant_type": "password",
            "client_id": "administration",
            "username": self.username,
            "password": self.password
        }
        
        try:
            response = requests.post(auth_url, json=auth_data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            
            if self.access_token:
                self.headers['Authorization'] = f'Bearer {self.access_token}'
                self.logger.info("Erfolgreich bei Shopware API authentifiziert")
                return True
            else:
                self.logger.error("Keine Access Token erhalten")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Fehler bei der Authentifizierung: {e}")
            return False
    
    def get_product_by_number(self, product_number: str) -> Optional[Dict]:
        """
        Sucht ein Produkt anhand der Produktnummer
        """
        if not self.access_token:
            if not self.authenticate():
                return None
        
        search_url = f"{self.base_url}/api/search/product"
        search_data = {
            "filter": [
                {
                    "type": "equals",
                    "field": "productNumber",
                    "value": product_number
                }
            ]
        }
        
        try:
            response = requests.post(search_url, json=search_data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            products = result.get('data', [])
            
            if products:
                return products[0]
            else:
                self.logger.warning(f"Produkt mit Nummer {product_number} nicht gefunden")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Fehler beim Suchen des Produkts {product_number}: {e}")
            return None
    
    def update_product(self, product_id: str, product_data: Dict) -> bool:
        """
        Aktualisiert ein Produkt in Shopware
        """
        if not self.access_token:
            if not self.authenticate():
                return False
        
        update_url = f"{self.base_url}/api/product/{product_id}"
        
        try:
            response = requests.patch(update_url, json=product_data, headers=self.headers)
            response.raise_for_status()
            
            self.logger.info(f"Produkt {product_id} erfolgreich aktualisiert")
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Fehler beim Aktualisieren des Produkts {product_id}: {e}")
            return False
    
    def create_product(self, product_data: Dict) -> Optional[str]:
        """
        Erstellt ein neues Produkt in Shopware
        """
        if not self.access_token:
            if not self.authenticate():
                return None
        
        create_url = f"{self.base_url}/api/product"
        
        try:
            response = requests.post(create_url, json=product_data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            product_id = result.get('data', {}).get('id')
            
            if product_id:
                self.logger.info(f"Neues Produkt erstellt mit ID: {product_id}")
                return product_id
            else:
                self.logger.error("Keine Produkt-ID nach Erstellung erhalten")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Fehler beim Erstellen des Produkts: {e}")
            return False
    
    def sync_product_from_csv_data(self, csv_row: Dict) -> bool:
        """
        Synchronisiert ein Produkt basierend auf CSV-Daten
        """
        product_number = csv_row.get('product_number')
        if not product_number:
            self.logger.error("Keine Produktnummer in CSV-Zeile gefunden")
            return False
        
        # Produkt in Shopware suchen
        existing_product = self.get_product_by_number(product_number)
        
        # Produktdaten aus CSV vorbereiten
        product_data = self._prepare_product_data(csv_row)
        
        if existing_product:
            # Produkt existiert - aktualisieren
            product_id = existing_product.get('id')
            return self.update_product(product_id, product_data)
        else:
            # Neues Produkt erstellen
            product_id = self.create_product(product_data)
            return product_id is not None
    
    def _prepare_product_data(self, csv_row: Dict) -> Dict:
        """
        Bereitet Produktdaten für die Shopware API vor
        """
        # Hier können Sie die Zuordnung zwischen CSV-Spalten und Shopware-Feldern anpassen
        product_data = {
            "productNumber": csv_row.get('product_number'),
            "name": csv_row.get('name'),
            "description": csv_row.get('description'),
            "price": [
                {
                    "currencyId": "b7d2554b0ce847cd82f3ac9bd1c0dfca",  # EUR (Standard Currency ID)
                    "gross": float(csv_row.get('price', 0)),
                    "net": float(csv_row.get('price', 0)) / 1.19,  # Annahme: 19% MwSt
                    "linked": True
                }
            ],
            "stock": int(csv_row.get('stock', 0)),
            "taxId": "f5c428b9cd2e455b9b2d3c9b9d9f1c85",  # Standard Tax ID (19%)
            "active": csv_row.get('active', 'true').lower() == 'true'
        }
        
        # Zusätzliche Felder können hier hinzugefügt werden
        if csv_row.get('weight'):
            product_data['weight'] = float(csv_row.get('weight'))
        
        if csv_row.get('ean'):
            product_data['ean'] = csv_row.get('ean')
        
        return product_data
