#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura del capitulo 9: lo que te ensenarian, y la linea que falta."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rutas import figura, datos
import csv, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

bl = list(csv.DictReader(open(datos("cap09_bloques.csv"))))
ac = np.array([float(r["acierto"]) for r in bl])*100
n  = np.array([int(r["n_disparos"]) for r in bl])
glob = 100*np.sum(ac/100*n)/n.sum()
ec = list(csv.DictReader(open(datos("cap09_costes.csv"))))

print(f"bloques: {len(bl)}  acierto global ponderado: {glob:.2f} %")
print(f"  mejor {ac.max():.2f} %   peor {ac.min():.2f} %   bloques por debajo de 50: {(ac<50).sum()}")

fig, ax = plt.subplots(1, 2, figsize=(13.5, 5.2))

x = np.arange(len(ac)); j = int(np.argmax(ac))
col = ["#b8c4d0"]*len(ac); col[j] = "#e08214"
ax[0].bar(x, ac-50, bottom=50, color=col)
ax[0].axhline(50, color="#666", lw=1.5)
ax[0].axhline(glob, color="#1f4e79", ls="--", lw=2)
ax[0].text(len(ac)-0.4, glob+0.35, f"todos los bloques juntos: {glob:.2f} %".replace(".", ","),
           fontsize=9, color="#1f4e79", ha="right")
ax[0].annotate(f"{ac[j]:.1f} %\nesto es lo que te enseñarían".replace(".", ","),
               xy=(j, ac[j]), xytext=(j+1.2, 58.6), fontsize=9, color="#a63603",
               arrowprops=dict(arrowstyle="->", color="#a63603", lw=1.2))
ax[0].set_ylim(46, 60); ax[0].set_xticks([]); ax[0].set_xlabel("18 bloques consecutivos, en orden")
ax[0].set_ylabel("aciertos (%)")
ax[0].set_title("A · La misma regla, trozo a trozo\n(el azar puro daría 50 %)", fontsize=11)
ax[0].grid(alpha=.3, axis="y")

etq = ["como cliente, al precio\nque te ofrecen, con comisión",
       "como cliente, al precio\njusto, con comisión",
       "como cliente, al precio que\nte ofrecen, SIN comisión",
       "como la casa, precio 0,50\nSIN comisión",
       "como la casa, precio 0,49\nSIN comisión"]
val = [float(r["pct_nocional"]) for r in ec]
col2 = ["#c0392b" if v < 0 else "#1f4e79" for v in val]
b = ax[1].barh(np.arange(5), val, color=col2)
for r, v in zip(b, val):
    ax[1].text(v + (0.14 if v > 0 else -0.14), r.get_y()+r.get_height()/2,
               f"{v:+.2f}".replace(".", ","), va="center", ha="left" if v > 0 else "right",
               fontsize=10.5, fontweight="bold")
ax[1].axvline(0, color="#666", lw=1.5)
ax[1].set_yticks(np.arange(5)); ax[1].set_yticklabels(etq, fontsize=8.5)
ax[1].invert_yaxis(); ax[1].set_xlim(-3.0, 4.6)
ax[1].set_xlabel("céntimos que deja cada contrato que paga 1 $")
ax[1].set_title("B · La ventaja es real. La línea del coste\nno está en el documento.", fontsize=11)
ax[1].grid(alpha=.3, axis="x")

coma = lambda x: f"{x:.2f}".replace(".", ",")
fig.suptitle(f"70.729 apuestas reales. En los meses que no se usaron para diseñarla, la regla acierta el {coma(glob)} %: "
             f"{coma(glob-50)} céntimos por contrato, antes de pagar por entrar.",
             fontsize=10.5, y=0.995)
plt.tight_layout(); plt.savefig(figura("fig9_senal.png"), dpi=170)
print("ok")
