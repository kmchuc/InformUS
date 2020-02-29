import requests

# lst = [{'address': {'locationName': 'San Clemente Outlets, Suite 505', 'line1': '101 West Avenida Vista Hermosa', 'city': 'San Juan Capistrano', 'state': 'CA', 'zip': '92672'}, 'notes': 'Same Day Voter Registration available;  Suite 505', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}, {'address': {'locationName': 'San Clemente Community Center', 'line1': '100 N Calle Seville', 'city': 'San Clemente', 'state': 'CA', 'zip': '92672'}, 'notes': 'Same Day Voter Registration available;', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}, {'address': {'locationName': 'San Clemente Library', 'line1': '242 Avenida Del Mar', 'city': 'San Clemente', 'state': 'CA', 'zip': '92672'}, 'notes': 'Same Day Voter Registration available;', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}, {'address': {'locationName': 'The Volare Resort', 'line1': '111 S Avenida De La Estrella', 'city': 'San Clemente', 'state': 'CA', 'zip': '92672'}, 'notes': 'Same Day Voter Registration available;', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}, {'address': {'locationName': 'Community Center at The Market Place, 2nd floor', 'line1': '2961 El Camino Real', 'city': 'Tustin', 'state': 'CA', 'zip': '92782'}, 'notes': 'Same Day Voter Registration available;', 'pollingHours': 'Election Day: 7am - 8pm', 'sources': [{'name': 'Voting Information Project', 'official': True}]}]
# newlst = []

# for line in lst:
#     geocode_json = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key' : 'AIzaSyCALOx3a43D4qa6l_2R9YJPAPF43A4NnjA', 
#             'address' : f"{line['address']['line1']}, {line['address']['city']}"})
#     newlst.append(geocode_json.json()['results'][0]['geometry']['location'])

# for coord in newlst:
#     # for cor in coord.values():
#     #     print(cor)
#     # print(coord)
#     print((coord['lat'], coord['lng']))

# full_address = "990 Jackson Street San Francisco, CA 94133"
# coord = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params={'key' : 'AIzaSyCALOx3a43D4qa6l_2R9YJPAPF43A4NnjA', 
#             'address' : full_address})

# print(coord.json())

result = {'results': [{'address_components': [{'long_name': '990', 'short_name': '990', 'types': ['street_number']}, {'long_name': 'Jackson Street', 'short_name': 'Jackson St', 'types': ['route']}, {'long_name': 'Nob Hill', 'short_name': 'Nob Hill', 'types': ['neighborhood', 'political']}, {'long_name': 'San Francisco', 'short_name': 'SF', 'types': ['locality', 'political']}, {'long_name': 'San Francisco County', 'short_name': 'San Francisco County', 'types': ['administrative_area_level_2', 'political']}, {'long_name': 'California', 'short_name': 'CA', 'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United States', 'short_name': 'US', 'types': ['country', 'political']}, {'long_name': '94133', 'short_name': '94133', 'types': ['postal_code']}, {'long_name': '4827', 'short_name': '4827', 'types': ['postal_code_suffix']}], 'formatted_address': '990 Jackson St, San Francisco, CA 94133, USA', 'geometry': {'bounds': {'northeast': {'lat': 37.7958494, 'lng': -122.4113117}, 'southwest': {'lat': 37.7955003, 'lng': -122.411531}}, 'location': {'lat': 37.79572539999999, 'lng': -122.411464}, 'location_type': 'ROOFTOP', 'viewport': {'northeast': {'lat': 37.7970238302915, 'lng': -122.4100723697085}, 'southwest': {'lat': 37.7943258697085, 'lng': -122.4127703302915}}}, 'place_id': 'ChIJc1ucjPKAhYARzuxA69M6nBg', 'types': ['premise']}], 'status': 'OK'}

coordinate = result['results'][0]['geometry']['location']['lat']
print(coordinate)