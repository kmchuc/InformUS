import os
import requests

api_key = os.environ['api_key']

def civic_to_maps(full_address):

    # The payload will replace parameters within the API request url
    payload = {'key' : api_key,
                'address' : full_address}

    # Assigning the GET API request to voting_json variable 
    voting_json = requests.get('https://www.googleapis.com/civicinfo/v2/voterinfo', params=payload)

    #Jsonifys the get request you make from API using input parameters from form
    voting_json = voting_json.json()

    #Assigns polling_locations to the pollingLocations value in the voting_json dictionary 
    polling_locations = voting_json['pollingLocations']
    
    # Starting new list to put the addresses of the polling locations from json dictionary
    polling_addresses = []

    # Created a for loop to go through the json dictionary that selects the address line and city to make sure the latitutde and longitude are specific enough
    for line in polling_locations:
        geocode_json = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key' : api_key, 
            'address' : f"{line['address']['line1']}, {line['address']['city']}"})
        polling_addresses.append(geocode_json.json()['results'][0]['geometry']['location'])