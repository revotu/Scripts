#!/srv/www/work/counterfeit/env python3
# -*- coding: utf-8 -*-
from openpyxl import load_workbook


keys = [1, 2, 3]
values = ['A', 'B', 'C']
extras = ['+', '-', '=']
print(zip(keys, values, extras))

print(zip(keys, values))

print(zip(keys))

d = dict(zip(keys, values))
print(d)

for k, v in d.iteritems():
    print(k, v)


keys = [1, 2, 3]
values = ['A', 'B', 'C']

d = dict(zip(keys, values))
print(d)


keys = [1, 2, 3]
values = ['A', 'B', 'C']

d = {}
for i, key in enumerate(keys):
    d[key] = values[i]
print(d)