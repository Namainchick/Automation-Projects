import os
import base64
import streamlit as st
from openai import OpenAI

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Gmail: nur Lesezugriff
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


# --- Hilfsfunktionen für Auth ---
def load_token_if_exists():
    """Lädt gespeicherte Credentials, falls vorhanden."""
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        return creds
    return None


def refresh_creds(creds):
    """Erneuert abgelaufene Credentials."""
    creds.refresh(Request())
    with open('token.json', 'w') as f:
        f.write(creds.to_json())
    return creds


def get_new_creds():
    """Startet neuen Login-Flow über Browser."""
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as f:
        f.write(creds.to_json())
    return creds


# --- Mail-Funktion ---
def fetch_last_mails(creds, n=5):
    """Holt die letzten n Mails als (subject, body)-Liste."""
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', maxResults=n).execute()
    messages = results.get('messages', [])

    mails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = msg_data.get("payload")
        headers = payload.get("headers")

        # Betreff
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(Ohne Betreff)")

        # Body extrahieren
        body = ""
        if payload.get("body") and payload["body"].get("data"):
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
        elif payload.get("parts"):
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain" and part.get("body") and part["body"].get("data"):
                    body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                    break

        mails.append((subject, body))
    return mails


# --- OpenAI ---
def summarize_mails(mails):
    """Fasst die Mails mit OpenAI zusammen."""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    joined_text = "\n\n".join([f"Betreff: {s}\nInhalt: {b}" for s, b in mails])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Fasse die folgenden E-Mails kurz und prägnant zusammen."},
            {"role": "user", "content": joined_text}
        ]
    )

    return response.choices[0].message.content


# --- Streamlit App ---
def main():
    st.title("📧 Gmail Summarizer")

    # Session-State initialisieren
    if "creds" not in st.session_state:
        st.session_state["creds"] = None
    if "summary" not in st.session_state:
        st.session_state["summary"] = ""

    # Buttons für Login
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Token laden", key="load_token"):
            creds = load_token_if_exists()
            if creds:
                if creds.expired and creds.refresh_token:
                    creds = refresh_creds(creds)
                st.session_state["creds"] = creds
                st.success("Token geladen ✅")
            else:
                st.warning("Keine gespeicherte token.json gefunden ❌")
    with col2:
        if st.button("🌐 Neu anmelden", key="new_login"):
            st.session_state["creds"] = get_new_creds()
            st.success("Neuer Login erfolgreich ✅")

    # Guard: ohne Creds stoppen
    if not st.session_state["creds"]:
        st.info("Bitte zuerst Zugangsdaten laden oder neu anmelden.")
        st.stop()

    # Zusammenfassung erzeugen
    if st.button("📄 Zusammenfassung erstellen", key="summarize"):
        mails = fetch_last_mails(st.session_state["creds"], n=5)
        if not mails:
            st.warning("Keine Nachrichten gefunden.")
        else:
            summary = summarize_mails(mails)
            st.session_state["summary"] = summary

    # Ausgabe
    if st.session_state["summary"]:
        st.subheader("Zusammenfassung")
        st.text_area("Ergebnis", value=st.session_state["summary"], height=300, disabled=True)


if __name__ == "__main__":
    main()
