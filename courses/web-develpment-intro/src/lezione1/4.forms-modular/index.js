document.getElementById('myForm').onsubmit = (e) => {
    e.preventDefault();
    const name = e.target.username.value;
    alert(`Ciao ${name}!`);
    const age = prompt("Quanti anni hai?");
    console.log("Età inserita:", age);
};
