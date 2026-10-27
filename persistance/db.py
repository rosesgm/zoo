import os
import time

import mysql.connector

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "host.docker.internal"),
    "port": int(os.getenv("DB_PORT", "9999")),
    "user": os.getenv("DB_USER", "usuario"),
    "password": os.getenv("DB_PASSWORD", "1234"),
    "database": os.getenv("DB_NAME", "animales"),
}

def conectar():
    return mysql.connector.connect(**DB_CONFIG)

def crear_tabla(reintentos=30, espera=2):
    for intento in range(1, reintentos + 1):
        try:
            conexion = conectar()
            break
        except mysql.connector.Error as e:
            if intento == reintentos:
                raise
            print(f"Esperando a MySQL ({intento}/{reintentos}): {e}")
            time.sleep(espera)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS animales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            especie VARCHAR(100) NOT NULL,
            edad INT NOT NULL,
            habitat VARCHAR(100) NOT NULL
        )
    """)
    conexion.commit()
    cursor.close()
    conexion.close()

def listar_animales():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM animales ORDER BY id")
    animales = cursor.fetchall()
    cursor.close()
    conexion.close()
    return animales

def agregar_animal(nombre, especie, edad, habitat):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """INSERT INTO animales (nombre, especie, edad, habitat)
           VALUES (%s, %s, %s, %s)""",
        (nombre, especie, edad, habitat)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_animal(animal_id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM animales WHERE id = %s", (animal_id,)
    )
    animal = cursor.fetchone()
    cursor.close()
    conexion.close()
    return animal

def actualizar_animal(animal_id, nombre, especie, edad, habitat):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        """UPDATE animales
           SET nombre=%s, especie=%s, edad=%s, habitat=%s
           WHERE id=%s""",
        (nombre, especie, edad, habitat, animal_id)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_animal(animal_id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "DELETE FROM animales WHERE id = %s", (animal_id,)
    )
    conexion.commit()
    cursor.close()
    conexion.close()
