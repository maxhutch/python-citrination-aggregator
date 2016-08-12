#!/bin/env python2
from json import dumps, load
from textwrap import wrap
import matplotlib.pyplot as plt
import operator
import numpy as np
from sys import argv

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

import pandas
keyset_counts = dict([x for x in keyset_counts.items() if x[1] > 100])
key_counts = dict([x for x in key_counts.items() if x[1] > 100])
#sorted_x = dict(sorted(counts, key=operator.itemgetter(1)))
#print dumps(sorted_x, indent=2)

M = len(key_counts)
indM = np.arange(M)

plt.figure()
plt.bar(indM, key_counts.values())
plt.xticks(indM+.5, key_counts, rotation=90)
plt.tight_layout()
plt.savefig("keys.png")


full_labels = [my_str(x) for x in keyset_counts]
#labels = [ '\n'.join(wrap(l, 20)) for l in full_labels ]
labels = full_labels

N = len(keyset_counts)
ind = np.arange(N)

plt.figure()
plt.bar(ind, keyset_counts.values())
plt.xticks(ind + .5, labels, rotation=90)
plt.tight_layout()
plt.savefig("keysets.png")

