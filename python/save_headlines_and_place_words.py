import requests
import json
import re



target_path_headlines= '../data/json/headlines/'
target_path_placewords= '../data/json/placewords/'
absolute_json_file_path = '../data/json/city_count.json'

# read in cities and neighborhoods keys
with open(absolute_json_file_path) as json_file:
    text = json_file.read()
    json_data = json.loads(text)
    
for place in json_data['rows']:

	# Trim place name and format key
	place_key = place['key']
	place_key = str(place['key'])
	place_key = place_key.replace(" ''","{}").replace("'", '"')

	place_key_start = place_key
	place_key_end = place_key.replace(",{}","")

	place_name = re.sub(r'\W+', '', str(place_key)).lower()

	if "Boston" in place_key:
		place_key = place_key.replace('"Boston",','')
		place_key_end = place_key
		place_key_start = place_key.replace("]", ",{}]")


	# Place Words 
	#placewords_url = 'http://globe.mediameter.org:5984/boston-globe-articles/_design/nltk/_view/place_frequency?limit=1&skip=154&descending=true&endkey='+str(place_key)+'&startkey='+str(place_key)
	placewords_url = 'http://globe.mediameter.org:5984/boston-globe-articles/_design/nltk/_view/place_frequency'
	
	params = 'limit=1&skip=154&descending=true&endkey='+place_key_end+'&startkey='+place_key_start

	placewords_filepath = target_path_placewords + place_name + '.json'

	response = requests.get(placewords_url, stream=True, params=params)
	
	handle = open(placewords_filepath, "wb")
	for chunk in response.iter_content(chunk_size=512):
	    if chunk:  # filter out keep-alive new chunks
	        handle.write(chunk)

	# Headlines
	if "boston" in place_name:
		headlines_url = 'http://globe.mediameter.org:5984/boston-globe-articles/_design/globe/_view/headline_by_neighborhood_and_date'
	else:
		headlines_url = 'http://globe.mediameter.org:5984/boston-globe-articles/_design/globe/_view/headline_by_city_and_date'

	params = 'limit=100&descending=true&endkey='+place_key_end+'&startkey='+place_key_start

	headlines_filepath = target_path_headlines + place_name + '.json'

	response = requests.get(headlines_url, stream=True, params=params)
	print(response.url)

	handle = open(headlines_filepath, "wb")
	for chunk in response.iter_content(chunk_size=512):
	    if chunk:  # filter out keep-alive new chunks
	        handle.write(chunk)


