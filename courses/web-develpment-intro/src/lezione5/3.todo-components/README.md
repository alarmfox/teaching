# Step 3: Rifattorizzazione Professionale

In questo esempio applichiamo i principi di **Clean Code** e **Singola Responsabilità** (Single Responsibility Principle).

## Cosa imparerai
1. **Component Abstraction**: Abbiamo spostato la visualizzazione dei singoli task in `components/TaskItem.js` e della lista in `components/TodoList.js`.
2. **Props**: Come passare dati dal componente genitore (`page.js`) ai componenti figli.
3. **useCallback**: Per memorizzare la funzione di cancellazione ed evitare rendering non necessari.
4. **Tailwind Avanzato**: Uso di stati `hover` e transizioni per rendere la UI più fluida.

## Perché farlo?
Scomponendo l'app, il componente principale `page.js` diventa molto più pulito e si occupa solo di gestire lo **stato** e la **comunicazione con le API**, delegando la visualizzazione ai sotto-componenti.
