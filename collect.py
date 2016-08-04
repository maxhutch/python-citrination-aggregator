#!/bin/env python2
import time
from citrination_client import CitrinationClient
from json import dumps, dump

with open("./.api_key", "r") as f:
    key = f.readline().split()[0]
client = CitrinationClient(key, 'http://citrination.com/')

size = 1
start = 0
max_records = 100
records = []
while size > 0 and start < max_records:
  #r = client.search(property="Thermoelectric figure of merit (zT)", from_record=start, per_page=100)
  r = client.search(property="Internal energy", from_record=start, per_page=100)
  size = len(r.json()['results'])
  records += (r.json()['results'])
  start += size
  print "Adding data: ", size
  time.sleep(3) # Remember to sleep to avoid rate limiting!
print "Found ", str(start), " records"

all_keys = []
for j in range(len(records)):
    for i in range(len(records[j]['sample']['measurement'])):
        all_keys.append(records[j]['sample']['measurement'][i]['property']['name'])

counts = {}
for k in all_keys:
    if k in counts:
        counts[k] += 1
    else:
        counts[k] = 1

"""
print dumps(counts, indent=2)
with open("counts.json", "w") as f:
    dump(counts, f)
"""
