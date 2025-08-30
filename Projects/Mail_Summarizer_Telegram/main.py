import os
import requests
from mail_utils import (
    load_token_if_exists,
    refresh_creds,
    get_new_creds,
    fetch_last_mails,
    summarize_mails,
)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, data=data)
    print(r.json())

def main():
    # Credentials laden oder neu holen
    creds = load_token_if_exists()
    if creds:
        if creds.expired and creds.refresh_token:
            creds = refresh_creds(creds)
    else:
        creds = get_new_creds()

    # Wenn immer noch keine Credentials da sind -> abbrechen
    if not creds:
        send_telegram("⚠️ Emails konnten nicht geladen werden (keine gültigen Credentials).")
        return

    # Letzte Mails holen
    mails = fetch_last_mails(creds, n=5)

    if not mails:
        message = "📭 Keine neuen E-Mails gefunden."
    else:
        message = summarize_mails(mails)

    # Nachricht an Telegram senden
    send_telegram(message)

if __name__ == "__main__":
    main()