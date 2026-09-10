#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura del capitulo 1."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rutas import figura
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

K_LIST = [1, 5, 10, 20, 50, 100]
SIG    = [5, 23, 40, 64, 92, 99]
MEJOR  = [0.14, 0.32, 0.38, 0.43, 0.50, 0.54]

# --- una realizacion TIPICA (no la mas espectacular): busco la primera semilla
#     cuya ganadora caiga cerca de la mediana de 0,43
def z(a): return (a - a.mean())/a.std()
elegido = None
for s in range(500):
    g = np.random.default_rng(s)
    y1 = z(g.standard_normal(24)); y2 = z(g.standard_normal(12))
    X1 = np.array([z(v) for v in g.standard_normal((20, 24))])
    X2 = np.array([z(v) for v in g.standard_normal((20, 12))])
    r1 = np.array([np.mean(x*y1) for x in X1])
    j = int(np.abs(r1).argmax())
    if 0.42 <= abs(r1[j]) <= 0.45:
        r2 = float(np.mean(X2[j]*y2))
        elegido = (y1, X1[j], r1[j], y2, X2[j], r2, s); break
y1, x1, r1g, y2, x2, r2g, s = elegido
print(f"semilla {s}: r primer ano {r1g:+.2f}, ano siguiente {r2g:+.2f}")

fig, ax = plt.subplots(1, 3, figsize=(15.5, 4.8))

ax[0].plot(K_LIST, SIG, "o-", color="#1f4e79", lw=2.4, ms=8)
for k, v in zip(K_LIST, SIG):
    ax[0].text(k, v+4.5, f"{v} %", ha="center", fontsize=9.5, color="#1f4e79")
ax[0].axhline(5, color="#c00000", ls="--", lw=1.8)
ax[0].text(101, 8, "lo que crees que\nte estás jugando: 5 %",
           fontsize=8.5, color="#c00000", ha="right")
ax[0].set_xscale("log"); ax[0].set_ylim(0, 112)
ax[0].set_xlabel("cosas que se te ocurre mirar (escala log)")
ax[0].set_ylabel("% de veces que alguna sale «significativa»")
ax[0].set_title("A · Y no hay nada que encontrar,\nporque no lo hemos puesto", fontsize=11)
ax[0].grid(alpha=.3, which="both")

for k, (xx, yy, rr, tit, c) in enumerate((
        (x1, y1, r1g, "B · La ganadora, el primer año", "#1f4e79"),
        (x2, y2, r2g, "C · La misma, el año siguiente", "#e08214"))):
    a = ax[k+1]
    a.scatter(xx, yy, s=70, color=c, alpha=.75, edgecolor="white", lw=1)
    p = np.polyfit(xx, yy, 1)
    xs = np.linspace(xx.min()-.2, xx.max()+.2, 10)
    a.plot(xs, np.polyval(p, xs), color=c, lw=2, ls="--")
    a.set_xlabel("la variable «que explica las ventas»")
    a.set_ylabel("ventas del mes")
    a.set_title(f"{tit}\ncorrelación r = {rr:+.2f}", fontsize=11)
    a.grid(alpha=.3)
    a.text(.03, .96, f"{len(xx)} meses", transform=a.transAxes, fontsize=9,
           color="#666", va="top")

fig.suptitle("Veinte candidatas, veinticuatro meses. Todas las series están sorteadas: "
             "no hay ninguna relación real en ninguna parte.", fontsize=10.5, y=0.99)
plt.tight_layout(); plt.savefig(figura("fig1_correlaciones.png"), dpi=170)
print("ok")
