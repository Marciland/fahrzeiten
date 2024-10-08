from os import getcwd, listdir, path
from uuid import UUID

from database import Base, Driver, Point, Track, Vehicle
from gpxpy.gpx import GPXTrackPoint
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from .gpx import parse_gpx


def create_connection() -> Engine:
    engine = create_engine('sqlite:///database/fahrzeiten.db')
    Base.metadata.create_all(engine)
    return engine


def update_database(session: Session):
    gpx_files = [file for file
                 in listdir(path.join(getcwd(), 'fahrten'))
                 if '.gpx' in file]
    for file in gpx_files:
        if bool(session.query(Track).where(Track.file_name == file).all()):
            continue

        driver_name = file.split('_')[0]
        try:
            driver = session.query(Driver) \
                .where(Driver.driver_name == driver_name)\
                .one()
        except NoResultFound:
            driver = Driver(driver_name=driver_name)
            session.add(driver)
            session.commit()

        vehicle_plate = file.split('_')[1]
        try:
            vehicle = session.query(Vehicle) \
                .where(Vehicle.vehicle_plate == vehicle_plate)\
                .one()
        except NoResultFound:
            vehicle = Vehicle(vehicle_plate=vehicle_plate)
            session.add(vehicle)
            session.commit()

        track = Track(file_name=file,
                      driver_id=driver.driver_id,
                      vehicle_id=vehicle.vehicle_id)
        session.add(track)
        session.commit()

        gpx = parse_gpx(file)
        # example file had only one track with one segment
        for trackpoint in gpx.tracks[0].segments[0].points:
            add_point(session, trackpoint, track.track_id)


def add_point(session: Session, trackpoint: GPXTrackPoint, track_id: UUID):
    point = Point(timestamp=trackpoint.time,
                  lat=trackpoint.latitude,
                  lon=trackpoint.longitude,
                  ele=trackpoint.elevation,
                  track_id=track_id)
    session.add(point)
    session.commit()
