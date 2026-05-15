// Selettori degli oggetti DOM
const input = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const list = document.getElementById('todoList');

// Stato dell'applicazione: array di oggetti
// Cerchiamo di caricare i dati dal localStorage all'avvio
let tasks = JSON.parse(localStorage.getItem('myTasks')) || [];

// Funzione per salvare lo stato nel browser
function saveTasks() {
    localStorage.setItem('myTasks', JSON.stringify(tasks));
}

// Funzione per renderizzare (Read) la lista basandosi sull'array
function renderTasks() {
    list.innerHTML = ''; // Svuotiamo la lista visuale
    
    tasks.forEach((task, index) => {
        const li = document.createElement('li');
        if (task.completed) li.classList.add('completed');
        
        li.innerHTML = `
            <span onclick="toggleTask(${index})">${task.text}</span>
            <span class="delete-btn" onclick="deleteTask(${index})">X</span>
        `;
        list.appendChild(li);
    });
}

// Operazione: Create
addBtn.addEventListener('click', () => {
    const text = input.value.trim();
    if (text) {
        tasks.push({ text: text, completed: false });
        input.value = '';
        saveTasks();
        renderTasks();
    }
});

// Operazione: Update
window.toggleTask = (index) => {
    tasks[index].completed = !tasks[index].completed;
    saveTasks();
    renderTasks();
};

// Operazione: Delete
window.deleteTask = (index) => {
    tasks.splice(index, 1);
    saveTasks();
    renderTasks();
};

// Primo render all'avvio
renderTasks();
