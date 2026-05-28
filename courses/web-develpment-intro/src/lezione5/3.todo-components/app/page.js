"use client";
import { useState, useEffect, useCallback } from "react";

// Sotto-componente per il singolo Task
// Usiamo React.memo (opzionale qui) o semplicemente lo definiamo fuori
const TaskItem = ({ task, onRemove }) => (
  <li className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100 hover:border-blue-200 transition">
    <span className="text-slate-700 font-medium">{task.text}</span>
    <button 
      onClick={onRemove}
      className="text-red-500 hover:scale-110 transition"
    >
      Elimina
    </button>
  </li>
);

// Sotto-componente per il Form
const TodoForm = ({ onAdd }) => {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    onAdd(text);
    setText("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="flex-grow px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        placeholder="Cosa devi fare?"
      />
      <button className="bg-blue-600 text-white px-5 py-2 rounded-lg font-medium active:scale-95 transition">
        Aggiungi
      </button>
    </form>
  );
};

export default function TodoComponents() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);

  const AUTH = btoa("admin:secret");
  const API_URL = "http://localhost:3001";

  const fetchAPI = useCallback(async (endpoint, method = "GET", body = null) => {
    const res = await fetch(`${API_URL}${endpoint}`, {
      method,
      headers: {
        Authorization: "Basic " + AUTH,
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : null,
    }, [AUTH]); // Dipendenza su AUTH
    return res.json();
  }, [AUTH]);

  const loadTasks = useCallback(async () => {
    setLoading(true);
    const data = await fetchAPI("/tasks");
    setTasks(data);
    setLoading(false);
  }, [fetchAPI]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  const addTask = async (text) => {
    await fetchAPI("/tasks", "POST", { text });
    loadTasks();
  };

  const deleteTask = async (index) => {
    await fetchAPI(`/tasks/${index}`, "DELETE");
    loadTasks();
  };

  return (
    <div className="bg-slate-50 min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-6">
        <h1 className="text-3xl font-extrabold text-slate-900 mb-6">
          Todo App (Componenti)
        </h1>

        {loading && <p className="text-blue-600 mb-4 animate-pulse">Caricamento...</p>}

        <TodoForm onAdd={addTask} />

        <ul className="space-y-3">
          {tasks.map((t, i) => (
            <TaskItem key={i} task={t} onRemove={() => deleteTask(i)} />
          ))}
          {!loading && tasks.length === 0 && (
            <p className="text-center text-slate-400 italic">Nessun task presente.</p>
          )}
        </ul>
      </div>
    </div>
  );
}
