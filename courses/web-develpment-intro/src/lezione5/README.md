# Lezione 5: I Framework Frontend Moderni

In questa cartella troverete gli esempi pratici per passare dalla programmazione imperativa a quella dichiarativa con **Next.js** e **React**.

## Struttura della Lezione (Percorso Evolutivo)
1.  `1.hello-world/`: Struttura base dell'App Router e sintassi JSX.
2.  `2.todo-monolith/`: La Todo App implementata in un **unico file**. Mostra come gestire stato (`useState`), effetti (`useEffect`) e filtraggio in modo semplice ma disordinato.
3.  `3.todo-components/`: La versione **professionale** del progetto precedente. Applichiamo l'astrazione in componenti (`TodoList`, `TaskItem`) e ottimizziamo con `useCallback`.
4.  `4.api-routes/`: Esempio di backend integrato direttamente in Next.js.

## Come iniziare
Per ogni esempio:
```bash
npm install
npm run dev
```
L'applicazione sarà visualizzabile su `http://localhost:3000`.
