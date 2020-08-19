import pandas as pd
import numpy as np
import statsmodels.tsa.stattools as ts
from scipy.stats import norm, kstest
from statsmodels.tsa.stattools import adfuller
from constants import *
#import plotly.plotly as py

def figure_coint_calc(df1, df2):
    if df1 is None or df2 is None:
        return None, None

    if df1.empty or df2.empty:
        return None, None

    cov = np.cov(df1['log'], df2['log'], ddof=0)
    var = np.var(df2['log'], ddof=1)

    if np.isnan(var):
        return np.nan
    #cointegration of df2
    if var == 0:
        coint_calc = 0
    else:
        coint_calc = cov[0,1] / var

    return coint_calc

def figure_coint_fit(df1, df2):
    if df1.empty or df2.empty:
        return None, None

    adf_list = list()
    dfs = pd.DataFrame()
    for i in range(-20, 21):
        coint = float(i / 10)

        dfs['value'] = df1['log'] - coint * df2['log']
        mean = dfs['value'].mean()
        dfs['value'] = (dfs['value'] - mean) * 100
        adf = adfuller(dfs['value'])

        adf_list.append((adf[1], coint))

    min_adf, coint_fit = min(adf_list)

    return coint_fit 

def figure_test(df1, df2, dfs):
    X = dfs['value']
    loc, scale = norm.fit(X)
    n = norm(loc=loc, scale=scale)

    if X.__len__() < 10:
        return n, None, None,None 

    # kstest
    result = kstest(X, n.cdf)
    ks_pvalue = result.pvalue

    # adf
    result = adfuller(X)
    adf_pvalue = result[1]

    #cointegration test
    coint_pvalue = ts.coint(df1['log'], df2['log'])[1]

    return n, ks_pvalue, adf_pvalue, coint_pvalue

def get_bins(df):
    return np.arange(df.min(), df.max()+0.5,0.5)

def figure_density(dfs):
    if dfs is None:
        return None

    bins = get_bins(dfs['value']).__len__()+1
    hist, bin_edges = np.histogram(dfs['value'], bins=bins, density=True)

    X = float("%.5f" % dfs['value'][-1])
    idx = get_idx_from_bins(X, bin_edges)

    diff = np.diff(bin_edges)[0]

    density = hist[idx] * diff * 100

    return density

def figure_place(dfs):
    place = 1

    sorted_dfs = list(dfs)
    sorted_dfs.sort()

    for i, h in enumerate(sorted_dfs):
        if h == dfs[-1]:
            place = i + 1
            break

    return place

def get_cy_cnt(cy, value):
    direction = cy[0]
    cy_cnt    = cy[1]

    if direction == D_NONE and value >= cy[2]:  #top
        direction = D_RISE
    if direction == D_NONE and value <= cy[3]:  #bottom
        direction = D_DROP
    if direction == D_DROP and value >= cy[2]:  #top
        direction = D_RISE
        cy_cnt = cy_cnt + 1
    if direction == D_RISE and value <= cy[3]:  #bottom
        direction = D_DROP
        cy_cnt = cy_cnt + 1
    return direction, cy_cnt

# Amplitude
def figure_pam(dfs):
    dir0 = D_NONE
    hit0_cnt = 0

    ss = dfs.sort_values(by='value')['value']
    
    #D_NONE IS -1
    ends  = [[-1,0,ss[-i:   ].mean(),ss[ 0:i].mean()] for i in range(10,100,10)]
    rng10 = [[-1,0,ss[-i:-10].mean(),ss[10:i].mean()] for i in range(20,100,10)]
    rng20 = [[-1,0,ss[-i:-20].mean(),ss[20:i].mean()] for i in range(30,100,10)]
    rng30 = [[-1,0,ss[-i:-30].mean(),ss[30:i].mean()] for i in range(40,100,10)]
    rng40 = [[-1,0,ss[-i:-40].mean(),ss[40:i].mean()] for i in range(50,100,10)]
    rng50 = [[-1,0,ss[-i:-50].mean(),ss[50:i].mean()] for i in range(60,100,10)]
    rng60 = [[-1,0,ss[-i:-60].mean(),ss[60:i].mean()] for i in range(70,100,10)]
    rng70 = [[-1,0,ss[-i:-70].mean(),ss[70:i].mean()] for i in range(80,100,10)]
    rng80 = [[-1,0,ss[-i:-80].mean(),ss[80:i].mean()] for i in range(90,100,10)]

    for i, row in dfs.iterrows():
        value = row.value
        # touch 0
        if dir0 == D_NONE and value > 0:
            dir0 = D_RISE
        if dir0 == D_NONE and value < 0:
            dir0 = D_DROP
        if dir0 == D_DROP and value >=0:
            dir0 = D_RISE
            hit0_cnt = hit0_cnt + 1
        if dir0 == D_RISE and value < 0:
            dir0 = D_DROP
            hit0_cnt = hit0_cnt + 1

        for idx, a in enumerate(ends):
            ends[idx][0],  ends[idx][1]  = get_cy_cnt(ends[idx],  value)
        for idx, a in enumerate(rng10):
            rng10[idx][0], rng10[idx][1] = get_cy_cnt(rng10[idx], value)
        for idx, a in enumerate(rng20):
            rng20[idx][0], rng20[idx][1] = get_cy_cnt(rng20[idx], value)
        for idx, a in enumerate(rng30):
            rng30[idx][0], rng30[idx][1] = get_cy_cnt(rng30[idx], value)
        for idx, a in enumerate(rng40):
            rng40[idx][0], rng40[idx][1] = get_cy_cnt(rng40[idx], value)
        for idx, a in enumerate(rng50):
            rng50[idx][0], rng50[idx][1] = get_cy_cnt(rng50[idx], value)
        for idx, a in enumerate(rng60):
            rng60[idx][0], rng60[idx][1] = get_cy_cnt(rng60[idx], value)
        for idx, a in enumerate(rng70):
            rng70[idx][0], rng70[idx][1] = get_cy_cnt(rng70[idx], value)
        for idx, a in enumerate(rng80):
            rng80[idx][0], rng80[idx][1] = get_cy_cnt(rng80[idx], value)

    return hit0_cnt, ends, rng10, rng20, rng30, rng40, rng50, rng60, rng70,rng80

# Amplitude
def figure_pam_old(dfs):
    dir0 = dir5 = dir10 = dir15 = dir20 = D_NONE
    cy0_cnt = cy5_cnt = cy10_cnt = cy15_cnt = cy20_cnt = 0

    dfs_sorted = dfs.sort_values(by='value')
    top_5  = dfs_sorted[-5:].mean()['value']
    top_10 = dfs_sorted[-10:].mean()['value']
    top_15 = dfs_sorted[-15:].mean()['value']
    top_20 = dfs_sorted[-20:].mean()['value']

    bottom_5  = dfs_sorted[0:5].mean()['value']
    bottom_10 = dfs_sorted[0:10].mean()['value']
    bottom_15 = dfs_sorted[0:15].mean()['value']
    bottom_20 = dfs_sorted[0:20].mean()['value']

    for value in dfs['value']:
        # touch 0
        if dir0 == D_NONE and value > 0:
            dir0 = D_RISE
        if dir0 == D_NONE and value < 0:
            dir0 = D_DROP
        if dir0 == D_DROP and value >=0:
            dir0 = D_RISE
            cy0_cnt = cy0_cnt + 1
        if dir0 == D_RISE and value < 0:
            dir0 = D_DROP
            cy0_cnt = cy0_cnt + 1

        dir5,  cy5_cnt  = get_cy_cnt(dir5,  cy5_cnt,  value, top_5,  bottom_5)
        dir10, cy10_cnt = get_cy_cnt(dir10, cy10_cnt, value, top_10, bottom_10)
        dir15, cy15_cnt = get_cy_cnt(dir15, cy15_cnt, value, top_15, bottom_15)
        dir20, cy20_cnt = get_cy_cnt(dir20, cy20_cnt, value, top_20, bottom_20)

    return cy0_cnt, cy5_cnt, cy10_cnt, cy15_cnt, cy20_cnt

def get_idx_from_bins(X, bin_edges):
    idx = -1
    for i, b in enumerate(bin_edges):
        if i == 0:
            if bin_edges[i] >= X:
                idx = i
                break
        if i == bin_edges.__len__() - 2:
                idx = i
                break

        if bin_edges[i] <= X <= bin_edges[i+1]:
            idx = i
            break
    return idx 

if __name__ == '__main__':
    pass
