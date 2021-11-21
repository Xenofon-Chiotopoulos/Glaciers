import math as m
def haversine_distance(lat1, lon1, lat2, lon2):
    """Return the distance in km between two points around the Earth.
    Latitude and longitude for each point are given in degrees.
    """
    lat1 = m.radians(lat1)
    lon1 = m.radians(lon1)
    lat2 = m.radians(lat2)
    lon2 = m.radians(lon2)

    lat_difference = lat2-lat1
    lon_difference = lon2-lon1
    R = 6371
    
    first_term = m.sin(lat_difference/2)*m.sin(lat_difference/2)
    second_term = m.cos(lat1)*m.cos(lat2)*m.sin(lon_difference/2)*m.sin(lon_difference/2)
    distance = 2*R*m.asin(m.sqrt(first_term+second_term))

    return distance
