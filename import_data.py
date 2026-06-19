from app.database import SessionLocal
from app import models
import json

db = SessionLocal()

with open(
    "fc_career_export.json",
    "r",
    encoding="utf-8"
) as archivo:
    data = json.load(archivo)

print("Importando equipos...")

for item in data.get("equipos", []):
    db.merge(models.Equipo(**item))

db.commit()

print("Importando carreras...")

for item in data.get("carreras", []):
    db.merge(models.Carrera(**item))

db.commit()

print("Importando temporadas...")

for item in data.get("temporadas", []):
    db.merge(models.Temporada(**item))

db.commit()

print("Importando jugadores...")

for item in data.get("jugadores", []):
    db.merge(models.Jugador(**item))

db.commit()

print("Importando jugadores_temporada...")

for item in data.get("jugadores_temporada", []):
    db.merge(models.JugadorTemporada(**item))

db.commit()

print("Importando estadisticas_club...")

for item in data.get("estadisticas_club", []):
    db.merge(models.EstadisticaClub(**item))

db.commit()

print("Importando logros_club...")

for item in data.get("logros_club", []):
    db.merge(models.LogroClub(**item))

db.commit()

print("Importando jugador_temporada...")

for item in data.get("jugador_temporada", []):
    db.merge(models.JugadorTemporada(**item))

db.commit()

db.close()

print("Importación completada correctamente.")