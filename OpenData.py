import requests

from APIKEY import api_key


def get_matching_station_informations(url, headers, prefix, limit):
    response = requests.get(url, headers=headers)
    data = response.json()
    stations = data['data']['stations']

    count = 0
    for station in stations:
        if station['name'].startswith(prefix):
            yield station
            count += 1
            if count == limit:
                break


def get_matching_station_statuses(url, headers, station_id):
    response = requests.get(url, headers=headers)
    data = response.json()
    stations = data['data']['stations']

    for station in stations:
        if station['station_id'] == station_id:
            return station

    return None

def compute_distance(l1, l2, l3, l4):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=" \
          f"{l1},{l2}&destinations={l3},{l4}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        distance = data["rows"][0]["elements"][0]["distance"]["value"]
        return distance
    else:
        return None

information_url = 'https://gbfs.urbansharing.com/rowermevo.pl/station_information.json'
status_url = 'https://gbfs.urbansharing.com/rowermevo.pl/station_status.json'

headers = {'Client-Identifier': 'IDENTIFIER'}
name = 'GDA'
N = 100

# get_matching_station_statuses(status_url, headers, 5)
# matching_stations = get_matching_station_informations(information_url, headers, name, N)
#
#
#
# for station in matching_stations:
#     station_id = station['station_id']
#     name = station['name']
#     lat = station['lat']
#     lon = station['lon']
#     capacity = station['capacity']
#
#     print("INFORMATION")
#     print(f"Station ID: {station_id}")
#     print(f"Name: {name}")
#     print(f"Latitude: {lat}")
#     print(f"Longitude: {lon}")
#     print(f"Capacity: {capacity}")
#
#     print("STATUS")
#     station_status = get_matching_station_statuses(status_url, headers, station_id)
#     print(station_status)
#     num_bikes_available = station_status['num_bikes_available']
#     print(num_bikes_available)
#     # print(num_bikes_disabled)
#     print()


lat1 = 54.35909
lon1 = 18.74597

lat2 = 54.32356
lon2 = 18.55579

print(compute_distance(lat1, lon1, lat2, lon2))