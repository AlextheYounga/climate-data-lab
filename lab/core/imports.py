from datetime import datetime
import sys
import json
import csv



def parseCSV(path, fullPath=False, headers=True):
    """
    Parameters
    ----------
    path     : string
               filename or complete file path if fullPath is set to true
    fullPath : boolean
    headers  : boolean
               if set to true, parser will use values in first line as dict keys

    Returns
    -------
    dict
        CSV values converted to dict
    """

    csv_path = 'lab/core/storage/{}'.format(path)
    if (fullPath == True):
        csv_path = path
    with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
        asset_data = []


        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader):
            asset_data.append(row)

        return asset_data


def readJson(filepath):
    with open(filepath) as jsonfile:
        json_data = json.loads(jsonfile.read())

    return json_data
