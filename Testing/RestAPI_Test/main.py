import requests
import pandas as pd

links = []

def download_image(image_url: str, timeout: int = 30):
    """
    Lädt ein Bild von einer URL herunter
    
    Args:
        image_url: URL des Bildes
        timeout: Timeout in Sekunden
        
    Returns:
        Tuple (success, image_data, content_type)
    """
    try:
        response = requests.get(
            image_url, 
            timeout=timeout,
            headers={'User-Agent': 'Shopware Media Importer 1.0'}
        )
        response.raise_for_status()
        
        # Content-Type bestimmen
        content_type = response.headers.get('content-type', 'image/jpeg')
        if not content_type.startswith('image/'):
            content_type = 'image/jpeg'
        
        return True, response.content, content_type
        
    except Exception as e:
        print(f"Fehler beim Download von {image_url}: {e}")
        return False, b'', ''
        
        


# Reload the CSV file
file_path = "moin.csv"
df = pd.read_csv(file_path)

# Extract the first 100 links from the 'merchant_image_url' column as strings
if "aw_image_url" in df.columns:
    # Filter for terracanis DE merchant and get their image URLs
    terracanis_df = df[df['merchant_name'] == "terracanis DE"]
    if not terracanis_df.empty:
        links = terracanis_df["aw_image_url"].dropna().astype(str).head(100).tolist()
    else:
        # If no terracanis DE found, get all merchant image URLs
        links = df["aw_image_url"].dropna().astype(str).head(100).tolist()
else:
    print("Column 'aw_image_url' not found in CSV")


if __name__ == "__main__":
    for link in links[:20]:
        download_image(link)