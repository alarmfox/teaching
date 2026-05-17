"use client";
import { useState, useEffect, useCallback } from "react";
import TodoList from "../components/TodoList";

/**
 * Page Principale: Gestisce lo STATO e la LOGICA di alto livello.
 * Utilizza componenti astratti per visualizzare i dati.
 */
export default function ComponentTodo() {
  const [tasks, setTasks] = useState([]);
  const [search, setSearch] = useState("");

  // Fetching dati (Stessa logica, ma separata dalla UI)
  useEffect(() => {
    fetch("http://localhost:3000/tasks", {
      headers: { "Authorization": "Basic " + btoa("admin:secret") }
    })
    .then(res => res.json())
    .then(data => setTasks(data));
  }, []);

  // Rimozione task memorizzata con useCallback per ottimizzare le performance
  const handleDelete = useCallback((index) => {
    setTasks(prev => prev.filter((_, i) => i !== index));
  }, []);

  const filteredTasks = tasks.filter(t => 
    t.text.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <main className="max-w-md mx-auto mt-10 p-6 bg-white rounded-2xl shadow-xl">
      <h1 className="text-3xl font-extrabold text-slate-800 mb-6">Pro Todo</h1>
      
      <input 
        type="text"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        placeholder="Cerca..."
        className="w-full p-3 border border-slate-200 rounded-xl mb-6 focus:ring-2 focus:ring-blue-500 focus:outline-none"
      />

      <TodoList tasks={filteredTasks} onItemDelete={handleDelete} />
    </main>
  );
}
