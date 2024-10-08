from os import getcwd, path

import gpxpy
from gpxpy.gpx import GPX


def parse_gpx(file_path: str) -> GPX:
    base_dir = path.join(getcwd(), 'fahrten')
    with open(file=path.join(base_dir, file_path),
              mode='r',
              encoding='utf-8') as gpx_file:
        return gpxpy.parse(gpx_file)
