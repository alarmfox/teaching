document.getElementById('myForm').addEventListener('submit', (e) => {
    // Modularità: il codice JS è separato dall'HTML
    e.preventDefault();
    
    // Recuperiamo i dati dall'oggetto target dell'evento (il form)
    const formData = new FormData(e.target);
    const name = formData.get('username');
    const age = formData.get('age');

    alert(`Ciao ${name}! Hai dichiarato ${age} anni.`);
    console.log("Invio asincrono simulato per:", name);
});
