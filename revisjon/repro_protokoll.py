#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Uavhengig revisorreproduksjon (skrevet fra protokolldefinisjonene, ikke kopiert):
  R1  M0/M1-tallene i tabell 17 (AV1) og notebook 02 (AV2)
  R2  Konformal kalibrering: AV1-skjema (t_j < t_i) mot tidsgyldig (t_j + h <= t_i)
  R3  Endelig-utvalgskorreksjonen (K3) og np.quantile linear/higher-sporsmalet
  R4  Identiteter: M0==M1 ved h=12; fasit april 2024; V1
Utvalg: est 2017m1-2026m06 (114 rader), 31 opprinnelser 2022m12-2025m06, h=1..12.
"""
import numpy as np, pandas as pd, json, math

RAW = "/home/user/bostotte-oslo/data/raw/husbanken_bostotte_oslo_manedlig.csv"

raa = pd.read_csv(RAW)
raa["dato"] = pd.to_datetime(dict(year=raa.aar, month=raa.manedsnr, day=1))
raa = raa.sort_values("dato").reset_index(drop=True)

# V1: fjern siste rad hvis (og bare hvis) termin-antallet er 0 (strukturell null)
siste = raa.dato.max()
v1_mask = (raa.dato == siste) & (raa.ant_husstander_termin == 0)
print(f"[R4] V1: siste rad {siste:%Y-%m}, termin={raa.ant_husstander_termin.iloc[-1]:.0f}, fjernes: {bool(v1_mask.any())}")
termin = raa[~v1_mask].reset_index(drop=True)

est = termin[termin.dato >= "2017-01-01"].reset_index(drop=True)
M = est.set_index("dato")["ant_husstander_termin"].astype(float)
L = np.log(M)
n_est = len(est)
print(f"[R4] n_est = {n_est} (krav 114), {est.dato.min():%Y-%m}..{est.dato.max():%Y-%m}")
assert n_est == 114

# fasit-sjekk april 2024 og fallet mars->april
m24_03, m24_04 = M.loc["2024-03-01"], M.loc["2024-04-01"]
print(f"[R4] mars 2024 = {m24_03:.0f}, april 2024 = {m24_04:.0f}, endring {100*(m24_04/m24_03-1):.1f} % (README: fasit 15 588, fall 25 %)")

MIN_TR, H = 72, 12
ORIG = [est.dato.iloc[i-1] for i in range(1, n_est+1) if MIN_TR <= i <= n_est - H]
assert len(ORIG) == 31 and ORIG[0] == pd.Timestamp("2022-12-01") and ORIG[-1] == pd.Timestamp("2025-06-01")

Z80, Z95 = 1.2815515655446004, 1.959963984540054

def nevner(t0):
    x = M.loc[:t0].values
    return np.abs(x[12:] - x[:-12]).mean()

rows = []
for t0 in ORIG:
    tr = L.loc[:t0]
    sd0 = math.sqrt(float((np.diff(tr.values)**2).mean()))          # naiv: uten df-korr
    sd1 = math.sqrt(float(((tr.values[12:]-tr.values[:-12])**2).mean()))
    for h in range(1, H+1):
        maal = t0 + pd.DateOffset(months=h)
        kilde = maal - pd.DateOffset(months=12*math.ceil(h/12))
        rows.append(dict(modell="M0", t0=t0, h=h, dato=maal, sant=M.loc[maal],
                         mu=float(tr.iloc[-1]), sd=sd0*math.sqrt(h)))
        rows.append(dict(modell="M1", t0=t0, h=h, dato=maal, sant=M.loc[maal],
                         mu=float(L.loc[kilde]), sd=sd1*math.sqrt(1+(h-1)//12)))
R = pd.DataFrame(rows)
R["pred"] = np.exp(R.mu); R["e"] = R.sant - R.pred
R["mase"] = R.e.abs() / R.t0.map({t: nevner(t) for t in ORIG})
R["lf"] = np.log(R.sant) - R.mu
for nv, z in [(80, Z80), (95, Z95)]:
    R[f"l{nv}"] = np.exp(R.mu - z*R.sd); R[f"u{nv}"] = np.exp(R.mu + z*R.sd)
    R[f"d{nv}"] = (R.sant >= R[f"l{nv}"]) & (R.sant <= R[f"u{nv}"])
R["ws"] = (R.u80-R.l80) + 10*(R.l80-R.sant)*(R.sant<R.l80) + 10*(R.sant-R.u80)*(R.sant>R.u80)

g = R.groupby("modell")
tab = pd.DataFrame({"MASE": g.mase.mean().round(3),
                    "RMSE": np.sqrt(g.apply(lambda x: (x.e**2).mean(), include_groups=False)).round(0),
                    "d80": (100*g.d80.mean()).round(0), "d95": (100*g.d95.mean()).round(0),
                    "WS": g.ws.mean().round(0)})
print("\n[R1] Reproduksjon av tabell 17 (M0/M1):")
print(tab.to_string())
FASIT = {"M0": (1.003, 1698, 91, 98, 7082), "M1": (1.228, 1844, 77, 97, 6125)}
ok = all(tuple(tab.loc[m]) == FASIT[m] for m in FASIT)
print("   AVSTEMT MOT PUBLISERT:", "JA - alle 10 tall like" if ok else "NEI - AVVIK")

# h=12-identiteten
h12 = R[R.h == 12].pivot(index="t0", columns="modell", values="mu")
print(f"[R4] M0==M1 ved h=12: {bool(np.allclose(h12.M0, h12.M1))}")

# ---- R2/R3: konformal, fire varianter (skjema x kvantil) --------------------
def konf(mod, tidsgyldig, endelig, alfa=0.20, min_kal=3):
    ut = []
    for h, gg in R[R.modell == mod].groupby("h"):
        gg = gg.sort_values("t0").reset_index(drop=True)
        realisert = gg.t0 + pd.DateOffset(months=int(h))
        for i in range(len(gg)):
            ti = gg.t0.iloc[i]
            kal = gg[realisert <= ti] if tidsgyldig else gg.iloc[:i]
            if len(kal) < min_kal: continue
            n = len(kal)
            niva = min(1.0, math.ceil((n+1)*(1-alfa))/n) if endelig else 1-alfa
            q = np.quantile(np.abs(kal.lf.values), niva, method="linear")
            ut.append(dict(h=h, t0=ti, n=n, q=q,
                           dekk=bool(np.exp(gg.mu.iloc[i]-q) <= gg.sant.iloc[i] <= np.exp(gg.mu.iloc[i]+q))))
    return pd.DataFrame(ut)

A  = konf("M0", False, False);  B  = konf("M0", True, False)
Ak = konf("M0", False, True);   Bk = konf("M0", True, True)
f = A.merge(B, on=["h","t0"], suffixes=("_a","_b"))
fk = Ak.merge(Bk, on=["h","t0"], suffixes=("_a","_b"))
print(f"\n[R2] Felles punkter: {len(f)} (paastand 270)")
print(f"[R2] Empirisk kvantil : AV1-skjema {100*f.dekk_a.mean():.1f} %  |  tidsgyldig {100*f.dekk_b.mean():.1f} %  (paastand 78,5 / 67,4)")
print(f"[R2] Bare AV1 dekker: {int((f.dekk_a&~f.dekk_b).sum())} (paastand 32), bare tidsgyldig: {int((~f.dekk_a&f.dekk_b).sum())} (paastand 2)")
rr = f.q_a/f.q_b
print(f"[R2] q_A/q_B: median {rr.median():.2f} snitt {rr.mean():.2f} maks {rr.max():.1f} (paastand 1,00 / 1,28 / 5,8); q_B>q_A i {int((rr<1).sum())} av {len(rr)} (paastand 135)")
print(f"[R3] Endelig utvalg  : AV1-skjema {100*fk.dekk_a.mean():.1f} %  |  tidsgyldig {100*fk.dekk_b.mean():.1f} %")
print(f"[R3] Lekkasje, empirisk: {100*(f.dekk_a.mean()-f.dekk_b.mean()):.1f} pp; endelig: {100*(fk.dekk_a.mean()-fk.dekk_b.mean()):.1f} pp (paastand 11,1 -> 11,9)")
print(f"[R3] Underdekning tidsgyldig: empirisk {80-100*f.dekk_b.mean():.1f} pp; endelig {80-100*fk.dekk_b.mean():.1f} pp (paastand 12,6 -> 5,6)")

# ---- R3b: linear vs higher som ordensstatistikk -----------------------------
print("\n[R3b] np.quantile-metode etter endelig-utvalgsjustering (niva = ceil((n+1)(1-a))/n):")
rng = np.random.default_rng(1)
verste = 0.0; under = 0
for n in range(4, 400):
    s = np.sort(rng.normal(size=n)); k = math.ceil((n+1)*0.8)
    if k > n: continue
    kreves = s[k-1]                       # k-te ordensstatistikk (1-basert)
    lin = np.quantile(s, k/n, method="linear")
    hig = np.quantile(s, k/n, method="higher")
    inv = np.quantile(s, k/n, method="inverted_cdf")
    if lin < kreves - 1e-12: under += 1
    verste = max(verste, float(hig - kreves))
    if n in (18, 19, 30, 304):
        print(f"   n={n:4d} k={k:3d}: kreves s[{k}]={kreves:+.4f}  linear={lin:+.4f}  higher={hig:+.4f}  inverted_cdf={inv:+.4f}")
print(f"   linear < kreves i {under} av testede n  ->  linear er >= k-te ordensstatistikk: {'JA' if under==0 else 'NEI'}")
