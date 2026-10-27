from persistance import db


def test_animal_existe():
    actual_result = db.listar_animales()
    nombres = [animal["nombre"] for animal in actual_result]

    assert "Vaca" in nombres
    assert "serpiente" in nombres