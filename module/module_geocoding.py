# -*- coding: utf-8 -*-
from geopy.geocoders import Nominatim

def nominatim_search(addressIn):

    geolocator = Nominatim()
    location = geolocator.geocode(addressIn)
    if location is not None:
        # print('boundingbox: {}'.format(location.raw['boundingbox']))
        bbox = location.raw['boundingbox']
        strBboxForOAM = '{},{},{},{}'.format(bbox[2], bbox[0], bbox[3], bbox[1])
        return strBboxForOAM
    else:
        return 'failed'
