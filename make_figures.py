"""make_figures.py - figures for the Ibdaa 2027 Qalib, drawn only from files in this repo.
Run after analysis_summer.py:  python make_figures.py --out figures"""
import argparse, os, sys
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import PRC

INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": MUTED,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 300, "figure.facecolor": "white"})
ORDER = ["Al Baha", "Dhahran", "Jeddah", "Al Wajh"]
LABEL = {"Al Baha": "Al Baha", "Dhahran": "Dhahran", "Jeddah": "Jeddah", "Al Wajh": "Al Wajh"}
SHORT = {"BaSO4-acrylic paint": "BaSO₄ paint", "BaSO4 nanoparticle film": "BaSO₄ film",
         "Hierarchically porous P(VdF-HFP) coating": "Porous P(VdF-HFP)", "CaCO3 paint": "CaCO₃ paint",
         "Commercial white paint (control)": "White paint (control)"}

def fig_results(res, out):
    s = pd.read_csv(os.path.join(res, "summary_by_material_station.csv"))
    s = s[s.material.isin(SHORT)]
    mats = list(SHORT)
    fig, axes = plt.subplots(1, 4, figsize=(10, 3.4), sharey=True, sharex=True)
    for ax, st in zip(axes, ORDER):
        d = s[s.station == st].set_index("material").loc[mats]
        y = np.arange(len(mats))[::-1]
        for yi, (m, r) in zip(y, d.iterrows()):
            c = ORANGE if "control" in m else BLUE
            ax.plot([r.p25_dT, r.p75_dT], [yi, yi], color=c, lw=5, solid_capstyle="round", alpha=.3)
            ax.plot(r.median_dT, yi, "o", ms=8, color=c, mec="white", mew=1.5, zorder=3)
            ax.text(r.median_dT, yi + .38, f"{r.median_dT:+.1f}".replace("-", "−"), ha="center", fontsize=8, color=INK2)
        ax.axvline(0, color=INK2, lw=1)
        ax.set_title(LABEL[st], fontsize=10, color=INK, loc="left")
        ax.grid(axis="x", color=GRID, lw=.8); ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
    axes[0].set_yticks(np.arange(len(mats))[::-1]); axes[0].set_yticklabels([SHORT[m] for m in mats])
    axes[0].set_ylim(-.6, len(mats) - .2)
    fig.supxlabel("Surface minus air temperature, ΔT (°C)   ← cooler than air | warmer than air →", fontsize=9, color=INK2)
    fig.tight_layout(); fig.savefig(os.path.join(out, "fig_results_dT.png")); plt.close(fig)

def fig_threshold(res, out):
    t = pd.read_csv(os.path.join(res, "alpha_threshold.csv")).set_index("station").loc[ORDER]
    need = (1 - t.max_alpha_for_median_below_air) * 100
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    x = np.arange(4)
    ax.bar(x, need - 80, bottom=80, width=.55, color=BLUE, edgecolor="white", lw=2)
    for xi, v in zip(x, need):
        ax.text(xi, v - .9, f"{v:.1f}%", ha="center", fontsize=9, color="white", fontweight="bold")
    refs = [(98.1, "BaSO₄ paint 98.1%"), (95.5, "CaCO₃ paint 95.5%"), (87.2, "White paint 87.2%")]
    for v, lab in refs:
        ax.axhline(v, color=ORANGE if "White" in lab else INK2, lw=1.2, ls="--")
        ax.text(4.55, v + .25, lab, ha="right", va="bottom", fontsize=8.5, color=INK2)
    ax.set_xticks(x); ax.set_xticklabels([LABEL[s] for s in ORDER]); ax.set_xlim(-.5, 4.6)
    ax.set_ylim(80, 100); ax.set_ylabel("Solar reflectance needed (%)")
    ax.grid(axis="y", color=GRID, lw=.8); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(os.path.join(out, "fig_reflectance_threshold.png")); plt.close(fig)

def fig_climate(out):
    rows = []
    for c in PRC.city_profiles:
        df = PRC.load_epw_weather(c); jja = df[df[1].isin([6, 7, 8])]
        st = [k for k in LABEL if c.startswith(k)][0]
        rows.append((LABEL[st], jja[PRC.epwDewPointCol].mean(), jja[PRC.epwDryBulbTempCol].mean()))
    d = pd.DataFrame(rows, columns=["st", "dew", "t"]).sort_values("dew")
    fig, ax = plt.subplots(figsize=(6.4, 2.8))
    y = np.arange(len(d))
    ax.barh(y, d.dew, height=.55, color=BLUE, edgecolor="white", lw=2)
    for yi, v in zip(y, d.dew): ax.text(v + .4, yi, f"{v:.1f} °C", va="center", fontsize=9)
    elev = {"Al Baha": "1,672 m", "Dhahran": "26 m", "Jeddah": "15 m", "Al Wajh": "20 m"}
    ax.set_yticks(y); ax.set_yticklabels([f"{s}  ({elev[s]})" for s in d.st])
    ax.set_xlabel("Mean June–August dew point (°C)"); ax.set_xlim(0, 27)
    ax.grid(axis="x", color=GRID, lw=.8); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
    fig.tight_layout(); fig.savefig(os.path.join(out, "fig_climate_dewpoint.png")); plt.close(fig)
    return d

def _box(ax, x, y, w, h, txt, fc="#eef4fc", ec=BLUE, fs=9):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.02,rounding_size=0.06", fc=fc, ec=ec, lw=1.2))
    ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=INK, linespacing=1.3)

def _arrow(ax, a, b, c=INK2, lw=1.4):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color=c, lw=lw))

def fig_flowchart(out):
    fig, ax = plt.subplots(figsize=(7.2, 4.4)); ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")
    _box(ax, 2.3, 5.4, 3.8, .9, "Weather: 4 TMYx files [4]\nJun–Aug hours, GHI > 600 W/m²")
    _box(ax, 7.7, 5.4, 3.8, .9, "Materials: 4 PDRC + control\nα, ε checked in papers [10, 24, 25]")
    _box(ax, 5, 3.9, 6.2, .95, "Energy balance for every hour × material × station\nsky emissivity [21], convection [22, 23], Brent solver")
    _box(ax, 1.8, 2.2, 3.0, .95, "Ranking\n(Objective 2)")
    _box(ax, 5, 2.2, 3.0, .95, "Sensitivity ±0.02\n+ α threshold (Obj. 3)")
    _box(ax, 8.2, 2.2, 3.0, .95, "Robustness\nGHI 400/800, L 0.1/10 m")
    _box(ax, 5, .7, 8.4, .8, "Validation (Objective 4): compare with fully reported, unshielded experiments\n— not completed: no qualifying experiment found",
         fc="#f6f5f2", ec=MUTED, fs=8.5)
    _arrow(ax, (2.3, 4.95), (3.6, 4.4)); _arrow(ax, (7.7, 4.95), (6.4, 4.4))
    for x in (1.8, 5, 8.2): _arrow(ax, (5 + (x - 5) * .45, 3.42), (x, 2.7))
    _arrow(ax, (5, 1.72), (5, 1.12), c=MUTED)
    fig.tight_layout(); fig.savefig(os.path.join(out, "fig_method_flowchart.png")); plt.close(fig)

def fig_heat_balance(out):
    fig, ax = plt.subplots(figsize=(7.2, 4.4)); ax.set_xlim(0, 10); ax.set_ylim(-0.3, 6); ax.axis("off")
    ax.add_patch(Rectangle((1, 1.2), 8, .35, fc="#dbe8f8", ec=BLUE, lw=1.2))
    ax.add_patch(Rectangle((1, .75), 8, .45, fc="#f1f0ec", ec=MUTED, lw=1, hatch="///"))
    ax.text(5, 1.375, "PDRC coating  (α, ε)", ha="center", va="center", fontsize=9)
    ax.text(5, .5, "Roof below, treated as insulated (no heat flow)", ha="center", fontsize=8.5, color=INK2)
    def lab(x, y, t, c=INK, ha="center"): ax.text(x, y, t, ha=ha, va="center", fontsize=9, color=c, linespacing=1.3)
    _arrow(ax, (1.8, 5.3), (2.4, 1.65), c=ORANGE, lw=2); lab(0.2, 5.55, "Sunlight\nα·GHI absorbed", ORANGE, "left")
    _arrow(ax, (4.2, 1.65), (4.2, 5.2), c=BLUE, lw=2); lab(4.2, 5.55, "Emitted infrared\nε σ Tₛ⁴", BLUE)
    _arrow(ax, (6.2, 5.2), (6.2, 1.65), c=INK2, lw=2); lab(6.2, 5.55, "Sky infrared absorbed\nε ε_sky σ Tₐᵢᵣ⁴", INK2)
    ax.annotate("", xy=(8.9, 2.3), xytext=(7.1, 2.3), arrowprops=dict(arrowstyle="<|-|>", color=AQUA, lw=2))
    lab(8.0, 2.85, "Convection with air\nh_c (Tₛ − Tₐᵢᵣ)", "#127a55")
    lab(5, 0.05, "Steady state:  ε σ Tₛ⁴ − ε ε_sky σ Tₐᵢᵣ⁴ − α·GHI + h_c (Tₛ − Tₐᵢᵣ) = 0", INK)
    fig.tight_layout(); fig.savefig(os.path.join(out, "fig_heat_balance.png")); plt.close(fig)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--results", default=os.path.join(HERE, "results"))
    ap.add_argument("--out", default=os.path.join(HERE, "figures")); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    fig_results(a.results, a.out); fig_threshold(a.results, a.out)
    print(fig_climate(a.out)); fig_flowchart(a.out); fig_heat_balance(a.out)
    print("Figures written to", a.out)
