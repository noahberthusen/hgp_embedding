import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import itertools
import numpy as np
import pandas as pd
import matplotlib
import math
import random
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import os

codes = [
    "24_20_5_6",
    "30_25_5_6",
    "36_30_5_6",
    # "swap3_42_35_5_6",
    "42_35_5_6",
    "48_40_5_6",
    "60_50_5_6",
    "72_60_5_6",
    "84_70_5_6"
]

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

def plot(ax, p_masks, plot_ind):
    if (plot_ind == 0):
        sched = "naive_scheduling"
        marker = 'o'
        label = "Simple scheduling"
    else:
        sched = "progressive_scheduling"
        marker = 'x'
        label = "Iterative scheduling"

    params = [[] for code in codes]
    errors = [[] for code in codes]

    for i, code in enumerate(codes):
        df = pd.read_csv(os.path.join(path, f'../../prebuilt_code/ssf_masked/results/{sched}/{code}/iterative_masked_decoding.res'))
        df['p_error'] = 1 - df['p_log']
        df['p_std_dev'] = np.sqrt(df['p_error'] * df['p_log'] / df['no_test'])
        df['p_std_dev'].replace(to_replace=0, value=1e-2, inplace=True)


        def fun(x, a):
            return (1 - (1 - a)**x)

        for j, k in enumerate(p_masks):
            if (k == 0.5):
                tmp_df = df[(df['p_mask'] == k) & (df['algo'] >= 200) & (df['p_std_dev'] > 0)]
            else:
                tmp_df = df[(df['p_mask'] == k) & (df['algo'] >= 300) & (df['p_std_dev'] > 0)]
            if (len(tmp_df)):
                popt, pcov = curve_fit(fun, tmp_df['algo'], tmp_df['p_error'], p0=(1e-5), maxfev=1000,
                    sigma=tmp_df['p_std_dev'])
                params[i].append(popt[0])
                errors[i].append(np.sqrt(np.diag(pcov))[0])
            else:
                params[i].append(0)
                errors[i].append(0)
    params = np.array(params)
    errors = np.array(errors)

    distances = np.array([6, 8, 12, 14, 16, 18, 20, 23])

    def exp_fun(x, c, V):
        return c / (np.abs(V)**((x+1)/2))
    def fun(x, c, V):
        return np.log(c) - V*((x+1)/2)

    for i, j in enumerate(p_masks):
        inds = np.where(params[:,i])
        if (len(inds[0])):
            ax.errorbar(distances[inds], params[:,i][inds], errors[:,i][inds], fmt="o", c='k', label=label, marker=marker)
            popt, pcov = curve_fit(fun, distances[inds], np.log(params[:,i][inds]), p0=(0.001, 0.2), maxfev=1000,
                sigma=np.log(errors[:,i][inds]))
            std_dev = np.sqrt(np.diag(pcov))
            print(j, np.exp(popt), np.sqrt(np.diag(pcov)))

            xx = np.linspace(distances[0], distances[-1], 1000)

            yy  = exp_fun(xx, popt[0], np.exp(popt[1]))
            yy1 = exp_fun(xx, popt[0] + std_dev[0], np.exp(popt[1] - std_dev[1]))
            yy2 = exp_fun(xx, popt[0] - std_dev[0], np.exp(popt[1] + std_dev[1]))
            ax.plot(xx, yy, 'k')
            ax.plot(xx, yy1, 'k--', alpha=0.2)
            ax.plot(xx, yy2, 'k--', alpha=0.2)
            ax.fill_between(xx, yy1, yy2, facecolor="gray", alpha=0.05)

            ax.set_yscale('log')

            
            # if (j == 0.3 or j == 0.4):
                # ax.set_yticks([0.001])
                # ax.set_yticklabels(["$10^{-3}$"])
            if (j == 0.5):
                ax.set_yticks([0.02, 0.01, 0.006])
                ax.set_yticklabels(["","$10^{-2}$",""])
            if (j == 0.3):
                handles,labels = ax.get_legend_handles_labels()
            # # handles = handles[::-1]
            # labels = labels[::-1]
            # ax[i].set_title(f'{int(j*100)}% masked')
                ax.legend(handles, labels, loc='lower left', fontsize=8)
            # ax[0].set_ylabel('Logical error per round, $\epsilon_L$')
            # ax[i].set_xlabel('Distance, $d$')

def plot_both(ax, plot_ind):
    p_masks = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]

    if (plot_ind == 0):
        sched = "naive_scheduling"
        tmp_colors = colors
    else:
        sched = "progressive_scheduling"
        tmp_colors = colors

    params = [[] for code in codes]
    errors = [[] for code in codes]

    for i, code in enumerate(codes):
        df = pd.read_csv(os.path.join(path, f'../../prebuilt_code/ssf_masked/results/{sched}/{code}/iterative_masked_decoding.res'))
        df['p_error'] = 1 - df['p_log']
        df['p_std_dev'] = np.sqrt(df['p_error'] * df['p_log'] / df['no_test'])
        df['p_std_dev'].replace(to_replace=0, value=1e-2, inplace=True)


        def fun(x, a):
            return (1 - (1 - a)**x)

        for j, k in enumerate(p_masks):
            if (k == 0.5):
                tmp_df = df[(df['p_mask'] == k) & (df['algo'] >= 200) & (df['p_std_dev'] > 0)]
            else:
                tmp_df = df[(df['p_mask'] == k) & (df['algo'] >= 300) & (df['p_std_dev'] > 0)]
            if (len(tmp_df)):
                popt, pcov = curve_fit(fun, tmp_df['algo'], tmp_df['p_error'], p0=(1e-5), maxfev=1000,
                    sigma=tmp_df['p_std_dev'])
                params[i].append(popt[0])
                errors[i].append(np.sqrt(np.diag(pcov))[0])
            else:
                params[i].append(0)
                errors[i].append(0)
    params = np.array(params)
    errors = np.array(errors)

    distances = np.array([6, 8, 12, 14, 16, 18, 20, 23])

    def exp_fun(x, c, V):
        return c / (np.abs(V)**((x+1)/2))
    def fun(x, c, V):
        return np.log(c) - V*((x+1)/2)

    for i, j in enumerate(p_masks):
        inds = np.where(params[:,i])

        if (len(inds[0])):
            ax[plot_ind].errorbar(distances[inds], params[:,i][inds], errors[:,i][inds], fmt="o", c=tmp_colors[i], label=f'{int(j*100)}% masked')
            popt, pcov = curve_fit(fun, distances[inds], np.log(params[:,i][inds]), p0=(0.001, 0.2), maxfev=1000,
                sigma=np.log(errors[:,i][inds]))
            std_dev = np.sqrt(np.diag(pcov))
            print(j, np.exp(popt), np.sqrt(np.diag(pcov)))

            xx = np.linspace(distances[0], distances[-1], 1000)

            yy  = exp_fun(xx, popt[0], np.exp(popt[1]))
            yy1 = exp_fun(xx, popt[0] + std_dev[0], np.exp(popt[1] - std_dev[1]))
            yy2 = exp_fun(xx, popt[0] - std_dev[0], np.exp(popt[1] + std_dev[1]))
            ax[plot_ind].plot(xx, yy, 'k')
            ax[plot_ind].plot(xx, yy1, 'k--', alpha=0.2)
            ax[plot_ind].plot(xx, yy2, 'k--', alpha=0.2)
            ax[plot_ind].fill_between(xx, yy1, yy2, facecolor="gray", alpha=0.05)

            ax[plot_ind].set_yscale('log')

            handles,labels = ax[0].get_legend_handles_labels()
            handles = handles[::-1]
            labels = labels[::-1]
            ax[0].legend(handles, labels, loc='lower left', fontsize=8)
            ax[0].set_ylabel('Logical error per round, $\epsilon_L$')
            # ax[plot_ind].set_xlabel('Distance, $d$')


fig =  plt.figure(figsize=(14,5))
# plot_both(ax, 0)
# plot_both(ax, 1)
ax1 = fig.add_subplot(1,4,1)
ax2 = fig.add_subplot(1,4,2)

ax3 = fig.add_subplot(2,4,3)
ax4 = fig.add_subplot(2,4,4)
ax5 = fig.add_subplot(2,4,7)
ax6 = fig.add_subplot(2,4,8)

plot_both([ax1, ax2], 0)
plot_both([ax1, ax2], 1)

plot(ax3, [0.1], 0)
plot(ax3, [0.1], 1)

plot(ax4, [0.2], 0)
plot(ax4, [0.2], 1)

plot(ax5, [0.3], 0)
plot(ax5, [0.3], 1)

plot(ax6, [0.5], 0)
plot(ax6, [0.5], 1)

ax1.text(-.17,1,'(a)', transform=ax1.transAxes, fontsize=16)
ax2.text(-.17,1,'(b)', transform=ax2.transAxes, fontsize=16)
ax3.text(-.17,1,'(c)', transform=ax3.transAxes, fontsize=16)
ax4.text(-.17,1,'(d)', transform=ax4.transAxes, fontsize=16)
ax5.text(-.17,1,'(e)', transform=ax5.transAxes, fontsize=16)
ax6.text(-.17,1,'(f)', transform=ax6.transAxes, fontsize=16)


# fig.supylabel('Logical error per round, $\epsilon_L$')
fig.supxlabel('Distance, $d$', fontsize=10)

# plt.show()
plt.savefig(os.path.join(path, '../lambda3.png'), dpi=1000, transparent=False, bbox_inches='tight')

