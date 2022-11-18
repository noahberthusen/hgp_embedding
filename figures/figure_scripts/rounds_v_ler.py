import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

fig, ax = plt.subplots(2, 1, figsize=(5,6.5), sharey=True, sharex=True, gridspec_kw={'height_ratios': [1, 1.25]})

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

df = pd.read_csv(os.path.join(path, '../../prebuilt_code/ssf_masked/results/naive_scheduling/48_40_5_6/iterative_masked_decoding.res'))
df['p_error'] = 1 - df['p_log']
df['p_std_dev'] = np.sqrt(df['p_error'] * df['p_log'] / df['no_test'])
# df['p_std_dev'].replace(to_replace=0, value=1e-2, inplace=True)
guesses = []
params = []

def fun(x, a):
    return 1 - (1 - a)**x

xs = [50,100,200,300,400,500,410,510,610,710,810,910,600,700,800,900,1000,1500,2000]
p_masks = [0.0, 0.1, 0.2, 0.3, 0.4]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
for i, j in enumerate(p_masks):
    if (j == 0.5):
        tmp_df = df[(df['p_mask'] == j) & (df['algo'] >= 200) & (df['p_std_dev'] > 0)]
    else:
        tmp_df = df[(df['p_mask'] == j) & (df['algo'] >= 300) & (df['p_std_dev'] > 0)]
    
    df = df[df['algo'].isin(xs)]
    tmp_df_fit = df[(df['p_mask'] == j) & (df['algo'] >= 300)]
    tmp_df_before = df[(df['p_mask'] == j) & (df['algo'] < 300)]

    ax[0].errorbar(tmp_df_fit['algo'], tmp_df_fit['p_error'], tmp_df_fit['p_std_dev'], label=f'{int(j*100)}% masked', fmt='o', c=colors[i])
    ax[0].errorbar(tmp_df_before['algo'], tmp_df_before['p_error'], tmp_df_before['p_std_dev'], fmt='x', alpha=0.8, c=colors[i])

    popt, pcov = curve_fit(fun, tmp_df['algo'], tmp_df['p_error'], maxfev=1000, p0=(0.001),
        sigma=tmp_df['p_std_dev'])

    xx = np.linspace(1, 2000, 1000)
    yy = fun(xx, *popt)
    ax[0].plot(xx[150:], yy[150:], c='k')
    ax[0].plot(xx[:150], yy[:150], c='k', linestyle='--', alpha=0.8)


ax[0].set_yscale('log')
ax[0].set_ylabel('Logical error rate, $p_\log$')
ax[1].set_xlabel('Rounds, $t$')

handles,labels = ax[0].get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
ax[0].legend(handles, labels, loc='lower right')

codes = [
    # "24_20_5_6",
    "30_25_5_6",
    "36_30_5_6",
    "42_35_5_6",
    "48_40_5_6",
    "60_50_5_6",
    "72_60_5_6",
    "84_70_5_6"
][::-1]

code_sizes = np.array([int(code[0:2])**2 + int(code[3:5])**2 for code in codes])
log_qbs = np.array([(int(code[0:2]) - int(code[3:5]))**2 for code in codes])
distances = np.array([8, 12, 14, 16, 18, 20, 23])[::-1]


def fun(x, a):
    return 1 - (1 - a)**x
params = []

sched = "naive_scheduling"

for i, code in enumerate(codes):
    df = pd.read_csv(os.path.join(path, f'../../prebuilt_code/ssf_masked/results/{sched}/{code}/iterative_masked_decoding.res'))
    df['p_error'] = 1 - df['p_log']
    df['p_std_dev'] = np.sqrt(df['p_error'] * df['p_log'] / df['no_test'])

    p_masks = [0.1]
    for j, k in enumerate(p_masks):
        if (k == 0.5):
            tmp_df = df[(df['p_mask'] == k) & (df['algo'] >= 200) & (df['p_std_dev'] > 0)]
        else:
            tmp_df = df[(df['p_mask'] == k) & (df['algo'] >= 300) & (df['p_std_dev'] > 0)]

        df = df[df['algo'].isin(xs)]
        # tmp_df_all = df[(df['p_mask'] == k) & (df['algo'] % 100 == 0) & (df['algo'] <= 2000) & (df['algo'] > 10)]

        # ax[1].errorbar(tmp_df_all['algo'], tmp_df_all['p_error'], tmp_df_all['p_std_dev'], label=f'{code}', fmt='o', c=colors[i])
        tmp_df_fit = df[(df['p_mask'] == k) & (df['algo'] >= 300)]
        tmp_df_before = df[(df['p_mask'] == k) & (df['algo'] < 300)]

        ax[1].errorbar(tmp_df_fit['algo'], tmp_df_fit['p_error'], tmp_df_fit['p_std_dev'], 
            fmt='o', c=colors[i], label=f"[[{code_sizes[i]},{log_qbs[i]},{distances[i]}]]")
        ax[1].errorbar(tmp_df_before['algo'], tmp_df_before['p_error'], tmp_df_before['p_std_dev'], fmt='x', alpha=0.8, c=colors[i])

        popt, pcov = curve_fit(fun, tmp_df['algo'], tmp_df['p_error'], p0=(0.001), maxfev=1000,
            sigma=tmp_df['p_std_dev'])

        xx = np.linspace(1, 2000, 1000)
        yy = fun(xx, *popt)
        ax[1].plot(xx[150:], yy[150:], c='k')
        ax[1].plot(xx[:150], yy[:150], c='k', linestyle='--', alpha=0.8)

# plt.text(-0.02, 0.94, "(a)", fontsize=16, transform=plt.gcf().transFigure, fontfamily='sans-serif')
# plt.text(-0.02, 0.46, "(b)", fontsize=16, transform=plt.gcf().transFigure, fontfamily='sans-serif')

ax[1].set_ylabel('Logical error rate, $p_\log$')
ax[1].legend(loc='lower right')

handles,labels = ax[1].get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
ax[1].legend(handles, labels, loc='lower right')

ax[0].text(-.2,.95,'(a)', transform=ax[0].transAxes, fontsize=16)
ax[1].text(-.2,.95,'(b)', transform=ax[1].transAxes, fontsize=16)


# plt.tight_layout()
# plt.show()

plt.savefig(os.path.join(path, '../rounds_v_ler.png'), dpi=1000, transparent=False, bbox_inches='tight')
