import googlemaps
# Initialize Google Maps client
GOOGLE_MAPS_API_KEY = ""  # Replace with your actual API key
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def get_lat_lon(location):
    try:
        geocode_result = gmaps.geocode(location)
        if geocode_result:
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            print(lat, lng)
    except Exception as e:
        print(f"Error fetching geocode for {location}: {e}")
    return None, None

get_lat_lon("Santacruz, Mumbai")