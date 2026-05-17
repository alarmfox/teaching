import TaskItem from "./TaskItem";

/**
 * TodoList: Gestisce la visualizzazione dell'elenco.
 * Astrae la logica di iterazione (map).
 */
export default function TodoList({ tasks, onItemDelete }) {
  if (tasks.length === 0) {
    return <p className="text-center text-slate-400 py-4">Nessun elemento.</p>;
  }

  return (
    <ul className="space-y-3">
      {tasks.map((t, i) => (
        <TaskItem 
          key={i} 
          text={t.text} 
          onDelete={() => onItemDelete(i)} 
        />
      ))}
    </ul>
  );
}
