import gpxpy


def wczytaj_plik(filename):
    lat=[]
    lon=[]
    ele=[]
    with open(filename,'r') as gpx_file:
        gpx=gpxpy.parse(gpx_file)
    for track in gpx.tracks:
        for seg in track.segments:
            for point in seg.points:
                lon.append(point.longitude)
                lat.append(point.latitude)
                ele.append(point.elevation)
    return lon, lat, ele