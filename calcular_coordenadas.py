
import csv
import numpy as np

nodes_lookup = {}  # node_id : [latitude, longitude]
preco_lookup = {}
ways = []

with open('vv_nodes.csv') as file:
    for node in csv.DictReader(file):
        nodes_lookup[node['id']] = [node['latitude'], node['longitude']]


with open('precos.csv') as file:
    for preco in csv.DictReader(file):
        preco_lookup[preco['cep']] = int(preco['valor'].replace('.', ''))


with open('vv_ways.csv') as file:
    for way in csv.DictReader(file):
        ways.append(way)


for way in ways:
    node_ids = way['nodes'].split(';')
    way['nodes'] = [nodes_lookup[node_id] for node_id in node_ids]
    way['postal_code'] = way['postal_code'].replace('-', '')

with open('dataset.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['latitude', 'longitude', 'preco', 'subject'])
    for way in ways:
        mean_cords = np.array(way['nodes'], dtype='f').mean(axis=0)
        try:
            writer.writerow([
                mean_cords[0],
                mean_cords[1],
                preco_lookup[way['postal_code']],
                ])
        except KeyError:
            continue
            # print(way['postal_code'])
