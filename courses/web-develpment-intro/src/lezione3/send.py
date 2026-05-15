import requests
import sys

# --- CONFIGURAZIONE ---
# Inserisci qui il tuo Personal Access Token da developer.webex.com
ACCESS_TOKEN = "IL_TUO_TOKEN_QUI"

# ID della stanza o email del destinatario
# Suggerimento: Per testare, usa la tua stessa email per scriverti in "Direct Message"
DESTINATARIO = "email@esempio.com"


def invia_messaggio(testo):
    """
    Invia un messaggio tramite le API di Webex.
    Documentazione: https://developer.webex.com/docs/api/v1/messages/create-a-message
    """
    url = "https://webexapis.com/v1/messages"

    # Headers per l'autenticazione Bearer
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    # Payload della richiesta
    payload = {"toPersonEmail": DESTINATARIO, "text": testo}

    try:
        print(f"Tentativo di invio messaggio a {DESTINATARIO}...")
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        # Verifica se la richiesta ha avuto successo (2xx)
        response.raise_for_status()

        print("Messaggio inviato con successo!")
        print(f"ID Messaggio: {response.json().get('id')}")

    except requests.exceptions.HTTPError as err:
        print(f"Errore HTTP: {err}")
        if response.status_code == 401:
            print("Verifica che il tuo ACCESS_TOKEN sia corretto e non scaduto.")
    except Exception as e:
        print(f"Errore imprevisto: {e}")


if __name__ == "__main__":
    if ACCESS_TOKEN == "IL_TUO_TOKEN_QUI":
        print("ERRORE: Devi configurare il tuo ACCESS_TOKEN nel file.")
        sys.exit(1)

    messaggio_test = (
        "Ciao! Questo e un messaggio inviato tramite il mio primo Bot Webex in Python."
    )
    invia_messaggio(messaggio_test)
