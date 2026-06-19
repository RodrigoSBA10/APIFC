import sqlite3
import psycopg2

sqlite_conn = sqlite3.connect("fc_career.db")
sqlite_cursor = sqlite_conn.cursor()

pg_conn = psycopg2.connect(
    "postgresql://postgres.pxmmcnouflibkemmxnnq:TU_PASSWORD@aws-1-us-east-1.pooler.supabase.com:6543/postgres"
)
pg_cursor = pg_conn.cursor()

tablas = [
    "equipos",
    "carreras",
    "temporadas",
    "estadisticas_club",
    "logros_club",
    "jugadores",
    "jugador_temporada"
]

for tabla in tablas:
    sqlite_cursor.execute(f"SELECT * FROM {tabla}")
    filas = sqlite_cursor.fetchall()

    columnas = [desc[0] for desc in sqlite_cursor.description]

    for fila in filas:
        placeholders = ", ".join(["%s"] * len(columnas))
        columnas_sql = ", ".join(columnas)

        query = f"""
        INSERT INTO {tabla} ({columnas_sql})
        VALUES ({placeholders})
        ON CONFLICT DO NOTHING
        """

        pg_cursor.execute(query, fila)

pg_conn.commit()

sqlite_conn.close()
pg_conn.close()

print("Migración completada")