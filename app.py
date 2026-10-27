from flask import Flask, render_template, request, redirect, url_for
from persistance.db import (
    crear_tabla, listar_animales, agregar_animal,
    obtener_animal, actualizar_animal, eliminar_animal
)

app = Flask(__name__)

crear_tabla()

@app.route("/")
def index():
    return render_template(
        "index.html",
        animales=listar_animales()
    )

@app.route("/agregar", methods=["POST"])
def agregar():
    nombre = request.form["nombre"].strip()
    especie = request.form["especie"].strip()
    edad = int(request.form["edad"])
    habitat = request.form["habitat"].strip()

    agregar_animal(nombre, especie, edad, habitat)
    return redirect(url_for("index"))

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    animal = obtener_animal(id)

    if animal is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        actualizar_animal(
            id,
            request.form["nombre"].strip(),
            request.form["especie"].strip(),
            int(request.form["edad"]),
            request.form["habitat"].strip()
        )
        return redirect(url_for("index"))

    return render_template("editar.html", animal=animal)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    eliminar_animal(id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
