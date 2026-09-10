#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cap02_tiendas.py — un plan de mejora que no hace nada, y funciona.

Mil tiendas. Cada una tiene un nivel de ventas propio, estable, y cada año le
suma o le resta su suerte. Se eligen las 200 peores del primer año, se reparten
por sorteo en dos grupos de 100: uno recibe un «plan de mejora» y el otro no.
El plan NO HACE NADA: por construccion, su efecto es cero.

La pregunta es que se ve el segundo año:
  - contra nada (antes y despues)        -> el plan parece funcionar
  - contra el grupo que no lo recibio    -> el plan no hace nada, que es la verdad

Todo se repite 2.000 veces con semilla fija.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rutas import figura
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

N, MEDIA, NIVEL, SUERTE = 1000, 100.0, 10.0, 10.0   # suerte anual tan grande como la diferencia entre tiendas
PEORES, REPS = 200, 2000
EFECTO_DEL_PLAN = 0.0                                # <- el plan no hace nada

rng = np.random.default_rng(20260910)
mejora_plan, mejora_ctrl, mejora_mejores, antes_despues = [], [], [], []
ej = None
for r in range(REPS):
    nivel = rng.normal(MEDIA, NIVEL, N)
    a1 = nivel + rng.normal(0, SUERTE, N)
    a2 = nivel + rng.normal(0, SUERTE, N)
    orden = np.argsort(a1)
    peores = orden[:PEORES]
    rng.shuffle(peores)
    plan, ctrl = peores[:PEORES // 2], peores[PEORES // 2:]
    a2p = a2.copy(); a2p[plan] += EFECTO_DEL_PLAN
    m_plan = 100 * (a2p[plan].mean() / a1[plan].mean() - 1)
    m_ctrl = 100 * (a2p[ctrl].mean() / a1[ctrl].mean() - 1)
    mejores = orden[-100:]
    m_mej = 100 * (a2[mejores].mean() / a1[mejores].mean() - 1)
    mejora_plan.append(m_plan); mejora_ctrl.append(m_ctrl); mejora_mejores.append(m_mej)
    if r == 0:
        ej = (a1, a2p, plan, ctrl)

mp, mc, mm = map(np.array, (mejora_plan, mejora_ctrl, mejora_mejores))
dif = mp - mc
print("=" * 76)
print("UN PLAN DE MEJORA QUE NO HACE NADA (efecto real = 0)")
print("=" * 76)
print(f"  {N} tiendas; se eligen las {PEORES} peores del ano 1; 100 reciben el plan, 100 no")
print(f"  repeticiones: {REPS}\n")
print(f"  {'':44}{'mediana':>10}{'p5':>9}{'p95':>9}")
print(f"  {'tiendas con plan: cambio de ventas, ano 1 a 2':44}{np.median(mp):>9.1f}%{np.percentile(mp,5):>8.1f}%{np.percentile(mp,95):>8.1f}%")
print(f"  {'tiendas SIN plan (las otras peores)':44}{np.median(mc):>9.1f}%{np.percentile(mc,5):>8.1f}%{np.percentile(mc,95):>8.1f}%")
print(f"  {'diferencia: el efecto del plan':44}{np.median(dif):>9.1f}%{np.percentile(dif,5):>8.1f}%{np.percentile(dif,95):>8.1f}%")
print(f"  {'las 100 MEJORES del ano 1 (sin tocar)':44}{np.median(mm):>9.1f}%{np.percentile(mm,5):>8.1f}%{np.percentile(mm,95):>8.1f}%")
print(f"\n  el plan 'mejora' las ventas en {100*(mp>0).mean():.1f} % de las repeticiones")
print(f"  el plan supera al grupo sin plan en {100*(dif>0).mean():.1f} % (una moneda da 50 %)")

# ---------- cuanto depende del peso de la suerte -------------------------------
print("\n  mejora aparente de las 200 peores segun cuanto pese la suerte de cada ano")
print("  (suerte medida en las mismas unidades que la diferencia entre tiendas, 10)")
rs = np.random.default_rng(7)
for su in (2.5, 5.0, 10.0, 20.0):
    ms = []
    for _ in range(500):
        nv = rs.normal(MEDIA, NIVEL, N)
        b1 = nv + rs.normal(0, su, N); b2 = nv + rs.normal(0, su, N)
        pe = np.argsort(b1)[:PEORES]
        ms.append(100 * (b2[pe].mean() / b1[pe].mean() - 1))
    print(f"    suerte {su:>5.1f}  ->  las peores 'mejoran' un {np.median(ms):5.1f} %")

# ---------- figura ------------------------------------------------------------
a1, a2, plan, ctrl = ej
fig, ax = plt.subplots(1, 2, figsize=(13.5, 5.0))
ax[0].scatter(a1, a2, s=6, color="#c9d6e3", label="las 1.000 tiendas")
ax[0].scatter(a1[plan], a2[plan], s=18, color="#e08214", label="las peores, con plan")
ax[0].scatter(a1[ctrl], a2[ctrl], s=18, color="#1f4e79", label="las peores, sin plan")
lim = [a1.min() - 3, a1.max() + 3]
ax[0].plot(lim, lim, color="#666", lw=1, ls="--")
ax[0].text(lim[1] - 1, lim[1] - 22, "por encima de la línea\ndiscontinua: mejoró", ha="right", fontsize=8.5, color="#666")
ax[0].set_xlabel("ventas del año 1"); ax[0].set_ylabel("ventas del año 2")
ax[0].set_title("A · Las peores del año 1 mejoran el año 2…\ncon plan y sin plan", fontsize=11)
ax[0].legend(fontsize=8.5, loc="upper left"); ax[0].grid(alpha=.3)

coma = lambda x: f"{x:+.1f} %".replace(".", ",")
et = ["con plan\n(contra nada)", "sin plan", "el efecto\ndel plan"]
v = [np.median(mp), np.median(mc), np.median(dif)]
b = ax[1].bar(range(3), v, 0.6, color=["#e08214", "#1f4e79", "#666"])
for rr, x in zip(b, v):
    ax[1].text(rr.get_x() + rr.get_width() / 2, x + 0.4 if x >= 0 else x - 1.2, coma(x),
               ha="center", fontsize=11, fontweight="bold")
ax[1].axhline(0, color="#666", lw=1)
ax[1].set_ylim(min(0, min(v)) - 1.5, max(v) + 2.5)
ax[1].set_xticks(range(3)); ax[1].set_xticklabels(et, fontsize=9.5)
ax[1].set_ylabel("cambio de ventas del año 1 al 2 (mediana)")
ax[1].set_title("B · Contra nada, el plan funciona.\nContra quien no lo recibió, no hace nada.", fontsize=11)
ax[1].grid(alpha=.3, axis="y")
fig.suptitle("El plan de esta simulación no hace absolutamente nada. Lo que se ve es suerte que vuelve a su sitio.",
             fontsize=10.5, y=0.995)
plt.tight_layout(); plt.savefig(figura("fig2_tiendas.png"), dpi=170)
print("\n  figura: fig2_tiendas.png")
