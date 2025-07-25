
from app import mysql


#Metodo para todos los álbumes activos
def getAll():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tb_albums WHERE state = 1")
    result = cursor.fetchall()
    cursor.close()
    return result

# Metodo para obtiene un álbum específico por ID
def getById(id):

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tb_albums WHERE id = %s", (id,))
    result = cursor.fetchone()
    cursor.close()
    return result

# Metodo Inserta un nuevo album
def insertAlbum(titulo, artista, anio):
    
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO tb_albums (album, artista, anio, state) VALUES (%s, %s, %s, 1)",
        (titulo, artista, anio)
    )
    mysql.connection.commit()
    cursor.close()

# Metodo para actualiza un album 
def updateAlbum(id, titulo, artista, anio):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE tb_albums SET album = %s, artista = %s, anio = %s WHERE id = %s",
        (titulo, artista, anio, id)
    )
    mysql.connection.commit()
    cursor.close()

#Elimina lógicamente un álbum (soft delete)."""
def softDeleteAlbum(id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE tb_albums SET state = 0 WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
