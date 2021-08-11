import pathlib
import itertools
import pandas as pd
import numpy as np

import hash_directory


policies_dir = pathlib.Path(r'E:\policies_output')

quarters = [[f'{y}-{q}' for q in range(1, 5)] for y in range(2012, 2021)]
quarters = list(itertools.chain.from_iterable(quarters))

urls = pd.read_csv('datenschutz.urls.csv')

availability = np.zeros(shape=(len(urls.doc_id), len(quarters)))
for url_ind, url_row in urls.iterrows():
    if url_ind % 1000 == 0:
        print(url_ind / 1000)
    dat = hash_directory.read(policies_dir, url_row['doc_id'])
    if dat is None:
        continue
    # Fill in the blanks between two identical snapshots.
    last, last_ind = '', 0
    for ind, row in dat.iterrows():
        if pd.isna(row.digest):
            continue
        if row.digest == last:
            for i in range(last_ind, ind):
                dat.loc[i, 'digest'] = last
        else:
            last = row.digest
            last_ind = ind
    availability[url_ind, :] = ~pd.isna(dat.digest)

availability = pd.DataFrame(availability)
before_avai = 0
after_avai = 0
both_avai = 0
# May 2018 belongs to 2nd quarter 2018, index 25 in the list
for firmindex, avail in availability.iterrows():
    before = False
    # check for index 0 to 24
    for i in range(25):
        if avail[i] == 1.0:
            before_avai += 1
            before = True
            break
    # check for index 25 to 35
    for i in range(25, 35):
        if avail[i] == 1.0:
            after_avai += 1
            if before == True:
                both_avai +=1
            break

print(before_avai, after_avai, both_avai)


