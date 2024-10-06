from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import json
from config import API_KEY
from stateabb import us_state_to_abbrev

app = Flask(__name__)

# Initialize the geolocator
loc = Nominatim(user_agent='user_agent')

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        address = request.form['address']
        election_info, polling_locations = get_election_info(address)
        # Slice the first 5 polling locations
        top_5_locations = polling_locations[:5]

        # Fetch events for the location and limit to top 5 events
        event_info = get_local_events(address)

        return render_template('index.html', election_info=election_info, polling_locations=top_5_locations, event_info=event_info, address=address)
    return render_template('index.html', election_info=None, polling_locations=None, event_info=None)

# Function to call Google Civic Information API for election day and polling locations
def get_election_info(address):
    url = "https://www.googleapis.com/civicinfo/v2/voterinfo"
    query_params = {"key": API_KEY, "address": address, 'electionId': 2000}
    response = requests.get(url, params=query_params)

    if response.status_code == 200:
        data = response.json()
        election_day = data.get('election', {}).get('electionDay')
        polling_locations = data.get('pollingLocations', [])
        return {'election_day': election_day}, polling_locations
    else:
        return None, []

# Function to get latitude, longitude and state from address
def long_lat_state(address):
    getLoc = loc.geocode(address)  
    latitude, longitude = getLoc.latitude, getLoc.longitude
    state = latlong_to_state(latitude, longitude)
    return {"Address": address, "longitude": longitude, "latitude": latitude, "State": state}

# Helper function to convert latitude and longitude to a state name
def latlong_to_state(latitude, longitude):
    location = loc.reverse((latitude, longitude), exactly_one=True)
    if location:
        address = location.raw['address']
        state = address.get('state', '')
        return state
    else:
        return "State not found"

# Function to scrape event data from Eventbrite based on state
def scrape_event_data(state):
    url = f"https://eventbrite.com/d/{state}/politics-and-government/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
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

# Function to get event information based on address and limit to top 5
def get_local_events(address):
    info = long_lat_state(address)
    state = info["State"]
    events = scrape_event_data(state)
    return events[:5]  # Return only the top 5 events

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
