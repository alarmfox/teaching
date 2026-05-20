# Esempio SSR (Server-Side Rendering) con Flask

Questo esempio mostra come creare una semplice applicazione Todo utilizzando il pattern SSR. 
A differenza della versione Vanilla JS, qui il codice HTML viene generato sul server e inviato al browser già "pronto".

## Come avviarlo
1. Assicurati di avere Python installato.
2. Installa le dipendenze: `pip install -r requirements.txt`
3. Avvia l'applicazione: `python main.py`
4. Apri il browser su `http://127.0.0.1:5000`

## Concetti Chiave
- **Template Engine**: Usiamo **Jinja2** (integrato in Flask) per inserire dati dinamici nell'HTML.
- **Form Handling**: I nuovi task vengono inviati tramite un form HTML standard con metodo `POST`.
- **Routing**: Ogni azione (aggiungi, toggle) corrisponde a una specifica rotta sul server che reindirizza poi alla home.
- **Styling**: Usiamo **Tailwind CSS** (via CDN) per una UI moderna e responsiva senza scrivere CSS custom.

## Esercizio per lo Studente
L'applicazione è incompleta! Manca la funzionalità di eliminazione delle task.
1. In `main.py`, implementa la funzione `delete_task(task_id)` e aggiungi la rotta `@app.route('/delete/<int:task_id>')`.
2. In `templates/template.html`, modifica il link di eliminazione per puntare alla nuova rotta utilizzando `url_for`.
