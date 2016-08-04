#!/bin/env python2
from json import dumps, load
import matplotlib.pyplot as plt
import operator

with open("counts.json", "r") as f:
    counts = load(f)

import pandas
counts = [x for x in counts.items() if x[1] > 100]
sorted_x = dict(sorted(counts, key=operator.itemgetter(1)))
print dumps(sorted_x, indent=2)

df = pandas.DataFrame.from_dict(sorted_x, orient='index')
ax = df.plot(kind='bar')
plt.tight_layout()
ax.get_figure().savefig('foo.png')

