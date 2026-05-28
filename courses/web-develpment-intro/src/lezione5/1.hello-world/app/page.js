export default function Home() {
  // Dati costanti (simulano una risposta da un database o API)
  const features = [
    { id: 1, title: "Componenti", desc: "Dividi la UI in pezzi riutilizzabili.", color: "text-blue-600" },
    { id: 2, title: "Stato & Hook", desc: "Gestisci i dati con useState e useEffect.", color: "text-green-600" },
    { id: 3, title: "Tailwind CSS", desc: "Stilizza velocemente con classi di utilità.", color: "text-purple-600" },
    { id: 4, title: "Next.js Router", desc: "Navigazione fluida basata su file system.", color: "text-orange-600" }
  ];

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-slate-50 text-slate-900">
      <div className="max-w-4xl w-full text-center">
        <h1 className="text-4xl font-extrabold text-slate-800 tracking-tight mb-4">
          Benvenuti alla Lezione 5
        </h1>
        <p className="text-lg text-slate-600 mb-12">
          Esempio di rendering dinamico utilizzando <code className="bg-slate-200 px-1 rounded">array.map()</code> in JSX.
        </p>

        {/* ESEMPIO ARRAY.MAP */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {features.map((item) => (
            <div 
              key={item.id} 
              className="p-6 bg-white rounded-xl shadow-sm border border-slate-200 hover:border-blue-300 transition-colors text-left"
            >
              <h2 className={`text-lg font-bold mb-2 ${item.color}`}>
                {item.title}
              </h2>
              <p className="text-sm text-slate-500">
                {item.desc}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-16 text-sm text-slate-400">
          Modifica <code className="font-mono">app/page.js</code> per aggiungere nuovi elementi all'array!
        </div>
      </div>
    </main>
  );
}
