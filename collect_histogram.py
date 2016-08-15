#!/bin/env python2
import time
from citrination_client import CitrinationClient
from json import dumps, dump, load
from string import rstrip

with open("./.api_key", "r") as f:
    key = f.readline().split()[0]
client = CitrinationClient(key, 'http://citrination.com/')

with open("./datasets.json", "r") as f:
    datasets = load(f)['ids']
print(len(datasets))

def collect_property(datasets, prop = None):
    max_records = 100000000
    records = []
    if prop is not None:
        print "Searching for " + prop
    for ds in datasets:
        size = 1
        start = 0
        while size > 0 and start < max_records:
            if prop is not None:
                r = client.search(property=prop, data_set_id=ds, from_record=start, per_page=100)
            else:
                r = client.search(data_set_id=ds, from_record=start, per_page=100)
            try:
                parsed = r.json()
            except ValueError:
                print "Failed on ", prop, ds, start
                continue

            size = len(parsed['results'])
            records += (parsed['results'])
            start += size
            time.sleep(3) # Remember to sleep to avoid rate limiting!
            print ".",
        if start == 10000:
            print "WARNING: topped out for ds=", str(ds)
    if prop is not None:
        print "\nCollected " + str(start) + " records for " + prop
    else:
        print "\nCollected " + str(start) + " records"
    return records

def recurse_names(obj):
    ans = []
    if isinstance(obj, dict):
        for k in obj.keys():
            if k == "name" :
                ans.append(obj["name"])
            else:
                ans = ans + recurse_names(obj[k])
    elif isinstance(obj, list):
        for o in obj:
            ans = ans + recurse_names(o)
    return ans

ndata = len(datasets)
block = 50
start = 1250
for i in range(start, ndata, block):
    rmin = i
    rmax = min(rmin+block, ndata)
    records = collect_property(datasets[rmin:rmax])
    record_contents = [recurse_names(x) for x in records]
    with open("./hist_data-{:09d}.json".format(rmin), "w") as f:
        dump(record_contents, f)

