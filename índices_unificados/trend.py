"""
Análisis de la fluctuación de índices unificados.
"""

import altair as alt
import pandas as pd
import sqlite3

from tabulate import tabulate


class SQLiteError(Exception):
    pass


def generate_chart(código: int, área: int, año=[pd.Timestamp.now().year - 1, pd.Timestamp.now().year]):

    conn = sqlite3.connect('índices_unificados/índices_unificados.db')
    try:
        cursor = conn.cursor()

        sql = """
            SELECT Nombre
            FROM códigos
            WHERE ID = ?
        """
        cursor.execute(sql, [código])
        nombre = cursor.fetchone()[0]

        sql = """
            SELECT Índice, Código, Área, Año, Mes
            FROM índices_unificados
        """
        df = pd.read_sql(sql, conn)
    except sqlite3.Error as e:
        raise SQLiteError(e)
    finally:
        conn.close()

    if año:
        if isinstance(año, list):
            df_filtered = df[(df.Código == código) & (
                df.Área == área) & (df.Año.isin(año))]
        else:
            df_filtered = df[(df.Código == código) & (
                df.Área == área) & (df.Año == año)]
    else:
        df_filtered = df[(df.Código == código) & (df.Área == área)]
    df_filtered = df_filtered.rename(columns={'Año': 'year', 'Mes': 'month'})
    df_filtered['Período'] = pd.to_datetime(
        df_filtered[['year', 'month']].assign(day=1))

    # padding for y axis
    min_y = df_filtered['Índice'].min()
    max_y = df_filtered['Índice'].max()
    padding = (max_y - min_y) * 0.5
    y_domain = (min_y - padding, max_y + padding)

    chart = alt.Chart(df_filtered).mark_line().encode(
        x=alt.X('Período:T', title='Mes', axis=alt.Axis(
            format='%Y-%m', labelAngle=-90, tickCount='month')),
        y=alt.Y('Índice:Q', title='Índice', axis=alt.Axis(
            tickCount=10), scale=alt.Scale(domain=y_domain)),
        tooltip=['Período', 'Índice']
    ).properties(
        title=[f"Índice Unificado {código} - Área {área}", f"{nombre}"]
    )
    return chart


def get_código_área():
    conn = sqlite3.connect('índices_unificados/índices_unificados.db')
    try:
        cursor = conn.cursor()

        sql = """
            SELECT ID, Nombre
            FROM códigos
        """
        cursor.execute(sql)
        códigos = cursor.fetchall()
        print(tabulate(códigos, tablefmt="orgtbl"))
        código = int(input('\nCódigo: '))

        sql = """
            SELECT ID, región
            FROM regiones
        """
        cursor.execute(sql)
        regiones = cursor.fetchall()
        print(tabulate(regiones, tablefmt="orgtbl"))
        región_ID = int(input('\nRegión: '))

        sql = """
            SELECT área_geográfica
            FROM regiones
            WHERE ID = ?
        """
        cursor.execute(sql, [región_ID])
        área = cursor.fetchone()[0]

        return código, área

    except sqlite3.Error as e:
        raise SQLiteError(e)
    finally:
        conn.close()


path = 'índices_unificados/chart.html'
código, área = get_código_área()
chart = generate_chart(código, área)
chart.save(path)
