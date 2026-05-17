"use client";
import { useState, useEffect } from "react";

/**
 * Esempio Monolitico: Tutto lo stato e la logica sono in un unico file.
 * Utile per capire le basi, ma difficile da mantenere.
 */
export default function MonolithicTodo() {
  const [tasks, setTasks] = useState([]);
  const [search, setSearch] = useState("");

  // Caricamento dati (Lezione 4 Backend)
  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch("http://localhost:3000/tasks", {
          headers: { "Authorization": "Basic " + btoa("admin:secret") }
        });
        const data = await res.json();
        setTasks(data);
      } catch (e) {
        console.error("Errore fetch:", e);
      }
    };
    load();
  }, []);

  // Stato derivato per il filtro
  const filteredTasks = tasks.filter(t => 
    t.text.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <main className="max-w-md mx-auto mt-10 p-6 bg-white rounded-xl shadow-lg">
      <h1 className="text-2xl font-bold mb-4">Todo App (Monolith)</h1>

      <input
        type="text"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Cerca tra i task..."
        className="w-full p-2 border border-gray-300 rounded mb-4"
      />

      <ul className="space-y-2">
        {filteredTasks.map((t, i) => (
          <li key={i} className="flex justify-between items-center p-3 bg-gray-50 rounded">
            <span>{t.text}</span>
            <button
              onClick={() => setTasks(tasks.filter((_, index) => index !== i))}
              className="text-red-500 hover:text-red-700 font-bold"
            >
              &times;
            </button>
          </li>
        ))}
      </ul>

      {filteredTasks.length === 0 && (
        <p className="text-center text-gray-400 mt-4 italic">Nessun task trovato.</p>
      )}
    </main>
  );
}
