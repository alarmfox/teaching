from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Stato dell'applicazione: una lista di dizionari in memoria
# In una applicazione reale, useremmo un database.
tasks = {
    1: {"text": "Imparare Flask", "completed": False},
    2: {"text": "Capire il Server-Side Rendering", "completed": True},
}


@app.route("/")
def index():
    return render_template("template.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    text = request.form.get("task_text")
    if text:
        new_id = max(list(tasks.keys()), default=0) + 1
        tasks[new_id] = {"text": text, "completed": False}
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    task = tasks.get(task_id)
    if task is not None:
        task["completed"] = not task["completed"]
    return redirect(url_for("index"))


# ESERCIZIO: Implementare la rotta per eliminare una task
# @app.route("/delete/<int:task_id>")
# def delete_task(task_id):
#     # Inserisci qui la logica per rimuovere la task dalla lista
#     return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
