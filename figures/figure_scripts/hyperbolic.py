import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy.optimize import curve_fit

plt.rc('font', family='serif')
# plt.rcParams['xtick.direction'] = 'in'
# plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.linewidth'] = 1
fig, ax = plt.subplots(1, 1, figsize=(5,3))

full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)


def fun(x, a):
    return 1 - (1 - a)**x

xs = [5] + list(np.arange(10, 201, 10))
# colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
colors = [(64, 83, 211), (221, 179, 16), (181, 29, 20), (0, 190, 255), (251, 73, 176), (0, 178, 93)]
# colors = [(239, 230, 69), (233, 53, 161), (0, 227, 255), (225, 86, 44), (83, 126, 255), (0, 203, 133)][::-1]
# colors = [(86, 100, 26), (192, 175, 251), (230, 161, 118), (0, 103, 138), (152, 68, 100), (94, 204, 171)]
colors = [(c[0]/255, c[1]/255, c[2]/255) for c in colors]


def plot(filename, m, c, label):
    df = pd.read_csv(os.path.join(path, filename))
    df['p_error'] = 1 - df['p_log']
    df['p_std_dev'] = np.sqrt(df['p_error'] * df['p_log'] / df['no_test'])
    # df['p_std_dev'].replace(to_replace=0, value=1e-2, inplace=True)

    df = df[df['t'].isin(xs)]

    tmp_df = df[(df['p_mask'] == m) & (df['p_std_dev'] > 0)]

    ax.errorbar(tmp_df['t'], tmp_df['p_error'], tmp_df['p_std_dev'], label=label, fmt='o', c=colors[c])

    popt, pcov = curve_fit(fun, tmp_df['t'], tmp_df['p_error'], maxfev=1000, p0=(0.001),
        sigma=tmp_df['p_std_dev'])

    xx = np.linspace(1, 200, 1000)
    yy = fun(xx, *popt)
    ax.plot(xx, yy, c='k')


plot('../../src/results/hyperbolic/hyperbolic.res', 0, 0, '0% masked')
plot('../../src/results/hyperbolic/hyperbolic_wait_alternating.res', 0, 1, 'Alternating WAIT, 0% masked')
plot('../../src/results/hyperbolic/hyperbolic_mask_alternating.res', 0.1, 2, 'Alternating 10%, 0% masked')


handles,labels = ax.get_legend_handles_labels()
handles = handles[::-1]
labels = labels[::-1]
ax.legend().get_frame().set_linewidth(1)
ax.legend(handles, labels, loc='lower right', framealpha=1)


ax.set_yscale('log')
ax.set_ylabel('Logical error rate, $p_\log$')
ax.set_xlabel('Rounds, $t$')

plt.tight_layout()
plt.show()

# plt.savefig(os.path.join(path, '../hyperbolic.pdf'), format="pdf", dpi=1000, transparent=False, bbox_inches='tight')
