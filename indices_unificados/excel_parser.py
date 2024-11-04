"""
Existe una base de datos histórica con registros desde enero de 2013:

https://m.inei.gob.pe/estadisticas/indice-tematico/price-indexes/

El link para "Índices Unificados de Precios de la Construcción (Base Julio 1992 = 100)"
no es estático, por lo que hay que descargarlo manualmente. Sin embargo, sirve para
obtener la base de datos con la que empezar.
"""

import sqlite3


class SQLiteError(Exception):
    pass


def insert_regiones(path: str, regiones: list[tuple]):
    conn = sqlite3.connect(path)

    try:
        conn.setconfig(1002)
        cursor = conn.cursor()
        sql = """
            INSERT INTO regiones("región", "área_geográfica")
            VALUES (?, ?)
    """
        cursor.executemany(sql, regiones)
        conn.commit()
    except sqlite3.Error as e:
        raise SQLiteError(e)
    finally:
        conn.close()


def insert_códigos(path: str, códigos: list[tuple]):
    conn = sqlite3.connect(path)

    try:
        conn.setconfig(1002)
        cursor = conn.cursor()
        sql = """
            INSERT INTO códigos("ID", "Categoría", "Activo")
            VALUES (?, ?, ?)
    """
        cursor.executemany(sql, códigos)
        conn.commit()
    except sqlite3.Error as e:
        raise SQLiteError(e)
    finally:
        conn.close()


def get_regiones(path: str):
    regiones_por_area = []

    with open(path, 'r+') as file:
        lines = file.readlines()
        for line in lines:
            área = line.split(sep=':')[0].strip()[-1]
            regiones = line.split(sep=':')[1].split(sep=',')
            for región in regiones:
                row = región.strip(), int(área)
                regiones_por_area.append(row)
    return regiones_por_area

def get_códigos(path:str):
    categorías = []

    with open(path, 'r+') as file:
        lines = file.readlines()
        for line in lines:
            código = int(line.split(sep=',')[0].strip())
            elemento = line.split(sep=',')[1].strip()
            activo = int(line.split(sep=',')[2].strip())
            row = código, elemento, activo
            categorías.append(row)
    return categorías

def main():
    # regiones = get_regiones(path='indices_unificados/áreas_geográficas.txt')
    # insert_regiones(path='indices_unificados/indices_unificados.db', regiones=regiones)

    relación_índices = get_códigos('indices_unificados/códigos.txt')
    print(relación_índices)
    insert_códigos('indices_unificados/indices_unificados.db', relación_índices)

main()