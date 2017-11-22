import gspread
import os
import json
import pandas as pd
import xml.etree.ElementTree as xml
import os
import plistlib
import csv
import time
import sys, os, getopt, csv, xml.etree.ElementTree as ET
from xml.dom import minidom

def install(pandas):
    pip.main(['install', pandas])
print("pandas installed")

from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('Desktop/Localisation_Updater/Client_Secret.json', scope)
client = gspread.authorize(creds)

# define workbook locations get_worksheets are subsheets in the same doc
iOS = client.open("Localisation").sheet1
Android = client.open("Localisation").get_worksheet(1)

#assign values locally
list_of_hashes = iOS.get_all_values()
list_of_hashes2= Android.get_all_values()

#create dataframe from api data
df = pd.DataFrame(list_of_hashes)
df2 = pd.DataFrame(list_of_hashes2)

#create directory to place data downloaded neatly
path = 'Desktop/Localisation2'
os.mkdir(path)

clock = time.strftime("%I:%M:%S\n")
calender = time.strftime("%d/%m/%Y")

with open("Desktop/Localisation2/ZLastUpdated.txt", "w") as text_file:
    text_file.write(clock)
    text_file.write(calender)

#converting fro df to csv
df.to_csv('Desktop/Localisation2/1_iOS.csv', index=False, header=False)
df2.to_csv('Desktop/Localisation2/1_Android.csv', index=False, header=False)

# -*- coding: utf-8 -*-
# Script takes a csv and creates strings for Android (.xml) and iOS (.Strings).
# csv in the format [key, language1, langauge2 ......]
# usage - Python converter.py [FILEPATH]

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

# Read in output directory
try:
    sys.argv[1:]
    fileDestination = sys.argv[1]
except IndexError:
    print "Error: Please supply an output directory."
    print "Usage: converter.py [FILEPATH]"
    sys.exit()

# Create directory if it doesn't exists
if not os.path.exists(fileDestination):
    os.makedirs(fileDestination)



# Read from csv
f = open('Desktop/Localisation2/1_iOS.csv')
csv_f = csv.reader(f)

# Determine the number of languages from the csv
line1 = csv_f.next()
numberOfLocales =  len(line1)

# Create strings for each language
for x in range(1, numberOfLocales):
    #Returns to the start of the csv and ignores the first line
    f.seek(0)
    csv_f.next()
    rowIndex = 0
    
    # Android xml
    resources = ET.Element("resources")
    
    # Create iOS strings file
    iOSFile = open(fileDestination+"/"+line1[x]+".Strings", "w+")
    
    for row in csv_f:
        ++rowIndex
        try:
            # Write string to xml
            ET.SubElement(resources, "string", name=row[0]).text = row[x].decode('utf-8')
            # Write string to iOS .Strings
            iOSFile.write("/*  */\n")
            iOSFile.write('"'+row[0]+'"'+ ' = ' + '"'+row[x]+'"' + ";\n")
            iOSFile.write("\n")
        except IndexError:
            f.seek(0)
            print "There is a problem with the csv file at row {}".format(rowIndex+1) + " with the language {}".format(line1[x])
            r = list(csv_f)
            print r[rowIndex]
            sys.exit()
    # Write to Android file
    androidFile = open(fileDestination+"/"+line1[x]+"_strings.xml", "w+")
    androidFile.write(prettify(resources).encode('utf-8'))

print(list_of_hashes)
print(list_of_hashes2)
print("Translation Files added")



