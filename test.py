import requests

lst = [{'address': {'locationName': 'San Clemente Outlets, Suite 505', 'line1': '101 West Avenida Vista Hermosa', 'city': 'San Juan Capistrano', 'state': 'CA', 'zip': '92672'}, 'notes': 'Same Day Voter Registration available;  Suite 505', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}, {'address': {'locationName': 'San Clemente Community Center', 'line1': '100 N Calle Seville', 'city': 'San Clemente', 'state': 'CA', 'zip': '92672'}, 'notes': 'Same Day Voter Registration available;', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}, {'address': {'locationName': 'San Clemente Library', 'line1': '242 Avenida Del Mar', 'city': 'San Clemente', 'state': 'CA', 'zip': '92672'}, 'notes': 'Same Day Voter Registration available;', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}, {'address': {'locationName': 'The Volare Resort', 'line1': '111 S Avenida De La Estrella', 'city': 'San Clemente', 'state': 'CA', 'zip': '92672'}, 'notes': 'Same Day Voter Registration available;', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}, {'address': {'locationName': 'Community Center at The Market Place, 2nd floor', 'line1': '2961 El Camino Real', 'city': 'Tustin', 'state': 'CA', 'zip': '92782'}, 'notes': 'Same Day Voter Registration available;', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}]
newlst = []

for line in lst:
    geocode_json = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key' : 'AIzaSyCALOx3a43D4qa6l_2R9YJPAPF43A4NnjA', 
            'address' : f"{line['address']['line1']}, {line['address']['city']}"})
    newlst.append(geocode_json.json()['results'][0]['geometry']['location'])

print(newlst)