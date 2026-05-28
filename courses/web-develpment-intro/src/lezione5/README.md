# Lezione 5: Modern Frontend Frameworks (Next.js)

Questa cartella contiene gli esempi pratici per la transizione da Vanilla JS a React/Next.js.

## Struttura degli esempi

1.  **`1.hello-world/`**: Introduzione alla sintassi JSX e alla struttura di una pagina Next.js.
2.  **`2.todo-monolith/`**: Implementazione della Todo App in un singolo componente. Comunica con il backend esterno (Express o Flask).
3.  **`3.todo-components/`**: Rifattorizzazione dell'esempio precedente in componenti riutilizzabili e ottimizzazione con `useCallback`.
4.  **`4.api-routes/`**: Applicazione Full-stack completa dove anche il backend è gestito da Next.js tramite le API Routes.

## Come avviare i progetti Next.js

Ogni cartella è un progetto Next.js indipendente. Per avviarlo:

1.  Entra nella cartella: `cd 1.hello-world` (o le altre)
2.  Installa le dipendenze: `npm install`
3.  Avvia il server di sviluppo: `npm run dev`
4.  Apri [http://localhost:3000](http://localhost:3000) nel browser.

## Backend per l'esempio 2 e 3

Gli esempi 2 e 3 richiedono il backend della Lezione 4 attivo. Puoi trovare una copia del backend Express in `2.todo-monolith/backend`. Ricorda di avviarlo su una porta diversa (es. 3001) se necessario, o configurare il CORS.
