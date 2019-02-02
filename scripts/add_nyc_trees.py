import csv
import requests

FILE_NAME = '2015_Street_Tree_Census_-_Tree_Data.csv'
TREE_URL = 'http://127.0.0.1:5000/tree/'
SPECIES_URL = 'http://127.0.0.1:5000/species/'

USER_ID = '**NYC Street Tree Map'

print('Getting the species in the database')
res = requests.get(SPECIES_URL)
species = res.json()
species_dict = { s['name']: s['id'] for s in species }



tree_list = []
print('Opening the CSV')
counter = 0
with open(FILE_NAME, newline='') as csvfile:
    tree_census_reader = csv.reader(csvfile, delimiter=',')
    tree_census_reader.__next__()
    for row in tree_census_reader:
        species = row[9]
        if species:
            if species not in species_dict:
                print(f'Species "{species}" not found in species_dict. Exiting')
                exit()
            species_id = species_dict[species]
            latitude = float(row[37])
            longitude = float(row[38])
            tree_list.append({
                'latitude': latitude,
                'longitude': longitude,
                'user_id': USER_ID,
                'species_votes': [{
                    'user_id': USER_ID,
                    'species_id': species_id,
                }],
            })
        counter += 1
        if counter % 50000 == 0:
            print(f'... {counter} lines read')
print(f'Done. {counter} lines read')

print('Now adding the species')

counter = 0
failures = 0
for tree in tree_list:

    response = requests.post(
        TREE_URL,
        json=tree
    )
    if response.status_code == 200 or response.status_code == 201:
        counter += 1
    else:
        failures += 1

    break
    if (counter + failures) % 10 == 0:
        print(f'... {counter} species added, {failures} failed')
print(f'Done. {counter} species added, {failures} failed')
