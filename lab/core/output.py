import texttable
from tabulate import tabulate
from .functions import dataSanityCheck
from datetime import date
from ..redisdb.controller import rdb_save_output
import colored
from colored import stylize
import sys
import csv
import os


def setWidths(data, w='default'):
    """ 
    Parameters
    ----------
    data :  dict|list
    """
    if (w == 'default'):
        w = 3
    if (type(data) == dict):
        widths = []
        for word in data.keys():
            length = len(word)
            if ((w != 3) or (length < 5)):
                length = length * w
            widths.append(length)
        return widths
    if (type(data) == list):
        widths = []
        for word in data:
            length = len(word)
            if ((w != 3) or (length < 5)):
                length = length * w
            widths.append(length)
        return widths
    return False


def printFullTable(data, struct='list', widths='default'):
    """ 
    Parameters
    ----------
    data :  dict
    """
    print("\n")
    table = texttable.Texttable()
    if (struct == 'list' and type(data) == list):
        headers = data.pop(0)
        table.header(headers)
        table.set_cols_width(setWidths(headers, widths))
        for r in data:
            table.add_rows([r], header=False)
    if (struct == 'dictlist' and type(data[0]) == dict):
        headers = list(data[0].keys())
        table.header(headers)
        table.set_cols_width(setWidths(headers, widths))
        for r, d in enumerate(data):
            table.add_rows([d.values()], header=False)

    print(table.draw())


def printTable(data, widths='default'):
    """ 
    Parameters
    ----------
    data :  dict
    """
    print("\n")
    headers = data.keys()
    table = texttable.Texttable()
    table.header(headers)
    table.set_cols_width(setWidths(data, widths))
    table.add_rows([data.values()], header=False)

    print(table.draw())


def printTabs(data, headers=[], tablefmt='simple'):
    """ 
    Parameters
    ----------
    data     :  list of lists
                first list must be list headers
    tablefmt : string
                see https://pypi.org/project/tabulate/ for supported text formats
    """
    tabdata = []
    if (type(data) == dict):
        for h, v in data.items():
            tabrow = [h, v]
            tabdata.append(tabrow)
        print(tabulate(tabdata, headers, tablefmt))
    if (type(data) == list):
        tabdata = data
        print(tabulate(tabdata, headers, tablefmt))


def drawBox(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['???' + '???' * width + '???']
    for s in lines:
        res.append('???' + (s + ' ' * width)[:width] + '???')
    res.append('???' + '???' * width + '???')
    return '\n'.join(res)


def listTable(data):
    dash = '-' * 40
    for i in range(len(data)):
        if i == 0:
            print(dash)
            print('{:<10s}{:>4s}{:>12s}'.format(data[i][0], data[i][1], data[i][2]))
            print(dash)
        else:
            print('{:<10s}{:>4s}{:>12.1f}'.format(data[i][0], data[i][1], data[i][2]))


# Data must be list of dicts
def writeCSV(data, output, append=False):
    if (not os.path.exists(output) or (append == False)):
        with open(output, mode='w') as resultsfile:
            write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            write_results.writerow(
                data[0].keys()
            )
            for row in data:
                write_results.writerow(
                    row.values()
                )
        return
    else:
        with open(output, mode='a') as resultsfile:
            write_results = csv.writer(resultsfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in data:
                write_results.writerow(
                    row.values()
                )
        return

