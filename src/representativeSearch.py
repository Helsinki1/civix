#curl \
#  -H 'Content-Type: application/json' \
#  -d '{"contents":[{"parts":[{"text":"Explain how AI works"}]}]}' \
#  -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBCQXD1NjxM2z1V7_m9qv8CLhFdFb-FDl0'

from dotenv import load_dotenv
import google.generativeai as genai
import os
import time
import requests

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
CIVIC_API_KEY = os.getenv('CIVIC_API_KEY')

# valid offices: executiveCouncil, governmentOfficer, headOfGovernment, 
#               headOfState, legislatorLowerBody, legislatorUpperBody
def findReps (address, office):
    params = {"key": CIVIC_API_KEY, "address": address, "roles": office}
    info = requests.get("https://www.googleapis.com/civicinfo/v2/representatives", params=params)
    if info.status_code != 200:
        print("civics api request failed")
        return None

    info_json = info.json()

    officials = info_json.get('officials', [])
    name_and_party = []
    for official in officials:
        name_and_party.append(official.get('name') + " - " + official.get('party'))

    return name_and_party


def decideRegion (position):
    if position=="Senate" or position=="House of Representatives" or position=="President": 
        return "National"
    else:
        return "Local"

def listStances (repName, region):
    if region == "National":
        issues = ["Fighting Poverty and Unemployment, ",
                "Taxes for Each Income Bracket, ",
                "Accessible Healthcare, ",
                "Education, ",
                "Climate Crisis, ",
                "LGBTQ+ Rights, ",
                "Immigration"]
    else: 
        issues = ["Fighting Poverty and Unemployment, ",
                "Affordable Housing, ",
                "Education, ",
                "Climate Crisis, ",
                "Law Enforcement"]

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    responses = model.generate_content("Explain "+repName+"'s stances using (100 words) on these issues: "+"".join(issues)).text
    return responses

def summarize (repName):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content("Give me a description of this politican that includes their party and position in 15 words or less: "+repName)
    return response.text


def describeNearbyReps (address):
    reps = findReps(address, "legislatorUpperBody")
    summaries = []

    for rep in reps:
        summaries.append(summarize(rep) + listStances(rep, "National"))
    
    return reps, summaries



#print(describeNearbyReps("215 Oakwood Terrace Ct, Ballwin, MO 63021"))

#for response in listStances("Timothy M Cain", decideRegion("Senate")):
#    print(response)
