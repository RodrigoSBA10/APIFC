from pydantic import BaseModel
from typing import Optional


class EquipoCreate(BaseModel):
    id_externo: Optional[str] = None
    nombre: str
    pais: Optional[str] = None
    liga: Optional[str] = None
    estadio: Optional[str] = None
    escudo: Optional[str] = None


class EquipoResponse(EquipoCreate):
    id: int

    class Config:
        from_attributes = True


class CarreraCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    equipo_id: int


class CarreraResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    equipo_id: int
    equipo: EquipoResponse

    class Config:
        from_attributes = True


class TemporadaCreate(BaseModel):
    nombre: str
    carrera_id: int


class TemporadaResponse(TemporadaCreate):
    id: int

    class Config:
        from_attributes = True

class TemporadaSimpleResponse(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

class EstadisticaClubCreate(BaseModel):
    temporada_id: int
    partidos_jugados: int = 0
    victorias: int = 0
    empates: int = 0
    derrotas: int = 0
    goles_favor: int = 0
    goles_contra: int = 0
    puntos: int = 0
    posicion_liga: Optional[int] = None


class LogroClubCreate(BaseModel):
    temporada_id: int
    titulo: str
    descripcion: Optional[str] = None
    tipo: Optional[str] = None


class JugadorCreate(BaseModel):
    id_externo: Optional[str] = None
    nombre: str
    pais: Optional[str] = None
    posicion: Optional[str] = None
    foto: Optional[str] = None


class JugadorResponse(JugadorCreate):
    id: int

    class Config:
        from_attributes = True


class JugadorTemporadaCreate(BaseModel):
    jugador_id: int
    temporada_id: int

    dorsal: Optional[int] = None
    edad: Optional[int] = None

    premio_individual: bool = False

    media_inicial: int = 0
    media_final: int = 0

    partidos_jugados: int = 0
    goles: int = 0
    asistencias: int = 0


class JugadorTemporadaUpdate(BaseModel):
    dorsal: Optional[int] = None
    edad: Optional[int] = None

    premio_individual: Optional[bool] = None

    media_inicial: Optional[int] = None
    media_final: Optional[int] = None

    partidos_jugados: Optional[int] = None
    goles: Optional[int] = None
    asistencias: Optional[int] = None

class LogroClubResponse(LogroClubCreate):
    id: int

    class Config:
        from_attributes = True


class JugadorTemporadaResponse(BaseModel):
    id: int
    dorsal: Optional[int] = None
    edad: Optional[int] = None
    premio_individual: bool

    media_inicial: int
    media_final: int
    subio: int

    partidos_jugados: int
    goles: int
    asistencias: int
    goles_asistencias: int

    porcentaje_goles: float
    porcentaje_asistencias: float

    jugador: JugadorResponse
    temporada: TemporadaSimpleResponse

    class Config:
        from_attributes = True