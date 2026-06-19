from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas


def calcular_jugador_temporada(datos):
    media_inicial = datos.media_inicial or 0
    media_final = datos.media_final or 0
    partidos = datos.partidos_jugados or 0
    goles = datos.goles or 0
    asistencias = datos.asistencias or 0

    subio = media_final - media_inicial
    goles_asistencias = goles + asistencias

    porcentaje_goles = goles / partidos if partidos > 0 else 0
    porcentaje_asistencias = asistencias / partidos if partidos > 0 else 0

    return subio, goles_asistencias, porcentaje_goles, porcentaje_asistencias


def crear_equipo(db: Session, equipo: schemas.EquipoCreate):
    nuevo = models.Equipo(**equipo.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_equipos(db: Session):
    return db.query(models.Equipo).all()


def obtener_equipo(db: Session, equipo_id: int):
    equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()

    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    return equipo


def crear_carrera(db: Session, carrera: schemas.CarreraCreate):
    equipo = obtener_equipo(db, carrera.equipo_id)

    nueva = models.Carrera(**carrera.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def listar_carreras(db: Session):
    return db.query(models.Carrera).all()


def obtener_carrera(db: Session, carrera_id: int):
    carrera = db.query(models.Carrera).filter(models.Carrera.id == carrera_id).first()

    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    return carrera


def crear_temporada(db: Session, temporada: schemas.TemporadaCreate):
    obtener_carrera(db, temporada.carrera_id)

    nueva = models.Temporada(**temporada.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def listar_temporadas_por_carrera(db: Session, carrera_id: int):
    obtener_carrera(db, carrera_id)

    return db.query(models.Temporada).filter(
        models.Temporada.carrera_id == carrera_id
    ).all()


def obtener_temporada(db: Session, temporada_id: int):
    temporada = db.query(models.Temporada).filter(
        models.Temporada.id == temporada_id
    ).first()

    if not temporada:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")

    return temporada


def crear_estadistica_club(db: Session, estadistica: schemas.EstadisticaClubCreate):
    obtener_temporada(db, estadistica.temporada_id)

    diferencia = estadistica.goles_favor - estadistica.goles_contra

    nueva = models.EstadisticaClub(
        **estadistica.model_dump(),
        diferencia_goles=diferencia
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def crear_logro_club(db: Session, logro: schemas.LogroClubCreate):
    obtener_temporada(db, logro.temporada_id)

    nuevo = models.LogroClub(**logro.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def crear_jugador(db: Session, jugador: schemas.JugadorCreate):
    nuevo = models.Jugador(**jugador.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_jugadores(db: Session):
    return db.query(models.Jugador).all()


def obtener_jugador(db: Session, jugador_id: int):
    jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()

    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    return jugador


def crear_jugador_temporada(db: Session, datos: schemas.JugadorTemporadaCreate):
    obtener_jugador(db, datos.jugador_id)
    obtener_temporada(db, datos.temporada_id)

    subio, goles_asistencias, porcentaje_goles, porcentaje_asistencias = calcular_jugador_temporada(datos)

    nuevo = models.JugadorTemporada(
        **datos.model_dump(),
        subio=subio,
        goles_asistencias=goles_asistencias,
        porcentaje_goles=porcentaje_goles,
        porcentaje_asistencias=porcentaje_asistencias
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def listar_jugadores_por_temporada(db: Session, temporada_id: int):
    obtener_temporada(db, temporada_id)

    return db.query(models.JugadorTemporada).filter(
        models.JugadorTemporada.temporada_id == temporada_id
    ).all()


def actualizar_jugador_temporada(
    db: Session,
    jugador_temporada_id: int,
    datos: schemas.JugadorTemporadaUpdate
):
    registro = db.query(models.JugadorTemporada).filter(
        models.JugadorTemporada.id == jugador_temporada_id
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    datos_actualizados = datos.model_dump(exclude_unset=True)

    for campo, valor in datos_actualizados.items():
        setattr(registro, campo, valor)

    registro.subio = registro.media_final - registro.media_inicial
    registro.goles_asistencias = registro.goles + registro.asistencias

    if registro.partidos_jugados > 0:
        registro.porcentaje_goles = registro.goles / registro.partidos_jugados
        registro.porcentaje_asistencias = registro.asistencias / registro.partidos_jugados
    else:
        registro.porcentaje_goles = 0
        registro.porcentaje_asistencias = 0

    db.commit()
    db.refresh(registro)
    return registro


def eliminar_jugador_temporada(db: Session, jugador_temporada_id: int):
    registro = db.query(models.JugadorTemporada).filter(
        models.JugadorTemporada.id == jugador_temporada_id
    ).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    db.delete(registro)
    db.commit()

    return {"mensaje": "Jugador eliminado de la temporada correctamente"}


def dashboard_temporada(db: Session, temporada_id: int):
    obtener_temporada(db, temporada_id)

    jugadores = db.query(models.JugadorTemporada).filter(
        models.JugadorTemporada.temporada_id == temporada_id
    ).all()

    if not jugadores:
        return {
            "mensaje": "No hay jugadores registrados en esta temporada",
            "temporada_id": temporada_id
        }

    max_goleador = max(jugadores, key=lambda j: j.goles)
    max_asistidor = max(jugadores, key=lambda j: j.asistencias)
    mejor_ga = max(jugadores, key=lambda j: j.goles_asistencias)
    mayor_subida = max(jugadores, key=lambda j: j.subio)

    return {
        "temporada_id": temporada_id,
        "maximo_goleador": {
            "jugador": max_goleador.jugador.nombre,
            "goles": max_goleador.goles
        },
        "maximo_asistidor": {
            "jugador": max_asistidor.jugador.nombre,
            "asistencias": max_asistidor.asistencias
        },
        "mejor_g_a": {
            "jugador": mejor_ga.jugador.nombre,
            "g_a": mejor_ga.goles_asistencias
        },
        "mayor_subida": {
            "jugador": mayor_subida.jugador.nombre,
            "subio": mayor_subida.subio
        }
    }

def listar_logros_por_temporada(db: Session, temporada_id: int):
    obtener_temporada(db, temporada_id)

    return db.query(models.LogroClub).filter(
        models.LogroClub.temporada_id == temporada_id
    ).all()

def obtener_estadistica_por_temporada(db: Session, temporada_id: int):
    obtener_temporada(db, temporada_id)

    return db.query(models.EstadisticaClub).filter(
        models.EstadisticaClub.temporada_id == temporada_id
    ).first()

def historial_jugador(db: Session, jugador_id: int):
    obtener_jugador(db, jugador_id)

    return db.query(models.JugadorTemporada).filter(
        models.JugadorTemporada.jugador_id == jugador_id
    ).all()