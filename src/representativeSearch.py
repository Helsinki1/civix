#curl \
#  -H 'Content-Type: application/json' \
#  -d '{"contents":[{"parts":[{"text":"Explain how AI works"}]}]}' \
#  -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBCQXD1NjxM2z1V7_m9qv8CLhFdFb-FDl0'

API_KEY = "AIzaSyBCQXD1NjxM2z1V7_m9qv8CLhFdFb-FDl0"

import google.generativeai as genai
import os

repName = "Timothy M Cain"
position = "Senate"
region = "National"
issues = []

if position=="Senate" or position=="House of Representatives" or position=="President": 
    region = "National"
    issues = ["Fighting Poverty and Unemployment",
                "Taxes for Each Income Bracket",
                "Accessible Healthcare",
                "Education",
                "Climate Crisis",
                "LGBTQ+ Rights",
                "International Relations",
                "Immigration"]
else: 
    region = "Local"
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

for response in responses:
    print(response)