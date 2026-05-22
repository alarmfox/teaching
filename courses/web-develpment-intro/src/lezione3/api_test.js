/**
 * JSONPlaceholder Client - Esempio Node.js
 * Utilizza l'API fetch nativa (Node.js 18+)
 */

async function getPost(id) {
    const url = `https://jsonplaceholder.typicode.com/posts/${id}`;

    try {
        console.log(`--- Recupero Post ID: ${id} ---`);
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Errore HTTP! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log(`Titolo: ${data.title}`);
        console.log(`Body:   ${data.body.substring(0, 50)}...`);

    } catch (error) {
        console.error("Errore nel recupero post:", error.message);
    }
}

async function createPost() {
    const url = "https://jsonplaceholder.typicode.com/posts";
    const payload = {
        title: "Lezione API Node.js",
        body: "Esempio di POST request.",
        userId: 1
    };

    try {
        console.log("\n--- Creazione Nuovo Post ---");
        const response = await fetch(url, {
            method: "POST",
            body: JSON.stringify(payload),
            headers: {
                "Content-type": "application/json; charset=UTF-8",
            },
        });

        if (response.ok) {
            const data = await response.json();
            console.log("Post creato con successo!");
            console.log("ID assegnato dal server:", data.id);
        }
    } catch (error) {
        console.error("Errore nella creazione post:", error.message);
    }
}

// Esecuzione
async function run() {
    await getPost(1);
    await createPost();
}

run();
