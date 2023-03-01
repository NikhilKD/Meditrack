from py_files.keys import google
import googlemaps # pip install googlemaps

def miles_to_meters(miles):
    try:
        return miles * 1_609.344
    except:
        return 0
        

def get_doctors(location,doctor):
    API_KEY = google['API_KEY']
    map_client = googlemaps.Client(API_KEY)

    address = location
    geocode = map_client.geocode(address=address)
    (lat, lng) = map(geocode[0]['geometry']['location'].get, ('lat', 'lng'))


    search_string = doctor
    distance = miles_to_meters(2)
    business_list = []

    response = map_client.places_nearby(
        location=(lat, lng),
        keyword=search_string,
        radius=distance
    )   

    business_list.extend(response.get('results'))
    return business_list