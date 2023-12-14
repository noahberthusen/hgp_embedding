import pandas as pd
import numpy as np
import os

codes = [
    # "24_20_5_6",
    # "30_25_5_6",
    # "36_30_5_6",
    # "swap3_42_35_5_6",
    # "swap3_48_40_5_6",
    "30_25_5_6_synd"
    # "60_50_5_6",
    # "72_60_5_6",
    # "swap3_84_70_5_6"
]

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

for code in codes:
    df = pd.read_csv(os.path.join(path, f'./{code}/iterative_tmp.res'), sep=',|\s+', engine='python')
    merged_df = pd.DataFrame(columns=df.columns)
    t_max = 4001
    p_masks = [0.0, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
    for i, p in enumerate(p_masks):
        for t in range(t_max):
            ind = i*t_max + t
            tmp = df[(df['algo'] == t) & (df['p_mask'] == p)]
            if (not tmp.empty):
                merged_df.loc[ind] = tmp.iloc[0]

                merged_df.loc[ind]['no_test'] = tmp['no_test'].sum()
                merged_df.loc[ind]['no_success'] = tmp['no_success'].sum()
                merged_df.loc[ind]['no_stop'] = tmp['no_stop'].sum()
                merged_df.loc[ind]['p_log'] = merged_df.loc[ind]['no_success']/merged_df.loc[ind]['no_test']
    print(len(merged_df))
    merged_df.head()

    merged_df.to_csv(os.path.join(path, f'./{code}/iterative_masked_decoding.res'), index=False)