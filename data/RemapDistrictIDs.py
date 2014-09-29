__author__ = 'Petriau'
import json
import csv

# read in the mapping dictionary
mappingFile = ("India_new_district_mapping.csv")
with open(mappingFile, 'r') as dictFile:
    reader = csv.reader(dictFile)
    mapping = {rows[0]:rows[1] for rows in reader}



inputFile = "india_newest_districts.txt"

data = []
with open(inputFile, 'r+') as f:
    for line in f:
        keyStart = '"id":'
        for key in mapping:
           line = line.replace(keyStart + key + ",", keyStart + '"' +  mapping[key]+ '",')

line.strip('\\')

#jsonFile = open(inputFile, "r")
#data = json.load(jsonFile)

#for line in data:
 #   print line

#jsonFile.close()

with open("bob.json", "w") as jsonFile:
    jsonFile.write(json.dumps(line))

