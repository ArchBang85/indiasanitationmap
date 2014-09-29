__author__ = 'Petriau'
import json
import csv

# Remaps the IDs in a map json file to what's given in a CSV file
# 29/09/2014 petriautio@wateraid.org

mappingFile = "India_new_district_mapping.csv"
inputFile = "india_newest_districts.txt"

# read in the mapping dictionary
with open(mappingFile, 'r') as dictFile:
    reader = csv.reader(dictFile)
    mapping = {rows[0]:rows[1] for rows in reader}

# read in the JSON mapfile
with open(inputFile, 'r+') as f:
    for line in f:
        keyStart = '"id":'
        for key in mapping:
           line = line.replace(keyStart + key + ",", keyStart + '"' +  mapping[key]+ '",')

with open("district_map_with_IDs.json", "w") as jsonFile:
    jsonFile.write(json.dumps(line))

# Might have to do some further formatting, i.e. remove outermost quotation marks in the output file and the backslashes