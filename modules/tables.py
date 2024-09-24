# pylint: skip-file
from uuid import UUID as py_UUID
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import REAL, TEXT, UUID

from modules.database import Base


class Fahrer(Base):
    __tablename__ = "fahrer"
    fahrer_id: Mapped[py_UUID] = mapped_column(type_=UUID,
                                               default_factory=uuid4,
                                               primary_key=True,
                                               nullable=False)
    name: Mapped[str] = mapped_column(type_=TEXT,
                                      default=None,
                                      primary_key=False,
                                      nullable=False)


class Track(Base):
    __tablename__ = "track"
    track_id: Mapped[py_UUID] = mapped_column(type_=UUID,
                                              default_factory=uuid4,
                                              primary_key=True,
                                              nullable=False)
    datei_name: Mapped[str] = mapped_column(type_=TEXT,
                                            default=None,
                                            primary_key=False,
                                            nullable=False)
    fahrer_id: Mapped[py_UUID] = mapped_column(ForeignKey('fahrer.fahrer_id'),
                                               type_=UUID,
                                               default=None,
                                               nullable=False)
    fahrzeug_id: Mapped[py_UUID] = mapped_column(ForeignKey('fahrzeug.fahrzeug_id'),
                                                 type_=UUID,
                                                 default=None,
                                                 nullable=False)


class Punkte(Base):
    __tablename__ = "punkte"
    punkte_id: Mapped[py_UUID] = mapped_column(type_=UUID,
                                               default_factory=uuid4,
                                               primary_key=True,
                                               nullable=False)
    timestamp: Mapped[str] = mapped_column(type_=TEXT,
                                           default=None,
                                           primary_key=False,
                                           nullable=False)
    lat: Mapped[float] = mapped_column(type_=REAL,
                                       default=None,
                                       primary_key=False,
                                       nullable=False)
    lon: Mapped[float] = mapped_column(type_=REAL,
                                       default=None,
                                       primary_key=False,
                                       nullable=False)
    ele: Mapped[float] = mapped_column(type_=REAL,
                                       default=None,
                                       primary_key=False,
                                       nullable=False)
    track_id: Mapped[py_UUID] = mapped_column(ForeignKey('track.track_id'),
                                              type_=UUID,
                                              default=None,
                                              nullable=False)


class Fahrzeug(Base):
    __tablename__ = "fahrzeug"
    fahrzeug_id: Mapped[py_UUID] = mapped_column(type_=UUID,
                                                 default_factory=uuid4,
                                                 primary_key=True,
                                                 nullable=False)
    kennzeichen: Mapped[str] = mapped_column(type_=TEXT,
                                             default=None,
                                             primary_key=False,
                                             nullable=False)
