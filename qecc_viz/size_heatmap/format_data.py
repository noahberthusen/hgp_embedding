import pandas as pd
import numpy as np
import os

code = "48_40_5_6"
# code = "60_50_5_6"

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
filename = os.path.join(path, f"./data/{code}_error_size.res")
df = pd.read_csv(filename, sep=';', header=None)

m = 0
for i in range(len(df)):
    for j in range(len(df.iloc[0])):
        x = df.iloc[i][j].replace('*', '').replace('+','')
        tmp = max(int(x.split(',')[0][1:]), int(x.split(',')[1][:-1]))
        m = tmp if (tmp > m) else m
print(m)

regex = [
    ("invis_to_invis",  "\([0-9]+,[0-9]+\+*\)"),
    ("invis_to_vis", "\([0-9]+,[0-9]+\*\+*\)"),
    ("vis_to_invis", "\([0-9]+\*,[0-9]+\+*\)"),
    ("vis_to_vis", "\([0-9]+\*,[0-9]+\*\+*\)")
]

def gen_all_heatmaps(successes, fails, m):
    def gen_heatmap(series, m):
        heatmap = np.zeros((m+1, m+1), dtype=int).tolist()
        tot = series.sum()
        for i, v in series.items():
            x = i.replace('*','').replace('+','')
            in_ind = int(x.split(',')[0][1:])
            out_ind = int(x.split(',')[1][:-1])
            heatmap[in_ind][out_ind] = v
        return (heatmap, tot)

    obj = {}
    for label, reg in regex:
        ser1 = successes.value_counts()
        ser1 = ser1[ser1.index.str.contains(reg)]
        tmp1 = gen_heatmap(ser1, m)

        ser2 = fails.value_counts()
        ser2 = ser2[ser2.index.str.contains(reg)]
        tmp2 = gen_heatmap(ser2, m)

        obj[label] = {
            "successes": {
                "heatmap": tmp1[0],
                "tot": int(tmp1[1])
            },
            "failures": {
                "heatmap": tmp2[0],
                "tot": int(tmp2[1])
            }
        }
    return obj


successes = df[~df[len(df.iloc[0]) - 1].str.contains("\+")]
fails = df[df[len(df.iloc[0]) - 1].str.contains("\+")]

data = []
for i in range(len(df.iloc[0])):
    data.append(gen_all_heatmaps(successes[i], fails[i], m))

with open(os.path.join(path, f"{filename}.js"), 'w') as f:
    f.write("heatmap_data = " + str({ "data": data, "tot": len(df), "dim": m }))