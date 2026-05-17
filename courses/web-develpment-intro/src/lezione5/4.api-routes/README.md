# Step 4: API Routes (Unified Full-Stack)

Next.js permette di integrare la logica backend direttamente nel progetto.

## Cosa osservare
-   La cartella `app/api/`: Ogni file `route.js` all'interno di una sottocartella definisce un endpoint HTTP (es. `/api/hello`).
-   In questo esempio mostriamo come restituire un JSON statico o generato dinamicamente.

## Vantaggio
Usando le API Routes, il tuo frontend React e il tuo backend vivono nello stesso dominio e porta. Questo elimina completamente la necessità di configurare il **CORS**.
