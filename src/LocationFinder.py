from tenacity import retry
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

geolocator = Nominatim(user_agent="my_geopy_app")

#@retry((Exception), tries=3, delay=0, backoff=0)
def getLocation(latitude, longitude):
    locationDict = {}
    try:
        location = geolocator.reverse(str(latitude) + "," + str(longitude))
        address = location.raw['address']

        city = address.get("city", "")
        state = address.get("state", "")
        country = address.get("country", "")
        code = address.get("country_code")
        zipcode = address.get("postcode")

        locationDict["city"] = city
        locationDict["state"] = state
        locationDict["country"] = country
        locationDict["code"] = code
        locationDict["zipcode"] = zipcode
    
    except GeocoderServiceError as e:
        print("Error: ", e)

    finally:
        return locationDict

def main():
    test_latitude = "25.594095"
    test_longitude = "85.137566"
    print(getLocation(test_latitude, test_longitude))

if __name__ == '__main__':
    main()
