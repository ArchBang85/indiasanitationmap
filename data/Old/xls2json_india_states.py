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

import json
import sys

from docopt import docopt
import xlrd

# The below maps the state / district names to codes that match what's in the map file
	# "Algeria": "DZ",
    # "Angola": "AO",
    # "Benin": "BJ",
    # "Botswana": "BW",
    # "Burkina Faso": "BF",
    # "Burundi": "BI",
    # "Cameroon": "CM",
    # "Cape Verde": "CV",
    # "Central African Republic": "CF",
    # "Chad": "TD",
    # "Comoros": "KM",
    # "Congo": "CG",
    # "Côte d'Ivoire": "CI",
    # "Democratic Republic of the Congo": "CD",
    # "Djibouti": "DJ",
    # "Egypt": "EG",
    # "Equatorial Guinea": "GQ",
    # "Eritrea": "ER",
    # "Ethiopia": "ET",
    # "Gabon": "GA",
    # "Gambia": "GM",
    # "Ghana": "GH",
    # "Guinea": "GN",
    # "Guinea-Bissau": "GW",
    # "Kenya": "KE",
    # "Lesotho": "LS",
    # "Liberia": "LR",
    # "Libyan Arab Jamahiriya": "LY",
    # "Madagascar": "MG",
    # "Malawi": "MW",
    # "Mali": "ML",
    # "Mauritania": "MR",
    # "Mauritius": "MU",
    # "Mayotte": "YT",
    # "Morocco": "MA",
    # "Mozambique": "MZ",
    # "Namibia": "NA",
    # "Niger": "NE",
    # "Nigeria": "NG",
    # "Réunion": "RE",
    # "Rwanda": "RW",
    # "Sao Tome and Principe": "ST",
    # "Senegal": "SN",
    # "Seychelles": "SC",
    # "Sierra Leone": "SL",
    # "Somalia": "SO",
    # "Somaliland": "-99",
    # "South Africa": "ZA",
    # "South Sudan": "SS",
    # "Sub-Saharan Africa": "Africa",
    # "Sudan": "SD",
    # "Swaziland": "SZ",
    # "Togo": "TG",
    # "Tunisia": "TN",
    # "Uganda": "UG",
    # "United Republic of Tanzania": "TZ",
    # "Western Sahara": "EH",
    # "Zambia": "ZM",
    # "Zimbabwe": "ZW",
NAME_CODE = {

	"ANDAMAN & NICOBAR ISLANDS":"IN.AN",
	"ANDHRA PRADESH":"IN.AP",
	"ARUNACHAL PRADESH":"IN.AR",
	"ASSAM":"IN.AS",
	"BIHAR":"IN.BR",
	"CHANDIGARH":"IN.CH",
	"CHHATTISGARH":"IN.CT",
	"DADRA & NAGAR HAVELI":"IN.DN",
	"DAMAN & DIU":"IN.DD",
	"DELHI":"IN.DL",
	"GOA":"IN.GA",
	"GUJARAT":"IN.GJ",
	"HARYANA":"IN.HR",
	"HIMACHAL PRADESH":"IN.HP",
	"JAMMU & KASHMIR":"IN.JK",
	"JHARKHAND":"IN.JH",
	"KARNATAKA":"IN.KA",
	"KERALA":"IN.KL",
	"LAKSHADWEEP":"IN.LD",
	"MADHYA PRADESH":"IN.MP",
	"MAHARASHTRA":"IN.MH",
	"MANIPUR":"IN.MN",
	"MEGHALAYA":"IN.ML",
	"MIZORAM":"IN.MZ",
	"NAGALAND":"IN.NL",
	"ODISHA":"IN.OR",
	"PUDUCHERRY":"IN.PY",
	"PUNJAB":"IN.PB",
	"RAJASTHAN":"IN.RJ",
	"SIKKIM":"IN.SK",
	"TAMIL NADU":"IN.TN",
	"TELANGANA ":"",
	"TRIPURA":"IN.TR",
	"UTTAR PRADESH":"IN.UP",
	"UTTARAKHAND":"IN.UT",
	"WEST BENGAL":"IN.WB",

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
        (6, 'water_initial'),
        (7, 'water_increase'),
        (8, 'sanitation_initial'),
        (9, 'sanitation_increase')
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
    opts = docopt(__doc__, argv[1:])

    # somaliland has the label "-99" in the map data, and no data in the
    # spreadsheets, but we still want a label.
    data = {"-99": {"name": "Somaliland"}}

    #xls2json.py [--verbose] <xlsPercentFile> <xlsAbsoluteFile>
    percent_book = xlrd.open_workbook(opts['<xlsPercentFile>'])
    percent_sheet = percent_book.sheet_by_index(0)
    data = process_percent_sheet(percent_sheet, data)

    absolute_book = xlrd.open_workbook(opts['<xlsAbsoluteFile>'])
    absolute_sheet = absolute_book.sheet_by_index(0)
    data = process_absolute_sheet(absolute_sheet, data)

    # limit float precision when printed
    data = pretty_floats(data)
    if opts['--verbose']:
        # pretty print the javascript
        print json.dumps(data, indent=4, sort_keys=True)
    else:
        # compressed javascript
        print json.dumps(data, separators=(',', ':'))
    with open("output.txt", 'w') as outfile:
		json.dump(data, outfile)
		
	#return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
