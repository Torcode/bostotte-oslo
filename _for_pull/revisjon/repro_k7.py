#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uavhengig reproduksjon av K7 (notebook 07): L0/G2 med regelverk kjent vs fryst.
Skrevet fra protokolldefinisjonene i notebookens kildekode (samme spesifikasjon,
uavhengig kjøring i dette miljøet). Fasit som skal treffes (notebook 07 / M20):
  L0 kjent 0.767 / 0.584 / 0.848    L0 fryst 1.112 / 0.652 / 1.344
  G2 kjent 0.815 / 0.584 / 0.939    G2 fryst 1.127 / 0.626 / 1.411
  M0       1.003 / 0.739 / 1.124
Skriver også gullsett-tabell for tre foreslåtte opprinnelser x h {1,3,6,12}.
"""
import os, time, json, math
import numpy as np, pandas as pd
import torch, torch.nn as nn
from xgboost import XGBRegressor

RAW = "/home/user/bostotte-oslo/data/raw/"
SEED = 20260807
np.random.seed(SEED); torch.manual_seed(SEED)
torch.set_num_threads(max(1, os.cpu_count()))

raa = pd.read_csv(RAW + "husbanken_bostotte_oslo_manedlig.csv")
raa["dato"] = pd.to_datetime(dict(year=raa.aar, month=raa.manedsnr, day=1))
raa = raa.sort_values("dato").reset_index(drop=True)
kant = raa.index[(raa.dato == raa.dato.max()) & (raa.ant_husstander_termin == 0)]
est = raa.drop(index=kant)
est = est[est.dato >= "2017-01-01"].reset_index(drop=True)
M = est.set_index("dato")["ant_husstander_termin"].astype(float)
LOG_M = np.log(M)
N_EST, MIN_TR, H = len(est), 72, 12
OPPRINNELSER = [est.dato.iloc[i-1] for i in range(1, N_EST+1) if MIN_TR <= i <= N_EST - H]
NEVNER = {t0: np.abs(M.loc[:t0].values[12:] - M.loc[:t0].values[:-12]).mean() for t0 in OPPRINNELSER}

mnd_alle = pd.date_range("2010-01-01", "2027-12-01", freq="MS")
X = pd.DataFrame(index=mnd_alle)
X["win_covid"] = ((mnd_alle >= "2020-04-01") & (mnd_alle <= "2020-10-01")).astype(int)
X["win_strom"] = ((mnd_alle >= "2021-12-01") & (mnd_alle <= "2024-03-01")).astype(int)
X["pakke_2024h2"] = (((mnd_alle >= "2024-07-01").astype(int)
                      + (mnd_alle >= "2024-09-01").astype(int)
                      + (mnd_alle >= "2024-10-01").astype(int)) / 3)

def u_av_fase(fase=0, fra=pd.Timestamp("2010-01-01"), til=pd.Timestamp("2027-12-31")):
    anker = pd.Timestamp("2014-01-06") + pd.Timedelta(days=fase)
    start = anker - pd.Timedelta(days=14*int(np.ceil((anker - fra).days/14)))
    d = pd.date_range(start, til, freq="14D"); d = d[d >= fra]
    return pd.Series(d).dt.to_period("M").dt.to_timestamp().value_counts().sort_index()

u = u_av_fase(0).reindex(mnd_alle)
X["k_pre"]  = (u - 26/12) * (mnd_alle <= "2024-12-01").astype(int)
X["k_post"] = (u - 26/12) * (mnd_alle >= "2025-01-01").astype(int)
REG, MIN_NZ, LAG = list(X.columns), 6, [1, 2, 3, 6, 11, 12]

def trekk(serie, s):
    v = serie.loc[:s]
    if len(v) < 13: return None
    d = np.diff(np.log(v.values))
    ut = {f"lag{l}": np.log(v.iloc[-1-l]) - np.log(v.iloc[-1]) for l in LAG}
    ut["niva"] = np.log(v.iloc[-1]); ut["d1"] = d[-1]
    ut["d12"] = np.log(v.iloc[-1]) - np.log(v.iloc[-13])
    ut["sd6"] = d[-6:].std(); ut["sd12"] = d[-12:].std(); ut["snitt6"] = d[-6:].mean()
    return ut

byd = pd.read_csv(RAW + "husbanken_bostotte_oslo_bydel_manedlig.csv", dtype={"kommunenr": str})
byd["dato"] = pd.to_datetime(dict(year=byd.aar, month=byd.manedsnr, day=1))
byd_nz = byd[byd.ant_husstander_termin > 0]
PANEL = {k: g.set_index("dato")["ant_husstander_termin"].astype(float).sort_index()
         for k, g in byd_nz.groupby("kommunenr") if k != "0301"}
PANEL = {k: v[v.index >= "2017-01-01"] for k, v in PANEL.items()}
SERIER = {"OSLO": M, **PANEL}
REKKE  = ["OSLO"] + sorted(PANEL)

KOL_T = list(pd.DataFrame([trekk(M, M.index[20])]).columns) + ["mnd"] + REG
HIST = {}
for k, v in SERIER.items():
    r = {s: trekk(v, s) for s in v.index}
    HIST[k] = pd.DataFrame({s: t for s, t in r.items() if t is not None}).T

def X_fryst(t0):
    Xf = X.copy()
    for r in ["win_covid", "win_strom", "pakke_2024h2"]:
        Xf.loc[Xf.index > t0, r] = Xf.loc[:t0, r].iloc[-1]
    return Xf

def sett_x(navn, t0, h, aktive, Xk):
    s, hh = SERIER[navn], HIST[navn]
    kilder = hh.index[hh.index + pd.DateOffset(months=h) <= t0]
    kilder = kilder[[k + pd.DateOffset(months=h) in s.index for k in kilder]]
    if len(kilder) == 0: return None, None
    maal = kilder + pd.DateOffset(months=h)
    D = hh.loc[kilder].copy(); D["mnd"] = maal.month
    for r in REG: D[r] = Xk.loc[maal, r].values if r in aktive else 0.0
    return D[KOL_T].to_numpy(float), np.log(s.loc[maal].values) - np.log(s.loc[kilder].values)

def prad_x(navn, t0, h, aktive, Xk):
    m_ = t0 + pd.DateOffset(months=h)
    if t0 not in HIST[navn].index or m_ not in SERIER[navn].index: return None
    d = HIST[navn].loc[[t0]].copy(); d["mnd"] = m_.month
    for r in REG: d[r] = Xk.loc[m_, r] if r in aktive else 0.0
    return d[KOL_T].to_numpy(float)

EPOKER, LR, WD = 400, 1e-2, 1e-4
def tren_lineaer(Xg, yg, Xpr):
    mx, sx = Xg.mean(0), Xg.std(0) + 1e-9
    my, sy = yg.mean(), yg.std() + 1e-9
    Xn = torch.tensor((Xg - mx)/sx, dtype=torch.float32)
    yn = torch.tensor((yg - my)/sy, dtype=torch.float32).view(-1, 1)
    Pn = torch.tensor((Xpr - mx)/sx, dtype=torch.float32)
    torch.manual_seed(SEED)
    m = nn.Linear(Xn.shape[1], 1)
    opt = torch.optim.Adam(m.parameters(), lr=LR, weight_decay=WD); f = nn.MSELoss()
    for _ in range(EPOKER):
        opt.zero_grad(); f(m(Xn), yn).backward(); opt.step()
    m.eval()
    with torch.no_grad():
        return m(Pn).numpy().ravel()*sy + my

PARAM = dict(n_estimators=300, max_depth=3, learning_rate=0.05, subsample=0.8,
             colsample_bytree=0.8, min_child_weight=5, reg_lambda=1.0,
             random_state=SEED, n_jobs=4, verbosity=0)

t_start, rf = time.time(), []
for t0 in OPPRINNELSER:
    aktive = [r for r in REG if (X.loc[M.loc[:t0].index, r] != 0).sum() >= MIN_NZ]
    Xf = X_fryst(t0)
    for h in range(1, H + 1):
        uu = dict(opprinnelse=t0, h=h, sant=float(M.loc[t0 + pd.DateOffset(months=h)]),
                  q=NEVNER[t0], M0=float(LOG_M.loc[t0]))
        for merke, Xk in [("kjent", X), ("fryst", Xf)]:
            Xs, ys, navn_pr, Xpr = [], [], [], []
            for navn in REKKE:
                a, b = sett_x(navn, t0, h, aktive, Xk)
                if a is not None: Xs.append(a); ys.append(b)
                p = prad_x(navn, t0, h, aktive, Xk)
                if p is not None: navn_pr.append(navn); Xpr.append(p)
            Xg, yg, Xp = np.vstack(Xs), np.concatenate(ys), np.vstack(Xpr)
            i, ank = navn_pr.index("OSLO"), float(LOG_M.loc[t0])
            uu[f"L0_{merke}"] = ank + float(tren_lineaer(Xg, yg, Xp)[i])
            uu[f"G2_{merke}"] = ank + float(XGBRegressor(**PARAM).fit(Xg, yg).predict(Xp)[i])
        rf.append(uu)
RF = pd.DataFrame(rf)
print(f"{len(RF)} punkter x 2 informasjonssett paa {time.time()-t_start:.0f} s", flush=True)

def m_(kol, hs=None):
    x = RF if hs is None else RF[RF.h.isin(hs)]
    return float((np.abs(x.sant - np.exp(x[kol]))/x.q).mean())

FASIT = {"L0_kjent": (0.767, 0.584, 0.848), "L0_fryst": (1.112, 0.652, 1.344),
         "G2_kjent": (0.815, 0.584, 0.939), "G2_fryst": (1.127, 0.626, 1.411),
         "M0":       (1.003, 0.739, 1.124)}
print(f"\n{'':12s} {'alle h':>8s} {'h 1-3':>8s} {'h 6-12':>8s}   fasit (notebook 07)")
for kol, fas in FASIT.items():
    v = (m_(kol), m_(kol, [1,2,3]), m_(kol, list(range(6,13))))
    ok = all(abs(a-b) < 0.006 for a, b in zip(v, fas))
    print(f"{kol:12s} {v[0]:8.3f} {v[1]:8.3f} {v[2]:8.3f}   {fas}  {'==' if ok else 'AVVIK'}")

# Gullsett: tre opprinnelser x h i {1,3,6,12}
GULL_T0 = [pd.Timestamp("2023-03-01"), pd.Timestamp("2023-10-01"), pd.Timestamp("2025-06-01")]
g = RF[RF.opprinnelse.isin(GULL_T0) & RF.h.isin([1,3,6,12])].copy()
g["naiv"] = np.exp(g.M0).round(0)
for kol in ["L0_kjent","L0_fryst","G2_kjent","G2_fryst"]:
    g[kol+"_pred"] = np.exp(g[kol]).round(0)
ut = g[["opprinnelse","h","sant","q","naiv","L0_kjent_pred","L0_fryst_pred","G2_kjent_pred","G2_fryst_pred"]]
ut.to_csv("/home/user/audit/gullsett_referanse.csv", index=False)
print("\nGullsett skrevet til /home/user/audit/gullsett_referanse.csv")
print(ut.to_string(index=False))
