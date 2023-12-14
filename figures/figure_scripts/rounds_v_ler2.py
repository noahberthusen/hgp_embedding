import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import seaborn as sns

plt.rc('font', family='serif')
# plt.rcParams['xtick.direction'] = 'in'
# plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.linewidth'] = 1
fig, ax = plt.subplots(1, 1, figsize=(4,4))

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

df = pd.read_csv(os.path.join(path, '../../prebuilt_code/ssf_masked/results/naive_scheduling/swap3_48_40_5_6/iterative_masked_decoding.res'))
df['p_error'] = 1 - df['p_log']
df['p_std_dev'] = np.sqrt(df['p_error'] * df['p_log'] / df['no_test'])
# df['p_std_dev'].replace(to_replace=0, value=1e-2, inplace=True)
guesses = []
params = []

def fun(x, a):
    return 1 - (1 - a)**x

xs = [50,100,200,300,400,500,410,510,610,710,810,910,600,700,800,900,1000,1500,2000]
p_masks = [0.0, 0.1, 0.2, 0.3, 0.4]
# colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
colors = [(64, 83, 211), (221, 179, 16), (181, 29, 20), (0, 190, 255), (251, 73, 176), (0, 178, 93)]
# colors = [(239, 230, 69), (233, 53, 161), (0, 227, 255), (225, 86, 44), (83, 126, 255), (0, 203, 133)][::-1]
# colors = [(86, 100, 26), (192, 175, 251), (230, 161, 118), (0, 103, 138), (152, 68, 100), (94, 204, 171)]
colors = [(c[0]/255, c[1]/255, c[2]/255) for c in colors]
# colors = sns.color_palette("hls", 6)
# colors = sns.color_palette("Set2", 6)
for i, j in enumerate(p_masks):
    if (j == 0.5):
        tmp_df = df[(df['p_mask'] == j) & (df['algo'] >= 200) & (df['p_std_dev'] > 0)]
    else:
        tmp_df = df[(df['p_mask'] == j) & (df['algo'] >= 300) & (df['p_std_dev'] > 0)]

    df = df[df['algo'].isin(xs)]
    tmp_df_fit = df[(df['p_mask'] == j) & (df['algo'] >= 300)]
    tmp_df_before = df[(df['p_mask'] == j) & (df['algo'] < 300)]

    ax.errorbar(tmp_df_fit['algo'], tmp_df_fit['p_error'], tmp_df_fit['p_std_dev'], label=f'{int(j*100)}% masked', fmt='o', c=colors[i])
    ax.errorbar(tmp_df_before['algo'], tmp_df_before['p_error'], tmp_df_before['p_std_dev'], fmt='x', alpha=0.8, c=colors[i])

    popt, pcov = curve_fit(fun, tmp_df['algo'], tmp_df['p_error'], maxfev=1000, p0=(0.001),
        sigma=tmp_df['p_std_dev'])

    xx = np.linspace(1, 2000, 1000)
    yy = fun(xx, *popt)
    ax.plot(xx[150:], yy[150:], c='k')
    ax.plot(xx[:150], yy[:150], c='k', linestyle='--', alpha=0.8)


ax.set_yscale('log')
ax.set_ylabel('Logical error rate, $p_\log$')
ax.set_xlabel('Rounds, $t$')

handles,labels = ax[0].get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
ax.legend(handles, labels, loc='lower right')

plt.tight_layout()
plt.show()

plt.savefig(os.path.join(path, '../rounds_v_ler.png'), dpi=1000, transparent=False, bbox_inches='tight')
