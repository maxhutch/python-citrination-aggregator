#!/bin/env python2
from json import dumps, load
from textwrap import wrap
import matplotlib.pyplot as plt
import operator
import numpy as np
from sys import argv
import pickle

def my_str(foo, wrap=40):
    ans = "["
    slen = 1
    for k in foo:
        if slen > 1 and slen + len(str(k)) > wrap:
            ans += "\n"
            slen = 0 
        slen += len(str(k))
        ans += str(k) + "|"
    return ans + "]"

with open(argv[1], "r") as f:
    contents = load(f)

set_contents = [frozenset(x) for x in contents]
keysets = set(set_contents)
keyset_counts = {}
for keyset in keysets:
    keyset_counts[keyset] = set_contents.count(keyset)

key_counts = {}
for keyset in keysets:
    for k in keyset:
        if k in key_counts:
            key_counts[k] += keyset_counts[keyset]
        else:
            key_counts[k] = keyset_counts[keyset]

with open("{}-raw.p".format(argv[1][:-5]), 'wb') as f:
    pickle.dump({"key_counts": key_counts, "keyset_counts" : keyset_counts}, f)


