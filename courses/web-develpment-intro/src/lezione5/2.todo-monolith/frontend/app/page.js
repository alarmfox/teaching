"use client";
import { useState, useEffect } from "react";

export default function TodoMonolith() {
  const [tasks, setTasks] = useState([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const AUTH = btoa("admin:secret");
  const API_URL = "http://localhost:3001";

  async function fetchAPI(endpoint, method = "GET", body = null) {
    const res = await fetch(`${API_URL}${endpoint}`, {
      method,
      headers: {
        Authorization: "Basic " + AUTH,
        "Content-Type": "application/json",
      },
      body: body ? JSON.stringify(body) : null,
    });
    return res.json();
  }

  async function loadTasks() {
    setLoading(true);
    const data = await fetchAPI("/tasks");
    setTasks(data);
    setLoading(false);
  }

  useEffect(() => {
    loadTasks();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!text.trim()) return;
    await fetchAPI("/tasks", "POST", { text });
    setText("");
    loadTasks();
  }

  async function deleteTask(index) {
    await fetchAPI(`/tasks/${index}`, "DELETE");
    loadTasks();
  }

  return (
    <div className="bg-slate-50 min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-6">
        <h1 className="text-3xl font-extrabold text-slate-900 mb-6 tracking-tight">
          Todo Next.js (Monolith)
        </h1>

        {loading && <p className="text-blue-600 mb-4 animate-pulse">Caricamento...</p>}

        <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="flex-grow px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            placeholder="Cosa devi fare?"
          />
          <button className="bg-blue-600 text-white px-5 py-2 rounded-lg font-medium">
            Aggiungi
          </button>
        </form>

        <ul className="space-y-3">
          {tasks.map((t, i) => (
            <li key={i} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100">
              <span className="text-slate-700">{t.text}</span>
              <button onClick={() => deleteTask(i)} className="text-red-500 hover:scale-110 transition">
                Elimina
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
