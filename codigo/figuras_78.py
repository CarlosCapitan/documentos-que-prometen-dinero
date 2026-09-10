#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figuras de los capitulos 7 y 8."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rutas import figura
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

# ============ FIGURA 7 · las rachas ==========================================
def p_racha(n, k, p):
    est = np.zeros(k); est[0] = 1.0; log = 0.0
    for _ in range(n):
        nue = np.zeros(k); nue[0] = est.sum()*(1-p); nue[1:] = est[:-1]*p
        log += est[k-1]*p; est = nue
    return log

fig, ax = plt.subplots(1, 2, figsize=(13.5, 5.0))
Ns = np.array([100, 1_000, 5_000, 20_000, 100_000])
for k, c in zip((5, 7, 9), ("#b8c4d0", "#7f9fc0", "#1f4e79")):
    esp = Ns * p_racha(10, k, 0.5)
    ax[0].plot(Ns, esp, "o-", color=c, lw=2, ms=6, label=f"{k} años seguidos")
ax[0].axhline(1, color="#c00000", ls="--", lw=1.8)
ax[0].text(1.05e5, 1.5, "por debajo de aquí ya no se espera ver ninguno",
           fontsize=8.5, color="#c00000", ha="right")
ax[0].set_xscale("log"); ax[0].set_yscale("log")
ax[0].set_xlabel("gestores en el mercado (escala log)")
ax[0].set_ylabel("cuántos lo consiguen SIN habilidad (escala log)")
ax[0].set_title("A · Rachas que aparecen solas\n(10 años, moneda justa)", fontsize=11)
ax[0].legend(fontsize=9, loc="upper left"); ax[0].grid(alpha=.3, which="both")

etq = ["sin cierres", "cierra el 15 %\npeor cada año"]
tasa = [50.0, 66.9]; racha = [1.90, 7.22]
x = np.arange(2); w = 0.35
b1 = ax[1].bar(x-w/2, tasa, w, color="#1f4e79", label="años batiendo al índice (%)")
b2 = ax[1].bar(x+w/2, racha, w, color="#e08214", label="con ≥7 seguidos (% de los vivos)")
for b in list(b1)+list(b2):
    ax[1].text(b.get_x()+b.get_width()/2, b.get_height()+1.2,
               f"{b.get_height():.1f} %", ha="center", fontsize=9.5)
ax[1].axhline(50, color="#c00000", ls="--", lw=1.5)
ax[1].text(1.45, 52, "lo que da una moneda justa", fontsize=8.5, color="#c00000", ha="right")
ax[1].set_xticks(x); ax[1].set_xticklabels(etq, fontsize=9.5)
ax[1].set_ylim(0, 78); ax[1].legend(fontsize=9); ax[1].grid(alpha=.3, axis="y")
ax[1].set_title("B · El sesgo del superviviente\n20.000 gestores, cero habilidad", fontsize=11)
fig.suptitle("Nadie tiene habilidad en esta simulación. Todo lo que se ve es azar y supervivencia.",
             fontsize=10.5, y=0.995)
plt.tight_layout(); plt.savefig(figura("fig7_rachas.png"), dpi=170)
print("fig 7 ok")

# ============ FIGURA 8 · el backtest sobre ruido =============================
d = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cap08_datos.npz"), allow_pickle=True)
IN, OUT, r, nombre = d["IN"], d["OUT"], d["r_gan"], str(d["nombre"][0])
CORTE = 2000
eq = np.cumprod(1 + r)

fig, ax = plt.subplots(1, 2, figsize=(13.5, 5.0))
ax[0].plot(np.arange(CORTE)/252, eq[:CORTE], color="#1f4e79", lw=2,
           label="los ocho años en que se eligió")
ax[0].plot(np.arange(CORTE, len(eq))/252, eq[CORTE:], color="#e08214", lw=2,
           label="los cuatro años siguientes")
ax[0].axvline(CORTE/252, color="#c00000", ls="--", lw=1.8)
ax[0].axhline(1, color="#999", lw=1)
ax[0].annotate("aquí acaba el periodo\nen el que se eligió",
               xy=(CORTE/252, eq[CORTE]), xytext=(3.0, eq[:CORTE].max()*0.98),
               fontsize=8.5, color="#c00000",
               arrowprops=dict(arrowstyle="->", color="#c00000", lw=1))
ax[0].set_xlabel("años"); ax[0].set_ylabel("capital (empieza en 1)")
ax[0].set_title("A · La mejor de 207 reglas sobre precios sorteados\n«impulso 25/80» — y esta siguió subiendo", fontsize=11)
ax[0].legend(fontsize=9, loc="upper left"); ax[0].grid(alpha=.3)

ax[1].scatter(IN, OUT, s=26, color="#1f4e79", alpha=.55, edgecolor="none")
ax[1].axhline(0, color="#666", lw=1); ax[1].axvline(0, color="#666", lw=1)
ax[1].axhline(np.median(OUT), color="#c00000", ls="--", lw=1.8)
ax[1].text(0.16, np.median(OUT)+0.09, f"lo normal después: {np.median(OUT):+.2f}".replace(".", ","),
           fontsize=8.5, color="#c00000")
ax[1].set_xlabel("Sharpe de la ganadora, en los años en que se eligió")
ax[1].set_ylabel("el mismo, en los cuatro años siguientes")
ax[1].set_title(f"B · 300 series sin nada dentro\nrelación entre antes y después: {np.corrcoef(IN,OUT)[0,1]:+.3f}".replace(".", ","),
                fontsize=11)
ax[1].grid(alpha=.3)
fig.suptitle("Los precios se generaron sorteando: por construcción no hay nada que predecir.\n"
             "El panel A es una anécdota. El B es la razón por la que una anécdota no vale.",
             fontsize=10.5, y=1.0)
plt.tight_layout(); plt.savefig(figura("fig8_backtest.png"), dpi=170)
print("fig 8 ok")
