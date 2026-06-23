from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, schemas, models
from .external_api import buscar_equipo_web, buscar_jugador_web

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/web/equipos")
async def buscar_equipos_web(nombre: str):
    return await buscar_equipo_web(nombre)


@router.get("/web/jugadores")
async def buscar_jugadores_web(nombre: str):
    return await buscar_jugador_web(nombre)


@router.post("/equipos")
def crear_equipo(equipo: schemas.EquipoCreate, db: Session = Depends(get_db)):
    return crud.crear_equipo(db, equipo)


@router.get("/equipos")
def listar_equipos(db: Session = Depends(get_db)):
    return crud.listar_equipos(db)


@router.get("/equipos/{equipo_id}")
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    return crud.obtener_equipo(db, equipo_id)


@router.post("/carreras")
def crear_carrera(carrera: schemas.CarreraCreate, db: Session = Depends(get_db)):
    return crud.crear_carrera(db, carrera)


@router.get("/carreras", response_model=list[schemas.CarreraResponse])
def listar_carreras(db: Session = Depends(get_db)):
    return crud.listar_carreras(db)


@router.get("/carreras/{carrera_id}", response_model=schemas.CarreraResponse)
def obtener_carrera(carrera_id: int, db: Session = Depends(get_db)):
    return crud.obtener_carrera(db, carrera_id)


@router.post("/temporadas")
def crear_temporada(temporada: schemas.TemporadaCreate, db: Session = Depends(get_db)):
    return crud.crear_temporada(db, temporada)


@router.get("/carreras/{carrera_id}/temporadas")
def listar_temporadas_por_carrera(carrera_id: int, db: Session = Depends(get_db)):
    return crud.listar_temporadas_por_carrera(db, carrera_id)


@router.get("/temporadas/{temporada_id}")
def obtener_temporada(temporada_id: int, db: Session = Depends(get_db)):
    return crud.obtener_temporada(db, temporada_id)


@router.post("/estadisticas-club")
def crear_estadistica_club(
    estadistica: schemas.EstadisticaClubCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_estadistica_club(db, estadistica)


@router.post("/logros-club")
def crear_logro_club(logro: schemas.LogroClubCreate, db: Session = Depends(get_db)):
    return crud.crear_logro_club(db, logro)


@router.post("/jugadores")
def crear_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db)):
    try:
        if jugador.id_externo:
            existente = db.query(models.Jugador).filter(
                models.Jugador.id_externo == jugador.id_externo
            ).first()

            if existente:
                return existente

        else:
            existente = db.query(models.Jugador).filter(
                models.Jugador.nombre == jugador.nombre
            ).first()

            if existente:
                return existente

        nuevo = models.Jugador(
            id_externo=jugador.id_externo,
            nombre=jugador.nombre,
            pais=jugador.pais,
            posicion=jugador.posicion,
            foto=jugador.foto,
        )

        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)

        return nuevo

    except Exception as e:
        db.rollback()
        raise e

    except Exception as e:
        db.rollback()
        return {
            "error": str(e),
            "tipo": type(e).__name__
        }

@router.get("/jugadores")
def listar_jugadores(db: Session = Depends(get_db)):
    return crud.listar_jugadores(db)


@router.get("/jugadores/{jugador_id}")
def obtener_jugador(jugador_id: int, db: Session = Depends(get_db)):
    return crud.obtener_jugador(db, jugador_id)


@router.post("/jugadores-temporada")
def crear_jugador_temporada(
    datos: schemas.JugadorTemporadaCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.crear_jugador_temporada(db, datos)

    except Exception as e:
        db.rollback()
        return {
            "error": str(e),
            "tipo": type(e).__name__
        }


@router.get(
    "/temporadas/{temporada_id}/jugadores",
    response_model=list[schemas.JugadorTemporadaResponse]
)
def listar_jugadores_por_temporada(
    temporada_id: int,
    db: Session = Depends(get_db)
):
    return crud.listar_jugadores_por_temporada(db, temporada_id)


@router.put("/jugadores-temporada/{jugador_temporada_id}")
def actualizar_jugador_temporada(
    jugador_temporada_id: int,
    datos: schemas.JugadorTemporadaUpdate,
    db: Session = Depends(get_db)
):
    return crud.actualizar_jugador_temporada(db, jugador_temporada_id, datos)


@router.delete("/jugadores-temporada/{jugador_temporada_id}")
def eliminar_jugador_temporada(
    jugador_temporada_id: int,
    db: Session = Depends(get_db)
):
    return crud.eliminar_jugador_temporada(db, jugador_temporada_id)


@router.get("/temporadas/{temporada_id}/dashboard")
def dashboard_temporada(temporada_id: int, db: Session = Depends(get_db)):
    return crud.dashboard_temporada(db, temporada_id)

@router.get("/temporadas/{temporada_id}/logros")
def listar_logros_por_temporada(temporada_id: int, db: Session = Depends(get_db)):
    return crud.listar_logros_por_temporada(db, temporada_id)

@router.get("/temporadas/{temporada_id}/estadisticas-club")
def obtener_estadistica_por_temporada(
    temporada_id: int,
    db: Session = Depends(get_db)
):
    return crud.obtener_estadistica_por_temporada(db, temporada_id)

@router.get(
    "/jugadores/{jugador_id}/historial",
    response_model=list[schemas.JugadorTemporadaResponse]
)
def historial_jugador(jugador_id: int, db: Session = Depends(get_db)):
    return crud.historial_jugador(db, jugador_id)