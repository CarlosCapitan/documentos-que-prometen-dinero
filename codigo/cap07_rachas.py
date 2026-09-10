#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cap07_rachas.py — cuantos gestores hacen falta para que uno parezca un genio.

Nadie tiene habilidad en esta simulacion. Cada gestor bate a su indice o no lo
bate por puro azar. La pregunta es cuantos anos seguidos de acierto aparecen
solos, y cuantos hacen falta para que signifiquen algo.

Se calcula de dos maneras independientes -exacta por programacion dinamica y
por simulacion- y se comprueba que coinciden. Si no coincidieran, una de las dos
estaria mal, y no habria forma de saber cual sin la otra.
"""
import numpy as np

# ---------- 1. probabilidad exacta de una racha, por programacion dinamica ----
def p_racha(n, k, p):
    """P(hay al menos k aciertos SEGUIDOS en n anos), con probabilidad p por ano.
    Estado = aciertos consecutivos acumulados (0..k-1) mas un estado absorbente."""
    est = np.zeros(k); est[0] = 1.0; logrado = 0.0
    for _ in range(n):
        nue = np.zeros(k)
        nue[0] = est.sum() * (1 - p)                 # falla: vuelve a cero
        nue[1:] = est[:-1] * p                       # acierta: avanza
        logrado += est[k-1] * p                      # alcanza la racha k
        est = nue
    return logrado

def p_racha_sim(n, k, p, reps, rng):
    x = rng.random((reps, n)) < p
    fin = np.zeros(reps, bool); run = np.zeros(reps, int)
    for j in range(n):
        run = np.where(x[:, j], run + 1, 0)
        fin |= run >= k
    return fin.mean()

rng = np.random.default_rng(20260909)
print("="*78)
print("COMPROBACION: exacto frente a simulacion (1.000.000 de gestores)")
print("="*78)
print(f"{'anos':>6}{'racha':>7}{'p/ano':>8}{'exacto':>12}{'simulado':>12}{'dif':>10}")
for n, k, p in ((10,7,0.5), (10,5,0.5), (20,7,0.5), (10,7,0.44), (15,10,0.5)):
    e = p_racha(n, k, p); s = p_racha_sim(n, k, p, 1_000_000, rng)
    print(f"{n:>6}{k:>7}{p:>8.2f}{e:>12.6f}{s:>12.6f}{abs(e-s):>10.6f}")

# ---------- 2. cuantos genios aparecen solos -----------------------------------
print("\n" + "="*78)
print("SIETE ANOS SEGUIDOS BATIENDO AL INDICE, SIN NINGUNA HABILIDAD")
print("="*78)
print("p = 0,50 por ano: la moneda justa, antes de comisiones.")
p1 = p_racha(10, 7, 0.50)
print(f"  probabilidad para UN gestor concreto en 10 anos : {p1:.5f}  (1 de cada {1/p1:,.0f})")
print(f"\n{'gestores':>12}{'esperados con >=7 seguidos':>30}{'P(al menos uno)':>20}")
for N in (100, 1_000, 5_000, 20_000, 100_000):
    print(f"{N:>12,}{N*p1:>30,.1f}{1-(1-p1)**N:>20.4f}")

print("\np = 0,44 por ano: lo mismo despues de comisiones tipicas.")
p2 = p_racha(10, 7, 0.44)
print(f"  probabilidad para UN gestor concreto en 10 anos : {p2:.5f}  (1 de cada {1/p2:,.0f})")
print(f"\n{'gestores':>12}{'esperados con >=7 seguidos':>30}{'P(al menos uno)':>20}")
for N in (100, 1_000, 5_000, 20_000, 100_000):
    print(f"{N:>12,}{N*p2:>30,.1f}{1-(1-p2)**N:>20.4f}")

# ---------- 3. la pregunta al reves: cuanto tiene que durar la racha ----------
print("\n" + "="*78)
print("LA PREGUNTA AL REVES: que racha es rara de verdad")
print("="*78)
print("Racha mas corta que NO se espera ver ni una vez por azar en N gestores")
print("(es decir, el numero esperado de gestores que la logran baja de 1)\n")
print(f"{'gestores':>12}{'10 anos':>12}{'15 anos':>12}{'20 anos':>12}")
for N in (100, 1_000, 5_000, 20_000, 100_000):
    fila = []
    for n in (10, 15, 20):
        k = next((kk for kk in range(1, n+1) if N*p_racha(n, kk, 0.5) < 1), n+1)
        fila.append(k)
    print(f"{N:>12,}" + "".join(f"{v:>12}" for v in fila))

# ---------- 4. y ahora los que cierran -----------------------------------------
print("\n" + "="*78)
print("EL SESGO QUE LO EMPEORA TODO: los que van mal cierran")
print("="*78)
print("Misma simulacion, cero habilidad, pero cada ano cierra el peor 15 %.")
print("Solo se puede leer la memoria de los que siguen abiertos.\n")

def con_cierres(N, anos, p, cierre, rng):
    vivo = np.ones(N, bool)
    acier = np.zeros((N, anos), np.int8)
    acum = np.zeros(N)
    for a in range(anos):
        r = rng.standard_normal(N)                 # rendimiento relativo al indice
        acier[:, a] = np.where(vivo, r > 0, -1)
        acum = np.where(vivo, acum + r, acum)
        if cierre > 0:
            v = np.where(vivo)[0]
            if len(v) > 10:
                corte = np.quantile(acum[v], cierre)
                vivo[v[acum[v] <= corte]] = False
    return acier, vivo

for cierre in (0.0, 0.15):
    acier, vivo = con_cierres(20_000, 10, 0.5, cierre, np.random.default_rng(7))
    sup = acier[vivo]
    tasa = (sup == 1).mean()
    run = np.zeros(len(sup), int); mx = np.zeros(len(sup), int)
    for j in range(sup.shape[1]):
        run = np.where(sup[:, j] == 1, run + 1, 0); mx = np.maximum(mx, run)
    etq = "sin cierres" if cierre == 0 else f"cierra el {cierre:.0%} peor cada ano"
    print(f"  {etq:<32} supervivientes {vivo.sum():>6,} de 20.000")
    print(f"  {'':<32} aciertos por ano en los vivos: {tasa:.1%}")
    print(f"  {'':<32} con >=7 seguidos: {(mx>=7).sum():>4}  "
          f"({100*(mx>=7).mean():.2f} % de los vivos)")
