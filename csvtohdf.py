import csv
import numpy as np
import pandas as pd
import json
import os
import sys
from datetime import datetime
import h5py


def parseData(file_path):
    contents = None
    try:
        with open(file_path, newline='') as fp:
            site, freq_start, step, lat, lon, data = csv.reader(fp,delimiter=' ')
        data = {
                "site": site[0],
                "freq_start": freq_start[0],
                "step": step[0],
                "lat-long": (np.float64(lat[0]),np.float64(lon[0])),
                "data": data
                }
        saveData(**data)
    except IOError as e:
        print(e)

def saveData(**kwargs):
    site = kwargs['site']
    date = kwargs['data'].pop(0)
    rssi = kwargs['data'][0].split(',')
    lat = kwargs['lat-long'][0]
    lon = kwargs['lat-long'][1]
    time = rssi.pop(0)
    rssi = np.array(rssi,dtype=np.float32)
    base_freq = np.float16(kwargs['freq_start'])
    step = float(kwargs['step'])/1000.0
    step = np.float16(step)
    
    with h5py.File('data.hdf5','a') as h5file:
        group = os.path.join(site,date,time)
        try:
            g = h5file.create_group(group)
        except ValueError as e:
            print(e)
            g = h5file[group]
        try:
            g.create_dataset("DATA",data=rssi)
            g.attrs["lat"] = lat
            g.attrs["lon"] = lon
            g.attrs["base_freq"] = base_freq
            g.attrs["step"] = step
        except:
            pass
