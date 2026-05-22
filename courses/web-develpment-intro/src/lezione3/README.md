# Esercitazione: Creazione di un Bot Webex con API REST

In questa esercitazione impareremo a interagire con una Web API reale utilizzando l'autenticazione tramite **Bearer Token**.

## Obiettivo
Interagire con Web API reali (JSONPlaceholder e Webex) utilizzando Python e Node.js.

## Esempio 1: Consumo API Libera (JSONPlaceholder)
Prima di passare a Webex, testiamo la comunicazione con un'API pubblica che non richiede autenticazione.

### Python
Utilizziamo il file `client.py`.
```bash
python client.py
```

### Node.js
Utilizziamo il file `api_test.js` (richiede Node.js 18+).
```bash
node api_test.js
```

## Esempio 2: Creazione di un Bot Webex
In questa parte utilizzeremo l'autenticazione tramite **Bearer Token**.

## Prerequisiti
1. **Python 3.x** installato.
2. Libreria `requests` installata:
   ```bash
   pip install requests
   ```
3. Un account su [Webex Developer](https://developer.webex.com/).

## Step 1: Ottenere il Token
1. Accedi a [developer.webex.com](https://developer.webex.com/).
2. Vai nella sezione **Documentation** -> **APIs** -> **Messages**.
3. Copia il tuo **Personal Access Token** (solitamente visibile nella barra laterale o dopo il login nella documentazione "Try it").
   - *Nota*: Il token personale scade dopo 12 ore. Per un bot permanente, dovresti creare un "Bot Account" nella sezione "My Apps".

## Step 2: Configurazione
Apri il file `bot.py` e modifica le seguenti variabili:
- `ACCESS_TOKEN`: Incolla il token ottenuto nello Step 1.
- `DESTINATARIO`: Inserisci la tua email (per inviarti un messaggio diretto) o quella di un compagno.

## Step 3: Esecuzione
Esegui lo script dal terminale:
```bash
python bot.py
```

## Sfida Extra
Modifica lo script per:
1. Chiedere all'utente di inserire il testo del messaggio tramite la funzione `input()`.
2. Recuperare gli ultimi messaggi ricevuti utilizzando il metodo `GET` sull'endpoint `/v1/messages`.
