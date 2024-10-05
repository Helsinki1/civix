#curl \
#  -H 'Content-Type: application/json' \
#  -d '{"contents":[{"parts":[{"text":"Explain how AI works"}]}]}' \
#  -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBCQXD1NjxM2z1V7_m9qv8CLhFdFb-FDl0'

from dotenv import load_dotenv
import google.generativeai as genai
import os
import requests

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
CIVIC_API_KEY = os.getenv('CIVIC_API_KEY')

# valid offices: executiveCouncil, governmentOfficer, headOfGovernment, 
#               headOfState, legislatorLowerBody, legislatorUpperBody
def findReps (address, office):
    params = {"key": CIVIC_API_KEY, "address": address, "roles": office}
    info = requests.get("https://www.googleapis.com/civicinfo/v2/representatives", params=params)
    if info.status_code == 200: 
        return info.json()
    else:
        print("civics api request failed")
        return None


def decideRegion (position):
    if position=="Senate" or position=="House of Representatives" or position=="President": 
        return "National"
    else:
        return "Local"

def listStances (repName, region):
    if region == "National":
        issues = ["Fighting Poverty and Unemployment",
                "Taxes for Each Income Bracket",
                "Accessible Healthcare",
                "Education",
                "Climate Crisis",
                "LGBTQ+ Rights",
                "International Relations",
                "Immigration"]
    else: 
        issues = ["Fighting Poverty and Unemployment",
                "Affordable Housing",
                "Education",
                "Climate Crisis",
                "Law Enforcement"]

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    responses = []
    for issue in issues:
        responses.append(issue +": "+ model.generate_content("Explain "+repName+"'s stance on "+issue+" in 10 to 15 words").text)

    return responses

print(findReps("340 Main St, Venice, CA 90291", "legislatorLowerBody"))

#for response in listStances("Timothy M Cain", decideRegion("Senate")):
#    print(response)
