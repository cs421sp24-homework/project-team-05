from geopy.distance import great_circle

def get_distance(addr1, addr2):
    return great_circle((addr1.latitude, addr1.longitude), (addr2.latitude, addr2.longitude)).miles