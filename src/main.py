from flask import Flask, render_template, request
from flask.typing import ResponseClass
import requests
from config import API_KEY

app = Flask(__name__)

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        address = request.form['address']
        election_info, polling_locations = get_election_info(address)
        # Slice the first 5 polling locations
        top_5_locations = polling_locations[:5]
        return render_template('index.html', election_info=election_info, polling_locations=top_5_locations, address=address)
    return render_template('index.html', election_info=None, polling_locations=None)

# Function to call Google Civic Information API for election day and polling locations
def get_election_info(address):
    url = "https://www.googleapis.com/civicinfo/v2/voterinfo"
    query_params = {"key": API_KEY, "address": address, 'electionId': 2000}
    response = requests.get(url, params=query_params)
    print(ResponseClass)

    if response.status_code == 200:
        data = response.json()
        election_day = data.get('election', {}).get('electionDay')
        polling_locations = data.get('pollingLocations', [])
        return {'election_day': election_day}, polling_locations
    else:
        return None, []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
