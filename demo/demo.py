#!/usr/bin/env python3

import pandas as pd
import pytexmex as tm

otu = pd.read_table('../data/pmaseq.txt')
n = otu['154']
fit = tm.poilog_fit(n)

print(fit)
