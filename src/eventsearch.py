
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import json
from stateabb import us_state_to_abbrev

# print(us_state_to_abbrev)

def long_lat_state(address):
    loc = Nominatim(user_agent="Geopy Library")

    # entering the location name
    getLoc = loc.geocode(address)   
    #print(str(getLoc).split(","))
    latitude, longitude = getLoc.latitude, getLoc.longitude

    state = str(getLoc).split(",")[4]

    return {"Address": address, "longitude": longitude, "latitude": latitude, "State": us_state_to_abbrev[state.lstrip()]}


def scrape_event_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Finds the script tag that contains the JSON data
        script_tag = soup.find('script', type='application/ld+json')
        if script_tag:
            json_data = script_tag.string
            events = json.loads(json_data)
            
            event_list = []
            for item in events.get('itemListElement', []):
                event = item.get('item', {})
                name = event.get('name', 'No Name')
                location = event.get('location', {})
                geo = location.get('geo', {})
                latitude = geo.get('latitude', 'No Latitude')
                longitude = geo.get('longitude', 'No Longitude')

                event_list.append({
                    'name': name,
                    'latitude': latitude,
                    'longitude': longitude
                })

            return event_list
        else:
            print("No script tag found containing the JSON data.")
    else:
        print(f"Error fetching the page: {response.status_code}")

    return []

def main():
    
    address = input("Address")
    info = long_lat_state(address)
    s = info["State"]
    url = f"https://eventbrite.com/d/{s}/politics-and-government/" 
    events = scrape_event_data(url)

    for event in events:
        print(f"Event Name: {event['name']} | Latitude: {event['latitude']} | Longitude: {event['longitude']}")

if __name__ == "__main__":
    main()



