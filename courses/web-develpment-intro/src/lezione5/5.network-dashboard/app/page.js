"use client";
import { useState, useEffect } from "react";

/**
 * Dashboard di Rete (Lezione 5) - Versione Completa
 * Include: Visualizzazione, Creazione, Cancellazione e Download Configurazione.
 */
export default function NetworkDashboard() {
  const [routers, setRouters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Stato per il form di creazione
  const [newHostname, setNewHostname] = useState("");

  const API_URL = "http://localhost:3005";

  // 1. Carica la lista dei router
  async function loadData() {
    try {
      setLoading(true);
      const res = await fetch(`${API_URL}/routers`);
      if (!res.ok) throw new Error("Server non raggiungibile");
      const data = await res.json();
      setRouters(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  // 2. Aggiunge un nuovo router (con un'interfaccia di default)
  async function addRouter(e) {
    e.preventDefault();
    if (!newHostname.trim()) return;

    const routerData = {
      hostname: newHostname,
      interfaces: [
        { name: "GigabitEthernet0", ip: "192.168.1.1", netmask: "255.255.255.0", description: "Default LAN" }
      ]
    };

    try {
      const res = await fetch(`${API_URL}/routers`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(routerData)
      });
      if (res.ok) {
        setNewHostname("");
        loadData();
      }
    } catch (err) {
      alert("Errore durante l'aggiunta");
    }
  }

  // 3. Rimuove un router
  async function deleteRouter(id) {
    if (!confirm("Sei sicuro di voler eliminare questo apparato?")) return;
    try {
      const res = await fetch(`${API_URL}/routers/${id}`, { method: "DELETE" });
      if (res.ok) loadData();
    } catch (err) {
      alert("Errore durante la cancellazione");
    }
  }

  // 4. Scarica la configurazione come file .txt
  async function downloadConfig(id, hostname) {
    try {
      const res = await fetch(`${API_URL}/routers/${id}/config`);
      const text = await res.text();
      
      // Creazione del file per il download
      const blob = new Blob([text], { type: "text/plain" });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${hostname}_config.txt`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Errore durante il download della configurazione");
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      <nav className="bg-indigo-700 text-white p-4 shadow-md">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold flex items-center gap-2">
            <span className="bg-white text-indigo-700 px-2 py-0.5 rounded text-sm font-black">NET</span>
            Network Inventory
          </h1>
          <button onClick={loadData} className="text-sm bg-indigo-500 px-3 py-1 rounded hover:bg-indigo-400 transition">
            Aggiorna
          </button>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto p-6">
        
        {/* Form Aggiunta */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 mb-8">
          <h2 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Aggiungi Nuovo Apparato</h2>
          <form onSubmit={addRouter} className="flex gap-4">
            <input 
              type="text" 
              placeholder="Hostname del router..." 
              value={newHostname}
              onChange={(e) => setNewHostname(e.target.value)}
              className="flex-grow border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
            />
            <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-indigo-700 transition">
              Aggiungi
            </button>
          </form>
        </div>

        {loading && <div className="text-center py-10 text-slate-500 animate-pulse">Caricamento...</div>}
        
        {error && <div className="bg-red-50 text-red-700 p-4 rounded-lg mb-8 border border-red-200">{error}</div>}

        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {routers.map((router) => (
              <div key={router.id} className="bg-white border border-slate-200 rounded-xl shadow-sm flex flex-col">
                <div className="bg-slate-50 p-4 border-b border-slate-200 flex justify-between items-center">
                  <h2 className="text-lg font-bold text-indigo-900">{router.hostname}</h2>
                  <button 
                    onClick={() => deleteRouter(router.id)}
                    className="text-red-400 hover:text-red-600 text-xs font-bold uppercase"
                  >
                    Elimina
                  </button>
                </div>
                
                <div className="p-4 flex-grow">
                  <div className="space-y-3">
                    {router.interfaces.map((iface, idx) => (
                      <div key={idx} className="flex justify-between items-center text-sm border-b border-slate-50 pb-2">
                        <span className="font-semibold text-slate-700">{iface.name}</span>
                        <code className="text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded font-mono text-xs">{iface.ip}</code>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="p-3 bg-slate-50 border-t border-slate-100 flex justify-between">
                   <span className="text-[10px] text-slate-400 flex items-center">ID: {router.id}</span>
                   <button 
                    onClick={() => downloadConfig(router.id, router.hostname)}
                    className="text-xs font-bold text-indigo-600 hover:underline"
                   >
                    Scarica Config .txt
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
