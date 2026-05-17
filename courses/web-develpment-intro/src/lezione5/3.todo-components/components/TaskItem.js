/**
 * TaskItem: Componente atomico per visualizzare il singolo elemento.
 * Riceve i dati e le funzioni di gestione tramite PROPS.
 */
export default function TaskItem({ text, onDelete }) {
  return (
    <li className="flex justify-between items-center p-3 bg-gray-50 rounded border border-transparent hover:border-blue-200 transition">
      <span className="text-slate-700">{text}</span>
      <button 
        onClick={onDelete}
        className="text-red-400 hover:text-red-600 transition"
      >
        Elimina
      </button>
    </li>
  );
}
