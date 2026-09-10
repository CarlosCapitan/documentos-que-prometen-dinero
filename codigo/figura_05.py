#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura 5 — la diversificacion deja de funcionar cuando hay un factor comun."""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from rutas import figura
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

# Los numeros NO se teclean: salen de cap05_montecarlo.py (ejecutarlo antes).
d = np.load(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "cap05_datos.npz"))
N = list(d["N"])
ETQ = ["independiente", "ciclo suave (σ=0,30)", "ciclo moderado (σ=0,50)", "ciclo fuerte (σ=0,80)"]
P1 = {e: list(100 * d["p_recuperar"][k]) for k, e in enumerate(ETQ)}
SD = {e: list(d["sd"][k]) for k, e in enumerate(ETQ)}
SUELO_08 = 100 * float(d["suelo_08"])
COL = {"independiente": "#1f4e79", "ciclo suave (σ=0,30)": "#7f9fc0",
       "ciclo moderado (σ=0,50)": "#e08214", "ciclo fuerte (σ=0,80)": "#a63603"}

fig, ax = plt.subplots(1, 2, figsize=(13.5, 5.0))

SUELO = 100/60_000          # 0 de 60.000 simulaciones: no se puede medir mas abajo
for k, v in P1.items():
    y = 100-np.array(v)
    vis = np.where(y <= 0, SUELO, y)
    ax[0].plot(N, vis, "o-", color=COL[k], label=k, lw=2, ms=5,
               markerfacecolor=["white" if a <= 0 else COL[k] for a in y][0] if False else None)
    cero = y <= 0
    if cero.any():
        ax[0].plot(np.array(N)[cero], np.full(cero.sum(), SUELO), "o",
                   color=COL[k], markerfacecolor="white", ms=6, zorder=5)
ax[0].axhline(SUELO, color="#999", ls=":", lw=1)
ax[0].text(1000, SUELO*1.35, "límite de resolución: 0 de 60.000 simulaciones",
           fontsize=7.5, color="#666", ha="right")
ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_ylim(SUELO*0.6, 80)
ax[0].set_xlabel("compañías en la cartera (escala log)")
ax[0].set_ylabel("% de carteras que pierden dinero (escala log)")
ax[0].set_title("A · Probabilidad de NO recuperar lo invertido", fontsize=11)
ax[0].annotate("independientes: se hunde.\nLa ley de los grandes\nnúmeros funciona",
               xy=(200, SUELO), xytext=(150, 0.012), fontsize=8.5, color="#1f4e79",
               arrowprops=dict(arrowstyle="->", color="#1f4e79", lw=1))
ax[0].annotate("con factor de ciclo tiende a un\nsuelo del 10,2 %: no se va por\nmuchas compañías que compres",
               xy=(1000, 10.6), xytext=(12, 0.9), fontsize=8.5, color="#a63603",
               arrowprops=dict(arrowstyle="->", color="#a63603", lw=1))
ax[0].legend(fontsize=8.5, loc="lower left"); ax[0].grid(alpha=.3, which="both")

for k, v in SD.items():
    ax[1].plot(N, v, "o-", color=COL[k], label=k, lw=2, ms=5)
ax[1].set_xscale("log"); ax[1].set_yscale("log")
ax[1].set_xlabel("compañías en la cartera (escala log)")
ax[1].set_ylabel("desviación típica del múltiplo de la cartera")
ax[1].set_title("B · El riesgo que la diversificación no quita", fontsize=11)
ax[1].annotate("cae como 1/√N", xy=(500, 0.608), xytext=(120, 0.5),
               fontsize=8.5, color="#1f4e79",
               arrowprops=dict(arrowstyle="->", color="#1f4e79", lw=1))
ax[1].annotate("suelo", xy=(1000, 3.639), xytext=(400, 6.0), fontsize=9, color="#a63603",
               arrowprops=dict(arrowstyle="->", color="#a63603", lw=1))
ax[1].legend(fontsize=8.5, loc="lower left"); ax[1].grid(alpha=.3, which="both")

fig.suptitle("La misma distribución de resultados, la misma media de 3,8×. "
             "Lo único que cambia es la independencia.", fontsize=10.5, y=0.995)
plt.tight_layout()
# suelo exacto con infinitas companias (sigma = 0,80), calculado en montecarlo.py
ax[0].axhline(SUELO_08, color="#a63603", ls=":", lw=1.2)
plt.savefig(figura("fig5_diversificacion.png"), dpi=170)
print("ok")
