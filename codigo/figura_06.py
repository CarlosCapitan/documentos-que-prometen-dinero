#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura del capitulo 6."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rutas import figura
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

FR = {2010:(41.35,22.87,12.84,2.17,-5.10), 2012:(43.19,28.10,17.50,11.04,1.49),
      2014:(32.75,23.12,15.55,10.47,5.05), 2016:(35.46,25.23,16.23,10.20,4.90),
      2018:(32.16,22.20,12.67,6.10,3.24),  2020:(25.21,17.05,10.21,5.20,0.28)}
A = sorted(FR); x = np.arange(len(A))
d90 = [FR[a][0] for a in A]; q1 = [FR[a][1] for a in A]
me  = [FR[a][2] for a in A]; q3 = [FR[a][3] for a in A]; d10 = [FR[a][4] for a in A]

fig, ax = plt.subplots(1, 2, figsize=(13.5, 5.2))

ax[0].axhspan(20, 25, color="#e08214", alpha=.18, zorder=0)
ax[0].text(5.42, 22.5, "«un 20-25 %»", fontsize=9.5, color="#a63603",
           ha="right", va="center", fontweight="bold")
ax[0].vlines(x, d10, d90, color="#c9d6e3", lw=13, zorder=1)
ax[0].vlines(x, q3, q1, color="#7f9fc0", lw=13, zorder=2)
ax[0].plot(x, me, "o-", color="#1f4e79", lw=2.2, ms=9, zorder=4, label="mediana")
ax[0].plot(x, q1, "_", color="#0d2d4d", ms=22, mew=2.5, zorder=5, label="frontera del 25 % mejor (1er cuartil)")
ax[0].axhline(0, color="#666", lw=1)
for i, a in enumerate(A):
    ax[0].text(i, d90[i]+1.4, f"{d90[i]:.0f}", ha="center", fontsize=8, color="#666")
    ax[0].text(i, d10[i]-3.0, f"{d10[i]:.0f}", ha="center", fontsize=8, color="#666")
ax[0].set_xticks(x); ax[0].set_xticklabels(A)
ax[0].set_xlabel("año de creación del fondo"); ax[0].set_ylabel("rentabilidad anual neta (%)")
ax[0].set_ylim(-9, 48)
ax[0].set_title("A · La frase describe el primer cuartil,\nno la experiencia típica", fontsize=11)
ax[0].legend(fontsize=9, loc="upper right"); ax[0].grid(alpha=.3, axis="y")

etq = ["una sola manera\n(lo honesto)", "elegir entre\n3 formas de medir",
       "elegir el año\n(±1)", "las dos cosas:\n9 combinaciones"]
val = [25.1, 37.3, 32.4, 46.0]
col = ["#1f4e79", "#7f9fc0", "#7f9fc0", "#e08214"]
b = ax[1].bar(np.arange(4), val, 0.62, color=col)
for r, v in zip(b, val):
    ax[1].text(r.get_x()+r.get_width()/2, v+1.2, f"{v:.1f} %".replace(".", ","), ha="center",
               fontsize=11, fontweight="bold")
ax[1].axhline(25, color="#c00000", ls="--", lw=1.8)
ax[1].text(3.42, 26.3, "lo que la palabra «cuartil» garantiza", fontsize=8.5,
           color="#c00000", ha="right")
ax[1].axhline(50, color="#666", ls=":", lw=1.5)
ax[1].text(3.42, 51.3, "Harris y Stucke midieron «la mitad» con datos reales",
           fontsize=8.5, color="#666", ha="right")
ax[1].set_xticks(np.arange(4)); ax[1].set_xticklabels(etq, fontsize=9)
ax[1].set_ylim(0, 60); ax[1].set_ylabel("% que puede decir, con razón, que es primer cuartil")
ax[1].set_title("B · Ninguna de esas elecciones es mentira", fontsize=11)
ax[1].grid(alpha=.3, axis="y")

fig.suptitle("Fronteras reales: PitchBook Benchmarks Q4 2024, rentabilidad anual neta, capital riesgo global, datos a 31-12-2024.",
             fontsize=10.5, y=0.995)
plt.tight_layout(); plt.savefig(figura("fig6_cuartiles.png"), dpi=170)
print("ok")
