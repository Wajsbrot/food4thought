# -*- coding:utf-8 -*-
"""
Created on the 10/03/2017
@author: Nicolas Thiebaut
@email: nkthiebaut@gmail.com
"""

import json
import pandas as pd
from glob import glob


def convert(x):
    ''' Convert a json string to a flat python dictionary
    which can be passed into Pandas. '''
    ob = json.loads(x)
    for k, v in ob.items():
        if isinstance(v, list):
            ob[k] = ','.join(v)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                ob['%s_%s' % (k, kk)] = vv
            del ob[k]
    return ob

convert_files = ['data/yelp_academic_dataset_business.json',
                 'data/yelp_academic_dataset_review.json']

for json_filename in convert_files:
    csv_filename = '%s.csv' % json_filename[:-5]
    print('Converting %s to %s' % (json_filename, csv_filename))
    df = pd.DataFrame([convert(line) for line in 
                       open(json_filename, 'r').readlines()])
    df.to_csv(csv_filename, encoding='utf-8', index=False)
