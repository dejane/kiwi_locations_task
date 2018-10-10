import argparse
import requests
import json
import sys

class Data(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)

def getLocationsDataFromApi():
    URL = "https://api.skypicker.com/locations"
    PARAMS = {
        'type': 'box',
        'low_lat': '50.10319',
        'low_lon': '-7.64133',
        'high_lat': '60.15456',
        'high_lon': '1.75159',
        'location_types': 'airport',
        'limit' : '250',
        'sort' : 'name'
    }
    r = requests.get(url=URL, params=PARAMS)
    locationData = Data(r.content)
    ukLocationData = []

    # if we use box api query with United Kingdom min-max-lat-lon, we also get some airports from other countries (like Ireland), we manualy remove them
    for x in locationData.locations:
        if (x['city']['country']['id'] == "GB"):
            ukLocationData.append(x)

    return ukLocationData

def printCities(locationData):
    print("Cities with airports:")
    for x in locationData:
        print(x['city']['name'], x['city']['code'])

def printCoords(locationData):
    print("Coordinates of each airport:")
    for x in locationData:
        print("Lat:", x['location']['lon'], "Lon:", x['location']['lat'])

def printIata(locationData):
    print("IATA codes:")
    for x in locationData:
        print(x['code'])

def printNames(locationData):
    print("Names of all airports:")
    for x in locationData:
        print(x['name'])

def printFull(locationData):
    print("Every detail from each airport:")
    print(json.dumps(locationData, indent=2))

def printDefault(locationData):
    print("Name and IATA code of airport:")
    for x in locationData:
        print(x['name'],x['code'])

def switch(option,locationData):

    switcher = {
        'cities': printCities,
        'coords': printCoords,
        'iata': printIata,
        'names': printNames,
        'full': printFull,
    }

    func = switcher.get(option, lambda: "")
    return func(locationData)

def main():

    locationData = getLocationsDataFromApi()
    parser = argparse.ArgumentParser(description='Kiwi location entry task instructions: ')

    if not len(sys.argv) > 1:
        printDefault(locationData)
        exit()

    parser.add_argument('--cities', action='store_true', help='cities with airports')
    parser.add_argument('--coords', action='store_true', help='coordinates of each airport')
    parser.add_argument('--iata', action='store_true',   help='IATA codes')
    parser.add_argument('--names', action='store_true',  help='name of the airport')
    parser.add_argument('--full', action='store_true',   help='print every detail from each airport')

    options = parser.parse_args()

    for k in options.__dict__:
        if options.__dict__[k] != False:
            switch(k, locationData)

if __name__ == "__main__":
    main()
