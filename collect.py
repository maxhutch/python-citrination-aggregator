#!/bin/env python2
import time
from citrination_client import CitrinationClient
from json import dumps, dump
from string import rstrip

with open("./.api_key", "r") as f:
    key = f.readline().split()[0]
client = CitrinationClient(key, 'http://citrination.com/')

with open("./properties.lst", "r") as f:
    properties_in = f.readlines()

properties = [rstrip(x) for x in properties_in if x[0] != "#"]

start_prop = "Density"
index = properties.index(start_prop)
properties = properties[index:]

def collect_property(prop):
    size = 1
    start = 0
    max_records = 20000000
    records = []
    print "Searching for " + prop
    while size > 0 and start < max_records:
        r = client.search(property=prop, from_record=start, per_page=100)
        size = len(r.json()['results'])
        records += (r.json()['results'])
        start += size
        time.sleep(3) # Remember to sleep to avoid rate limiting!
        print ".",
    print "\nCollected " + str(start) + " records for " + prop
    return records

for prop in properties:
    records = collect_property(prop)
    with open(prop.replace(" ","") + ".json", "w") as f:
        dump(records, f)

"""
record_contents = []
for j in range(len(records)):
    names = []
    for i in range(len(records[j]['sample']['measurement'])):
        names.append(records[j]['sample']['measurement'][i]['property']['name'])
    record_contents.append(names)
"""


