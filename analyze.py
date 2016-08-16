#!/bin/env python2
from json import dumps, load
from textwrap import wrap
import matplotlib.pyplot as plt
import operator
import pickle
import numpy as np
from sys import argv

def my_str(foo, wrap=40):
    ans = unicode("[")
    slen = 1
    for k in foo:
        if slen > 1 and slen + len(unicode(k)) > wrap:
            ans += unicode("\n")
            slen = 0 
        slen += len(unicode(k))
        ans += unicode(k) + unicode("|")
    return ans + unicode("]")

def merge_counts(old, new):
    for k in new:
        if k in old:
            old[k] += new[k]
        else:
            old[k] = new[k]

key_counts = {}
keyset_counts = {}
for fname in argv[1:]:
    with open(fname, "rb") as f:
        data = pickle.load(f)
        merge_counts(key_counts, data["key_counts"])
        merge_counts(keyset_counts, data["keyset_counts"])


import pandas
keyset_list = sorted(keyset_counts.items(), key=operator.itemgetter(1))
key_list = sorted(key_counts.items(), key=operator.itemgetter(1))
keyset_list.reverse()
key_list.reverse()
#sorted_x = dict(sorted(counts, key=operator.itemgetter(1)))
#print dumps(sorted_x, indent=2)

M = 20 #len(key_counts)
indM = np.arange(M)

plt.figure()
plt.bar(indM, [x[1] for x in key_list][0:M])
plt.xticks(indM+.5, [x[0] for x in key_list][0:M], rotation=90)
plt.tight_layout()
plt.savefig("keys.png")


full_labels = [my_str(x[0]) for x in keyset_list]
#labels = [ '\n'.join(wrap(l, 20)) for l in full_labels ]
labels = full_labels

N = 5 #len(keyset_counts)
ind = np.arange(N)

plt.figure()
plt.bar(ind, [x[1] for x in keyset_list][0:N])
plt.xticks(ind + .5, labels[0:N], rotation=90)
plt.tight_layout()
plt.savefig("keysets.png")


