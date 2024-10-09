from os import getcwd, listdir, path
from uuid import UUID

from database import Base, Driver, Point, Track, Vehicle
from gpxpy.gpx import GPXTrack, GPXTrackPoint
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from .gpx import parse_gpx


def create_connection() -> Engine:
    engine = create_engine('sqlite:///database/fahrzeiten.db')
    Base.metadata.create_all(engine)
    return engine


def update_database(session: Session):
    errors = {}

    gpx_files = [file for file
                 in listdir(path.join(getcwd(), 'fahrten'))
                 if '.gpx' in file]
    for file in gpx_files:
        if bool(session.query(Track).where(Track.file_name == file).all()):
            # expecting a file to not be modified by eg adding another track later
            continue

        driver_name, vehicle_plate = file.split('_')[:2]
        driver = _get_or_create(session,
                                Driver,
                                Driver.driver_name,
                                driver_name)
        vehicle = _get_or_create(session,
                                 Vehicle,
                                 Vehicle.vehicle_plate,
                                 vehicle_plate)

        gpx = parse_gpx(file)
        # gpx.waypoints
        if not gpx.tracks:
            errors.update({file: 'unable to find any tracks.'})
            continue
        for gpx_track in gpx.tracks:
            if not gpx_track.segments:
                errors.update({file: 'unable to find any segments'})
                continue
            track = Track(file_name=file,
                          driver_id=driver.driver_id,
                          vehicle_id=vehicle.vehicle_id)
            session.add(track)
            session.commit()
            add_track(session, gpx_track, track.track_id)

    return errors


def add_track(session: Session, track: GPXTrack, track_id):
    for segment in track.segments:
        for trackpoint in segment.points:
            add_point(session, trackpoint, track_id)


def add_point(session: Session, trackpoint: GPXTrackPoint, track_id: UUID):
    point = Point(timestamp=trackpoint.time,
                  lat=trackpoint.latitude,
                  lon=trackpoint.longitude,
                  ele=trackpoint.elevation,
                  track_id=track_id)
    session.add(point)
    session.commit()


def _get_or_create(session: Session, model, field, value):
    try:
        instance = session.query(model).where(field == value).one()
    except NoResultFound:
        instance = model(**{field.key: value})
        session.add(instance)
        session.commit()
    return instance
