from app.database import SessionLocal
from app import models
import json

db = SessionLocal()

data = {
    "equipos": [e.__dict__ for e in db.query(models.Equipo).all()],
    "carreras": [c.__dict__ for c in db.query(models.Carrera).all()],
    "temporadas": [t.__dict__ for t in db.query(models.Temporada).all()],
    "estadisticas_club": [e.__dict__ for e in db.query(models.EstadisticaClub).all()],
    "logros_club": [l.__dict__ for l in db.query(models.LogroClub).all()],
    "jugadores": [j.__dict__ for j in db.query(models.Jugador).all()],
    "jugador_temporada": [jt.__dict__ for jt in db.query(models.JugadorTemporada).all()],
}

for tabla in data:
    for item in data[tabla]:
        item.pop("_sa_instance_state", None)

with open("fc_career_export.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

db.close()

print("Datos exportados en fc_career_export.json")