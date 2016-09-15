import json
import requests
import argparse
from math import sin, cos, asin, sqrt, radians


def load_data(filepath):
    with open(filepath, 'r') as json_file:
        return json.load(json_file)


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
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_closest_bar(data, longitude, latitude):
    random_bar = data[0]
    min_length = haversine(
        longitude,
        latitude,
        random_bar['Cells']['geoData']['coordinates'][0],
        random_bar['Cells']['geoData']['coordinates'][1],
    )
    for item in data[1:]:
        bar_longtitude, bar_latitude = item['Cells']['geoData']['coordinates']
        length = haversine(longitude, latitude, bar_longtitude, bar_latitude)
        if length < min_length:
            min_length = length
            bar = item
    return bar


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Path to file', required=True)
    args = parser.parse_args()

    bars = load_data(args.path)
    print('Самый большой бар: ', get_biggest_bar(bars)['Cells']['Name'])
    print('Самый маленький бар: ', get_smallest_bar(bars)['Cells']['Name'])
    longitude = float(input('Type longtitude: '))
    latitude = float(input('Type latitude: '))
    print(
        'Ближайший бар: ',
        get_closest_bar(bars, longitude, latitude)['Cells']['Name'],
    )
