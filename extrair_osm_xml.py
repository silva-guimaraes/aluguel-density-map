from xml.sax import parse
from xml.sax.handler import ContentHandler
import csv

print("é capaz que isso leve alguns minutos...")


class handler(ContentHandler):

    ways = []
    nodes = []
    current_way = {}

    def startElement(self, name, attrs):
        match name:
            case "node":
                node = {
                        "id": attrs["id"],
                        "lat": attrs["lat"],
                        "lon": attrs["lon"],
                }
                self.nodes.append(node)
            case "way":
                self.current_way = {
                    "id": attrs["id"],
                    "nodes": [],
                }
            case "nd":
                if self.current_way is None:
                    return
                self.current_way["nodes"].append(attrs["ref"])
            case "tag":
                if self.current_way is None:
                    return
                self.current_way[attrs["k"]] = attrs["v"]

    def endElement(self, name):
        if name != "way":
            return
        self.ways.append(self.current_way)
        self.current_way = None


foo = handler()
parse("./mapa.xml", foo)

foo.ways = [i for i in foo.ways if "highway" in i]

# print(foo.ways)

with open("vv_ways.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
            ["id", "name", "alt_name", "highway", "surface",
             "postal_code", "nodes"])

    for way in foo.ways:
        name = way["name"] if "name" in way else ""
        alt_name = way["alt_name"] if "alt_name" in way else ""
        highway = way["highway"] if "highway" in way else ""
        surface = way["surface"] if "surface" in way else ""
        postal_code = way["postal_code"] if "postal_code" in way else ""
        nodes = ';'.join(way["nodes"])

        writer.writerow([way["id"], name, alt_name, highway, surface,
                         postal_code, nodes])

with open("vv_nodes.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["id", "latitude", "longitude"])

    for way in foo.nodes:
        writer.writerow([way["id"], way["lat"], way["lon"]])
