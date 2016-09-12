import json
import requests
from math import sin, cos, asin, sqrt, radians


def load_data(filepath):
    return open(filepath, 'r')


def get_biggest_bar(data):
    return max([item for item in data], key=lambda x: x['Cells']['SeatsCount'])


def get_smallest_bar(data):
    return min([item for item in data], key=lambda x: x['Cells']['SeatsCount'])


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_closest_bar(data, longitude, latitude):
	min_length = 2**32
	bar = 0
	for item in data:
		bar_longtitude = item['Cells']['geoData']['coordinates'][0]
		bar_latitude = item['Cells']['geoData']['coordinates'][1] 
		length = haversine(longitude, latitude, bar_longtitude, bar_latitude)
		if length < min_length:
			min_length = length
			bar = item
	return bar


if __name__ == '__main__':
    with load_data('/home/lamberk/python/devman/3_bars/data.json') as file:
    	bars = json.loads(file.read())
    	print (get_biggest_bar(bars))
    	print (get_smallest_bar(bars))
    	longitude = float(input('Type longtitude: '))
    	latitude = float(input('Type latitude: '))
    	print (get_closest_bar(bars, longitude, latitude))
