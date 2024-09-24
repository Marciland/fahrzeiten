# pylint: skip-file
from os import getcwd, listdir, path, system
from uuid import UUID

try:
    import sqlalchemy
except:
    system(f'pip install sqlalchemy==2.0.35')

try:
    import gpxpy
except:
    system(f'pip install gpxpy==1.6.2')

import gpxpy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from modules import Base, Fahrer, Fahrzeug, Track, Punkte


FAHRTEN_DIR = path.join(getcwd(), 'fahrten')


def save_new_data(session: Session, files: list[str]):
    for file in files:
        if bool(session.query(Track).where(Track.datei_name == file).all()):
            continue

        fahrer = Fahrer(name=file.split('_')[0])
        session.add(fahrer)
        session.commit()

        fahrzeug = Fahrzeug(kennzeichen=file.split('_')[1])
        session.add(fahrzeug)
        session.commit()

        track = Track(datei_name=file,
                      fahrer_id=fahrer.fahrer_id,
                      fahrzeug_id=fahrzeug.fahrzeug_id)
        session.add(track)
        session.commit()

        add_points(session, file, track.track_id)


def add_points(session: Session, file: str, track_id: UUID):
    with open(path.join(FAHRTEN_DIR, file), 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        # example file had only one track with one segment
        for trackpoint in gpx.tracks[0].segments[0].points:
            punkt = Punkte(timestamp=trackpoint.time,
                           lat=trackpoint.latitude,
                           lon=trackpoint.longitude,
                           ele=trackpoint.elevation,
                           track_id=track_id)
            session.add(punkt)
            session.commit()


if __name__ == '__main__':
    engine = create_engine('sqlite:///fahrzeiten.db')
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        save_new_data(session, listdir(FAHRTEN_DIR))
