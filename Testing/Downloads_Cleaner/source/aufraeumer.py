import os
import shutil

ordner_dict = {
    "bilder": {
        "pfad": None,
        "endungen": (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp")
    },
    "dokumente": {
        "pfad": None,
        "endungen": (".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".odt")
    },
    "audios": {
        "pfad": None,
        "endungen": (".mp3", ".wav", ".flac", ".aac", ".ogg")
    },
    "videos": {
        "pfad": None,
        "endungen": (".mp4", ".mov", ".avi", ".mkv", ".wmv", ".webm")
    },
    "archive": {
        "pfad": None,
        "endungen": (".zip", ".rar", ".7z", ".tar", ".gz")
    },
    "programme": {
        "pfad": None,
        "endungen": (".exe", ".msi", ".dmg", ".pkg", ".deb", ".apk")
    },
    "sonstige": {  
        "pfad": None,
        "endungen": ()  
    }
}

downloads_ordner = "/Users/namanhbui/download_probe"

def ordner_erstellen():
    for schluessel in ordner_dict:
        ordner_dict[schluessel]["pfad"] = os.path.join(downloads_ordner, schluessel)
        os.makedirs(ordner_dict[schluessel]["pfad"], exist_ok=True)

def datei_zuordnen():
    for schluessel in ordner_dict:
        for datei_name in os.listdir(downloads_ordner): 
            if datei_name.endswith(ordner_dict[schluessel]["endungen"]):
                quell_pfad = os.path.join(downloads_ordner, datei_name)
                ziel_pfad = os.path.join(ordner_dict[schluessel]["pfad"], datei_name)
                shutil.move(quell_pfad, ziel_pfad)
                

ordner_erstellen()
datei_zuordnen()