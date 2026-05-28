"use client";
import { useState, useEffect } from "react";

export default function FullstackTodo() {
  const [tasks, setTasks] = useState([]);
  const [text, setText] = useState("");

  const loadTasks = async () => {
    const res = await fetch("/api/tasks");
    const data = await res.json();
    setTasks(data);
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const addTask = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    await fetch("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ text }),
    });
    setText("");
    loadTasks();
  };

  const deleteTask = async (index) => {
    await fetch(`/api/tasks/${index}`, { method: "DELETE" });
    loadTasks();
  };

  return (
    <div className="bg-slate-50 min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-6">
        <h1 className="text-3xl font-extrabold text-slate-900 mb-6 tracking-tight">Todo Full-stack</h1>
        <form onSubmit={addTask} className="flex gap-2 mb-6">
          <input 
            value={text} 
            onChange={e => setText(e.target.value)}
            className="flex-grow px-4 py-2 border border-slate-200 rounded-lg focus:ring-2 focus:ring-green-500 outline-none transition"
            placeholder="Nuovo task..."
          />
          <button className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-lg font-medium transition active:scale-95">
            Aggiungi
          </button>
        </form>
        <ul className="space-y-3 mb-6">
          {tasks.map((t, i) => (
            <li key={i} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100 hover:border-green-200 transition">
              <span className="text-slate-700 font-medium">{t.text}</span>
              <button onClick={() => deleteTask(i)} className="text-slate-400 hover:text-red-500 transition">
                Elimina
              </button>
            </li>
          ))}
          {tasks.length === 0 && (
            <p className="text-center text-slate-400 italic py-4">Nessun task per ora.</p>
          )}
        </ul>
        <div className="p-4 bg-blue-50 rounded-xl border border-blue-100">
          <p className="text-sm text-blue-800 italic">
            <strong>Nota:</strong> Questa applicazione è full-stack. Il backend è integrato in Next.js tramite le API Routes!
          </p>
        </div>
      </div>
    </div>
  );
}
