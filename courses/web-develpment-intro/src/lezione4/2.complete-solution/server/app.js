const express = require('express');
const basicAuth = require('express-basic-auth');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

const FILE_PATH = './tasks.json';

// Inizializzazione dati in memoria dal file
let tasks = [];
if (fs.existsSync(FILE_PATH)) {
    tasks = JSON.parse(fs.readFileSync(FILE_PATH));
} else {
    fs.writeFileSync(FILE_PATH, JSON.stringify([]));
}

// Auth Middleware
app.use(basicAuth({
    users: { 'admin': 'secret' },
    challenge: true
}));

// Operazioni CRUD (In-Memory)
app.get('/tasks', async (req, res) => {
    // Simula latenza di rete (2 secondi)
    await new Promise(resolve => setTimeout(resolve, 2000));
    res.json(tasks);
});

app.post('/tasks', (req, res) => {
    tasks.push(req.body);
    res.status(201).json({ status: "created" });
});

app.delete('/tasks/:id', (req, res) => {
    tasks.splice(req.params.id, 1);
    res.json({ status: "deleted" });
});

app.post('/save', (req, res) => {
    fs.writeFileSync(FILE_PATH, JSON.stringify(tasks, null, 4));
    res.json({ status: "saved" });
});

app.post('/reset', (req, res) => {
    tasks = [];
    fs.writeFileSync(FILE_PATH, JSON.stringify([]));
    res.json({ status: "reset" });
});

app.use(express.static(path.join(__dirname, '..')));


app.listen(3000, () => console.log('Server in ascolto su porta 3000'));
