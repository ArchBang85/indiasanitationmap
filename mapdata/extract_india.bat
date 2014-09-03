REM !/bin/sh

REM extract just Indian districts into subunits.json

REM # convert to topojson (saves lots of space) and drop lots of properties
topojson ^
    --id-property 'HASC^2' ^
    -p name=NAME^2 ^
    -p name ^
    -o india.json ^


REM # make a readable version of the json
type india.json | python -mjson.tool > india.pp.json

exit 0


    # -where "continent IN ('Africa')" \
    # -where "ISO^A2 IN ('DZ', 'EG', 'EH', 'LY', 'MA', 'SD', 'SS', 'TN')" \
    # -where "ADM0^A3 IN ('ZAF', 'MWI', 'DZA', 'EGY', 'TGO', 'SEN')" \

    #'DZ', 'EG', 'EH', 'LY', 'MA', 'SD', 'SS', 'TN',
    #'BF', 'BJ', 'CI', 'CV', 'GH', 'GM', 'GN', 'GW', 'LR', 'ML', 'MR', 'NE', 'NG', 'SH', 'SL', 'SN', 'TG',
    #'AO', 'CD', 'ZR', 'CF', 'CG', 'CM', 'GA', 'GQ', 'ST', 'TD',
    #'BI', 'DJ', 'ER', 'ET', 'KE', 'KM', 'MG', 'MU', 'MW', 'MZ', 'RE', 'RW', 'SC', 'SO', 'TZ', 'UG', 'YT', 'ZM', 'ZW',
    #'BW', 'LS', 'NA', 'SZ', 'ZA',

    # names from inaspsite, country^pages/geochart^data.py
    # Northern Africa
    #'015': set(['DZ', 'EG', 'EH', 'LY', 'MA', 'SD', 'SS', 'TN']),
    # Western Africa
    #'011': set(['BF', 'BJ', 'CI', 'CV', 'GH', 'GM', 'GN', 'GW', 'LR', 'ML', 'MR', 'NE', 'NG', 'SH', 'SL', 'SN', 'TG']),
    # Middle Africa
    #'017': set(['AO', 'CD', 'ZR', 'CF', 'CG', 'CM', 'GA', 'GQ', 'ST', 'TD']),
    # Eastern Africa
    #'014': set(['BI', 'DJ', 'ER', 'ET', 'KE', 'KM', 'MG', 'MU', 'MW', 'MZ', 'RE', 'RW', 'SC', 'SO', 'TZ', 'UG', 'YT', 'ZM', 'ZW']),
    # Southern Africa
    #'018': set(['BW', 'LS', 'NA', 'SZ', 'ZA']),
