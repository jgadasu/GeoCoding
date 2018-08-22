"""
Geocoding and Web APIs Project Toolbox exercise
Find the MBTA stops closest to a given location.
Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""

import urllib
from urllib.parse import urlencode
from urllib.request import urlopen
import json
from pprint import pprint
#URLs of Useful Location APIs
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key={}&lat={}&lon={}&format=json"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(response_text)
    return response_data


def into_url(place_name):
    """
    Given a place name or address, turn that into a url that can then be
    put into Google Maps to find its information
    """
    d = {"address" : place_name}
    address = urlencode(d)
    url = GMAPS_BASE_URL + '?' + address
    return url


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    # first get the url from the place_name
    url = into_url(place_name)

    # once you have the url, you can then use the previous function to get
    # the data and then extract latitude and longitude
    response_data = get_json(url)
    lat = response_data["results"][0]["geometry"]["location"]['lat']
    lng = response_data["results"][0]["geometry"]["location"]['lng']
    return (lat,lng)


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.
    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    # this gets the right url
    mbta_url_formatted = MBTA_BASE_URL.format(MBTA_DEMO_API_KEY, latitude, longitude)
    stations = get_json(mbta_url_formatted)

    # creating an empty list for all of the stops
    all_stops = []

    # this says that if there are no close stops, say that there are no close stops
    if len(stations["stop"]) == 0:
        return "There are no stops close to your location"

    # this gets rid of the bus stations and only gets subway stations
    else:
        for station in stations["stop"]:
            all_stops.append(station["parent_station_name"])
        for i, parent_station_name in enumerate(all_stops):
            if len(parent_station_name) != 0:
                return parent_station_name, stations["stop"][i]["distance"]


def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the
    distance from the given place to that stop.
    """
    # creating a format for what it returns
    result_text = "{} is {} miles from {}"

    # getting the actual information
    lat, lng = get_lat_long(place_name)
    station, distance = get_nearest_station(lat, lng)

    # formatting the resulting text
    return result_text.format(station, distance, place_name)


if __name__ == '__main__':
    print (find_stop_near('789 Somerville Avenue, Somerville, MA'))
