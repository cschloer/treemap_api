import csv
import requests

FILE_NAME = '2015_Street_Tree_Census_-_Tree_Data.csv'
URL = 'http://127.0.0.1:5000/species/'

species_list = set()
latin_name_dict = {}
print('Opening the CSV')
counter = 0
with open(FILE_NAME, newline='') as csvfile:
    tree_census_reader = csv.reader(csvfile, delimiter=',')
    tree_census_reader.__next__()
    for row in tree_census_reader:
        species = row[9]
        if species:
            species_list.add(row[9])

            latin_name = row[8]
            if latin_name and species not in latin_name_dict:
                latin_name_dict[species] = latin_name
        counter += 1
        if counter % 50000 == 0:
            print(f'... {counter} lines read')
print(f'Done. {counter} lines read')

print('Now adding the species')

counter = 0
failures = 0
for species in species_list:

    response = requests.post(
        URL,
        json={
            'name': species,
            'latin_name': latin_name_dict[species],
        }
    )
    if response.status_code == 200 or response.status_code == 201:
        counter += 1
    else:
        failures += 1

    if (counter + failures) % 10 == 0:
        print(f'... {counter} species added, {failures} failed')
print(f'Done. {counter} species added, {failures} failed')
