def civic_to_maps():
    # Get form variables and add to array
    street = request.form["street"]
    city = request.form["city"]
    state = request.form["state"]
    zipcode = request.form["zipcode"]

    #Rendered variables from form into a f format string
    full_address = f"{street} {city}, {state} {zipcode}"

    #the payload will replace parameters within the API request url
    payload = {'key' : api_key,
                'address' : full_address}

    #
    voting_json = requests.get('https://www.googleapis.com/civicinfo/v2/voterinfo', params=payload)

    #Jsonifys the get request you make from API using input parameters from form
    voting_json = voting_json.json()

    #Assigns polling_locations to the pollingLocations value in the voting_json dictionary 
    polling_locations = voting_json['pollingLocations']
    
    address_list = []

    for line in address_list:
        address_list.append(line['address']['line1'])
    
    newlst = []

    for line in lst:
        geocode_json = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key' : 'AIzaSyDSUxrguk0DawgTvSbouXhoHgWXzsCNxdI', 
            'address' : f"{line['address']['line1']}, {line['address']['city']}"})
        newlst.append(geocode_json.json()['results'][0]['geometry']['location'])