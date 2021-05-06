import statistics
import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import pylab
import numpy as np
from scipy import stats
from ..core.functions import chunks, extract_data
from ..core.imports import readJson
from ..core.data import data_route
import math


def graph_climate_data(dataset):
    data = readJson(data_route(dataset))

    dates = list(reversed(extract_data(data, 'Date', queryKey=['Source', 'GCAG'])))
    means = list(reversed(extract_data(data, 'Mean', queryKey=['Source', 'GCAG'])))

    fig = plt.subplots(figsize=(12, 7))

    x = dates
    y = means

    plt.plot(x, y, label='Value')
    plt.xlabel('x Date')
    plt.title('Average Global Temperatures')
    plt.xticks(np.arange(0, len(x)+1, 126))
    plt.xticks(rotation=45)

    plt.draw()
    plt.pause(1)
    input("<Hit Enter To Close>")
    plt.close()
