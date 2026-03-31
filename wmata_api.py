import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "649bc6ab4b8f4af1925634bff6382e52" #<YOUR_API_KEY_HERE>
INCIDENTS_URL = "https://api.wmata.com/Incidents.svc/json/ElevatorIncidents"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):

    # create an empty list called 'incidents'
    incidents = []
    # use 'requests' to do a GET request to the WMATA Incidents API
    # retrieve the JSON from the response
    wmata_responses = requests.get(INCIDENTS_URL, headers=headers)
    # iterate through the JSON response and retrieve all incidents matching 'unit_type'

    for response in wmata_responses.json()["ElevatorIncidents"]:

        if response["UnitType"] == unit_type.upper():

            # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
            response_to_add = {"StationCode":response["StationCode"], \
                               "StationName":response["StationName"],\
                               "UnitType":response["UnitType"],\
                               "UnitName":response["UnitName"]}

            #   -StationCode, StationName, UnitType, UnitName
            # add each incident dictionary object to the 'incidents' list
            incidents.append(response_to_add.copy())
    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents)
if __name__ == '__main__':
    app.run(debug=True)
