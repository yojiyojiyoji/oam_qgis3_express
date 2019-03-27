# -*- coding: utf-8 -*-
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim

def nominatim_search(addressIn):
    ctx = ssl.create_default_context(cafile=certifi.where())
    geopy.geocoders.options.default_ssl_context = ctx
    geolocator = Nominatim()
    # geolocator = Nominatim(scheme='http')
    location = geolocator.geocode(addressIn)
    if location is not None:
        # print('boundingbox: {}'.format(location.raw['boundingbox']))
        bbox = location.raw['boundingbox']
        strBboxForOAM = '{},{},{},{}'.format(bbox[2], bbox[0], bbox[3], bbox[1])
        return strBboxForOAM
    else:
        return 'failed'
