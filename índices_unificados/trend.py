"""
Análisis de la fluctuación de índices unificados.

Cuenta con tener la base de datos actualizada al mes.

Veámos cómo nos va.
"""

import altair as alt
import pandas as pd
import sqlite3

class SQLiteError(Exception):
    pass

conn = sqlite3.connect('índices_unificados/índices_unificados.db')
sql = """
    SELECT Índice, Código, Área, Año, Mes
    FROM índices_unificados
"""
df = pd.read_sql(sql, conn)
print(df)