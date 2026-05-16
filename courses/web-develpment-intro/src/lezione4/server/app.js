const express = require('express');
const basicAuth = require('express-basic-auth');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

const FILE_PATH = './tasks.json';

// Inizializzazione file se non esiste
if (!fs.existsSync(FILE_PATH)) {
    fs.writeFileSync(FILE_PATH, JSON.stringify([]));
}

// Auth Middleware
app.use(basicAuth({ 
    users: { 'admin': 'secret' }, 
    challenge: true 
}));

// Operazioni CRUD
app.get('/tasks', (req, res) => {
    const tasks = JSON.parse(fs.readFileSync(FILE_PATH));
    res.json(tasks);
});

app.post('/tasks', (req, res) => {
    const tasks = JSON.parse(fs.readFileSync(FILE_PATH));
    tasks.push(req.body);
    res.status(201).json({ status: "created" });
});

app.delete('/tasks/:id', (req, res) => {
    let tasks = JSON.parse(fs.readFileSync(FILE_PATH));
    tasks.splice(req.params.id, 1);
    res.json({ status: "deleted" });
});

app.use(express.static(path.join(__dirname, '..')));


app.listen(3000, () => console.log('Server in ascolto su porta 3000'));
