import requests

# JSONPlaceholder e una finta API REST online per test e prototipazione.
# Endpoint: https://jsonplaceholder.typicode.com
# Documentazione: https://jsonplaceholder.typicode.com/guide/

def get_placeholder_post(post_id):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    
    try:
        print(f"--- Recupero Post ID: {post_id} ---")
        response = requests.get(url, timeout=5)
        
        # Verifica se la richiesta ha avuto successo
        response.raise_for_status()
        
        # Deserializzazione automatica del JSON
        data = response.json()
        
        print(f"User ID: {data['userId']}")
        print(f"Titolo:  {data['title']}")
        print(f"Corpo:   {data['body'][:50]}...")
        
    except requests.exceptions.HTTPError as err:
        print(f"Errore HTTP: {err}")
    except Exception as e:
        print(f"Errore imprevisto: {e}")

def create_placeholder_post():
    url = "https://jsonplaceholder.typicode.com/posts"
    new_post = {
        "title": "Mio nuovo post",
        "body": "Contenuto del post inviato tramite API.",
        "userId": 1
    }
    
    try:
        print("\n--- Creazione Nuovo Post ---")
        # Invio dati (Serializzazione automatica con parametro 'json')
        response = requests.post(url, json=new_post)
        
        if response.status_code == 201:
            print("Post creato con successo (Status 201)!")
            print("Risposta dal server:", response.json())
            
    except Exception as e:
        print(f"Errore nella creazione: {e}")

if __name__ == "__main__":
    get_placeholder_post(1)
    create_placeholder_post()
