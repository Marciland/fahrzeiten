# pylint: skip-file
from uuid import UUID as py_UUID
from uuid import uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedAsDataclass,
                            mapped_column)
from sqlalchemy.types import REAL, TEXT, UUID


class Base(DeclarativeBase, MappedAsDataclass):
    '''Cannot use DeclarativeBase directly.'''


class Driver(Base):
    __tablename__ = "driver"
    driver_id: Mapped[py_UUID] = mapped_column(type_=UUID,
                                               default_factory=uuid4,
                                               primary_key=True,
                                               nullable=False)
    driver_name: Mapped[str] = mapped_column(type_=TEXT,
                                             default=None,
                                             primary_key=False,
                                             nullable=False)


class Track(Base):
    __tablename__ = "track"
    track_id: Mapped[py_UUID] = mapped_column(type_=UUID,
                                              default_factory=uuid4,
                                              primary_key=True,
                                              nullable=False)
    file_name: Mapped[str] = mapped_column(type_=TEXT,
                                           default=None,
                                           primary_key=False,
                                           nullable=False)
    driver_id: Mapped[py_UUID] = mapped_column(ForeignKey('driver.driver_id'),
                                               type_=UUID,
                                               default=None,
                                               nullable=False)
    vehicle_id: Mapped[py_UUID] = mapped_column(ForeignKey('vehicle.vehicle_id'),
                                                type_=UUID,
                                                default=None,
                                                nullable=False)


class Point(Base):
    __tablename__ = "point"
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


class Vehicle(Base):
    __tablename__ = "vehicle"
    vehicle_id: Mapped[py_UUID] = mapped_column(type_=UUID,
                                                default_factory=uuid4,
                                                primary_key=True,
                                                nullable=False)
    vehicle_plate: Mapped[str] = mapped_column(type_=TEXT,
                                               default=None,
                                               primary_key=False,
                                               nullable=False)
