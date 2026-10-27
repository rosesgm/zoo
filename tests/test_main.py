from persistance import db


def test_animal_existe():
    db.crear_tabla()
    db.agregar_animal("Simba", "León", 5, "Sabana")

    actual_result = db.listar_animales()
    nombres = [animal["nombre"] for animal in actual_result]

    assert "Simba" in nombres