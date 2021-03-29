#!/usr/bin/env python3

import time
import sys
import os
import requests
import numpy as np
import datetime as dt
from PIL import Image
from lib import weather

def readOptions(filename):
    if os.path.isfile(filename):
        try:
            f = open(filename, 'r')
            #print ("Reading options file")
            for line in f:
                if len(line) > 2:
                    # split on the first '=' only
                    s = line[:len(line) - 1].split('=', 1)
                    value = s[1][:len(s[1])]
                    if s[0] == 'weatherKey':
                        weatherKey = value
                    elif s[0] == 'weatherBaseurl':
                        weatherBaseurl = value
                    elif s[0] == 'weatherZip':
                        weatherZip = value
                    elif s[0] == 'weatherModifiers':
                        weatherModifiers = value
        except IOError:
            print ("Failure reading options file")
        except IndexError:
            print ("Error in options.ini: " + line)
        finally:
            f.close()
    else:
        print ("Unable to find options.ini file 2")
    return weatherKey, weatherBaseurl, weatherZip, weatherModifiers

def runWeather(filename):
    #get weather settings from options file
    weatherKey, weatherBaseurl, weatherZip, weatherModifiers = readOptions(filename)
    #put weather url together
    weatherUrl = weatherBaseurl+"?key="+weatherKey+"&q="+weatherZip+"&"+weatherModifiers
    #call weather url and return json data
    weather_json_data = weather.get_weather(weatherUrl)

    return weather_json_data


