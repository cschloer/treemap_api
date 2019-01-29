import csv
import requests

SPECIES_URL = 'http://127.0.0.1:5000/species/'
SPECIES_URL_URL = 'http://127.0.0.1:5000/speciesurl/'
#WIKIPEDIA_URL = 'https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch=%s'
WIKIPEDIA_URL = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=info&generator=allpages&inprop=url&gapfrom=%s&gaplimit=1'

response = requests.get(
    SPECIES_URL,
)
if response.status_code != 200 and response.status_code != 201:
    print('Failed to get the species')
    exit()
res_json = response.json()
print(f'Got {len(res_json)} species')
species_without_urls = []
for species in res_json:
    if not len(species['urls']):
        species_without_urls.append(species)
print (f'{len(species_without_urls)} species have no urls')

species_id_to_url = {}
counter = 0
for species in species_without_urls:
    if counter % 5 == 0:
        print(f'Gathered {counter} urls... Still working')
    wiki_response = requests.get(
        WIKIPEDIA_URL % species['name'],
    )
    wiki_res_json = wiki_response.json()
    results = wiki_res_json['query']['pages']
    if not len(results.keys()):
        print(f'No results found for {species["name"]}')
        continue
    new_url = results[list(results.keys())[0]]['fullurl']
    species_id_to_url[species['id']] = new_url
    counter += 1
    if counter == 1:
        break
print(f'Gathered {counter} total urls!')

counter = 0
failures = 0
for species_id, url in species_id_to_url.items():
    response = requests.post(
        SPECIES_URL_URL,
        json={
            'species_id': species_id,
            'url': url,
        }
    )
    if response.status_code == 200 or response.status_code == 201:
        counter += 1
    else:
        failures += 1

    if (counter + failures) % 10 == 0:
        print(f'... {counter} species urls added, {failures} failed')
print(f'Done. {counter} species urls added, {failures} failed')




