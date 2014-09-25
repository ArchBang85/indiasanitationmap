#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert the WashWatch spreadsheet into our JSON format

Usage:
    xls2json.py [--verbose] <xlsPercentFile> <xlsAbsoluteFile>
    xls2json.py (-h | --help)

Options:
    -h --help       Show this screen
    -v --verbose    Output verbose javascript
"""

# script to read in Excel spreadsheet and spit out the json format we
# need

from __future__ import unicode_literals

pfile = "C:\\Users\\Petriau\\Downloads\\indiasanitationmap\\data\\book2.xls"
        #mapdata_india_sanitation_states_new3.xlsx"
afile = "C:\\Users\Petriau\\Downloads\\indiasanitationmap\\data\\mapdata3.xlsx"

import json
import sys

from docopt import docopt
import xlrd

# The below maps the state / district names to codes that match what's in the map file
NAME_CODE = {

	"Andaman & Nicobar Islands":"IN.AN",
	"Andhra Pradesh":"IN.AP",
	"Arunachal Pradesh":"IN.AR",
	"Assam":"IN.AS",
	"Bihar":"IN.BR",
	"Chandigarh":"IN.CH",
	"Chhattisgarh":"IN.CT",
	"Dadra & Nagar Haveli":"IN.DN",
	"Daman & Diu":"IN.DD",
	"Delhi":"IN.DL",
	"Goa":"IN.GA",
	"Gujarat":"IN.GJ",
	"Haryana":"IN.HR",
	"Himachal Pradesh":"IN.HP",
	"Jammu & Kashmir":"IN.JK",
	"Jharkhand":"IN.JH",
	"Karnataka":"IN.KA",
	"Kerala":"IN.KL",
	"Lakshadweep":"IN.LD",
	"Madhya Pradesh":"IN.MP",
	"Maharashtra":"IN.MH",
	"Manipur":"IN.MN",
	"Meghalaya":"IN.ML",
	"Mizoram":"IN.MZ",
	"Nagaland":"IN.NL",
	"Odisha":"IN.OR",
	"Puducherry":"IN.PY",
	"Punjab":"IN.PB",
	"Rajasthan":"IN.RJ",
	"Sikkim":"IN.SK",
	"Tamil Nadu":"IN.TN",
	"Telangana ":"",
	"Tripura":"IN.TR",
	"Uttar Pradesh":"IN.UP",
	"Uttarakhand":"IN.UT",
	"West Bengal":"IN.WB",

}

CODE_NAME = dict([(v, k) for k, v in NAME_CODE.items()])

# we want to limit the decimal precision of the percentage figures
# from http://stackoverflow.com/a/1733105/3189
class PrettyFloat(float):
    def __repr__(self):
        return '%.3f' % self

def pretty_floats(obj):
    if isinstance(obj, float):
        return PrettyFloat(obj)
    elif isinstance(obj, dict):
        return dict((k, pretty_floats(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return map(pretty_floats, obj)
    return obj


def add_data_for_cell(sheet, row, col, datadict, key):
    if sheet.cell_type(row, col) == xlrd.XL_CELL_NUMBER:
        datadict[key] = sheet.cell_value(row, col)


def process_percent_sheet(sheet, data):
    """ returns dictionary, key is country code, value is dictionary of
    year: value, or None if no data """
    col_key_mapping = [
        (6, 'indicator1_initial'),
        (7, 'indicator1_increase'),
        (8, 'indicator2_initial'),
        (9, 'indicator2_increase'),
        (10, 'indicator1_pop_current'),
        (11, 'indicator2_pop_current'),
        (12, 'indicator1_pop_universal'),
        (13, 'indicator2_change_needed'),
        (15, 'schools_without_toilets'),
        (16, 'no_toilet'),
        (17, 'subsidy_for_govt_schools_R'),
        (18, 'subsidy_for_govt_schools_Lakh'),
        (19, '%_of_noSuggestions_without_toilets'),
        (20, 'no_latrine'),
        (21, 'subsidy_for_anganwadi_toilets_R'),
        (22, 'subsidy_for_anganwadi_toilets_Lakh'),
        (23, 'required_complexes'),
        (24, 'subsidy_for_sanitary_complex_R'),
        (25, 'subsidy_for_sanitary_complex_Lakh'),
        (26, 'Access_to_IHHL_latrine'),
        (27, 'Cost_of_meeting_SBA_target_R'),
        (28, 'Cost_of_meeting_SBA_target_Lakh'),
        (29, 'Total_cost_of_SBA_R'),
        (30, 'Total_cost_of_SBA_Lakh'),
        (31, 'Total_cost_of_SBA_Crore'),

    ]

    for curr_row in xrange(1, sheet.nrows):
        country_name = sheet.cell_value(curr_row, 0)
        if country_name in NAME_CODE and NAME_CODE[country_name]:
            country_code = NAME_CODE[country_name]
        else:
            #print "%s not found" % country_name
            continue

        if country_code not in data:
            data[country_code] = {'name': CODE_NAME[country_code]}

        for col, key in col_key_mapping:
            add_data_for_cell(sheet, curr_row, col, data[country_code], key)

    return data


def process_absolute_sheet(sheet, data):
    """ returns dictionary, key is country code, value is dictionary of
    year: value, or None if no data """
    col_key_mapping = [
        (1, 'water_pop_current'),
        (2, 'water_pop_universal'),
        (3, 'sanitation_pop_current'),
        (4, 'sanitation_pop_universal')
    ]

    for curr_row in xrange(2, sheet.nrows):
        country_name = sheet.cell_value(curr_row, 0)
        if country_name in NAME_CODE and NAME_CODE[country_name]:
            country_code = NAME_CODE[country_name]
        else:
            #print "%s not found" % country_name
            continue

        if country_code not in data:
            data[country_code] = {'name': CODE_NAME[country_code]}

        for col, key in col_key_mapping:
            add_data_for_cell(sheet, curr_row, col, data[country_code], key)

    return data


def main(argv):
   # opts = docopt(__doc__, argv[1:])

    # somaliland has the label "-99" in the map data, and no data in the
    # spreadsheets, but we still want a label.
    data = {"-99": {"name": "Z"}}

    ## Consolidating to one sheet only
    #xls2json.py [--verbose] <xlsPercentFile> <xlsAbsoluteFile>
    percent_book = xlrd.open_workbook(argv[0])#opts['<xlsPercentFile>'])
    percent_sheet = percent_book.sheet_by_index(0)
    data = process_percent_sheet(percent_sheet, data)

    #absolute_book = xlrd.open_workbook(argv[1])#opts['<xlsAbsoluteFile>'])
    #absolute_sheet = absolute_book.sheet_by_index(0)
    #data = process_absolute_sheet(absolute_sheet, data)
   # bopts[0] = "--verbose"
    # limit float precision when printed
    data = pretty_floats(data)
   # if bopts['--verbose']:
        # pretty print the javascript
    print json.dumps(data, indent=4, sort_keys=True)
   # else:
        # compressed javascript
   #     print json.dumps(data, separators=(',', ':'))
    with open("output.txt", 'w') as outfile:
		json.dump(data, outfile)

	#return
#debugging
argvo = (pfile, afile)
main(argvo)


if __name__ == '__main__':
    #sys.exit(main(sys.argv))
    main(sys.argv)