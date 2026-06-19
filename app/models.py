from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    id_externo = Column(String, nullable=True)
    nombre = Column(String, nullable=False)
    pais = Column(String)
    liga = Column(String)
    estadio = Column(String)
    escudo = Column(String)

    carreras = relationship("Carrera", back_populates="equipo")


class Carrera(Base):
    __tablename__ = "carreras"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

    equipo_id = Column(Integer, ForeignKey("equipos.id"))

    equipo = relationship("Equipo", back_populates="carreras")
    temporadas = relationship("Temporada", back_populates="carrera")


class Temporada(Base):
    __tablename__ = "temporadas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    carrera_id = Column(Integer, ForeignKey("carreras.id"))

    carrera = relationship("Carrera", back_populates="temporadas")
    estadistica_club = relationship(
        "EstadisticaClub",
        back_populates="temporada",
        uselist=False
    )
    logros = relationship("LogroClub", back_populates="temporada")
    jugadores_temporada = relationship("JugadorTemporada", back_populates="temporada")


class EstadisticaClub(Base):
    __tablename__ = "estadisticas_club"

    id = Column(Integer, primary_key=True, index=True)

    temporada_id = Column(Integer, ForeignKey("temporadas.id"))

    partidos_jugados = Column(Integer, default=0)
    victorias = Column(Integer, default=0)
    empates = Column(Integer, default=0)
    derrotas = Column(Integer, default=0)

    goles_favor = Column(Integer, default=0)
    goles_contra = Column(Integer, default=0)
    diferencia_goles = Column(Integer, default=0)

    puntos = Column(Integer, default=0)
    posicion_liga = Column(Integer, nullable=True)

    temporada = relationship("Temporada", back_populates="estadistica_club")


class LogroClub(Base):
    __tablename__ = "logros_club"

    id = Column(Integer, primary_key=True, index=True)

    temporada_id = Column(Integer, ForeignKey("temporadas.id"))

    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    tipo = Column(String, nullable=True)

    temporada = relationship("Temporada", back_populates="logros")


class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)

    id_externo = Column(String, nullable=True)
    nombre = Column(String, nullable=False)
    pais = Column(String)
    posicion = Column(String)
    foto = Column(String)

    temporadas = relationship("JugadorTemporada", back_populates="jugador")


class JugadorTemporada(Base):
    __tablename__ = "jugador_temporada"

    id = Column(Integer, primary_key=True, index=True)

    jugador_id = Column(Integer, ForeignKey("jugadores.id"))
    temporada_id = Column(Integer, ForeignKey("temporadas.id"))

    dorsal = Column(Integer, nullable=True)
    edad = Column(Integer, nullable=True)

    premio_individual = Column(Boolean, default=False)

    media_inicial = Column(Integer, default=0)
    media_final = Column(Integer, default=0)
    subio = Column(Integer, default=0)

    partidos_jugados = Column(Integer, default=0)
    goles = Column(Integer, default=0)
    asistencias = Column(Integer, default=0)
    goles_asistencias = Column(Integer, default=0)

    porcentaje_goles = Column(Float, default=0)
    porcentaje_asistencias = Column(Float, default=0)

    jugador = relationship("Jugador", back_populates="temporadas")
    temporada = relationship("Temporada", back_populates="jugadores_temporada")