import pandas as pd
import numpy as np
import os

codes = [
    # "24_20_5_6",
    # "30_25_5_6",
    # "36_30_5_6",
    # "42_35_5_6",
    # "48_40_5_6",
    "60_50_5_6",
    # "84_70_5_6"
]

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
p_masks = [0.0, 0.1, 0.2, 0.3, 0.4]
ps = [0.001, 0.002, 0.003, 0.004, 0.005]
ts = [100]

tmp_arr = []
for code in codes:
    df = pd.read_csv(os.path.join(path, f'./{code}/iterative_tmp.res'), sep=',|\s+', engine='python')
    for i, p_mask in enumerate(p_masks):
        for j, p in enumerate(ps):
            for t in ts:
                tmp_df = df[(df['algo'] == t) & (df['p_mask'] == p_mask) & (df['p_phys'] == p)]
                if (not tmp_df.empty):
                    tmp = list(tmp_df.iloc[0])

                    tmp[8] = tmp_df['no_test'].sum()
                    tmp[9] = tmp_df['no_success'].sum()
                    tmp[10] = tmp_df['no_stop'].sum()
                    tmp[11] = tmp[9]/tmp[8]
                    tmp_arr.append(tmp)
    merged_df = pd.DataFrame(tmp_arr, columns=df.columns)
    
    print(len(merged_df))
    merged_df.head()

    merged_df.to_csv(os.path.join(path, f'./{code}/iterative_masked_decoding.res'), index=False)