#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cap01_correlaciones.py — el ejemplo minimo del capitulo 1.

Veinticuatro meses de ventas. Veinte cosas que se te ocurre que podrian
explicarlas. Ninguna de las veintiuna series tiene NADA que ver con las otras:
todas se sortean por separado. No hay causa, no hay efecto, no hay nada.

La pregunta es cuanto de bien sale la mejor de las veinte, y con que frecuencia
sale lo bastante bien como para que alguien construya una historia encima.

Se puede reproducir en una hoja de calculo con =ALEATORIO() y =COEF.DE.CORREL().
"""
import numpy as np

REPS = 200_000
rng = np.random.default_rng(20260909)

def experimento(n_meses, n_variables, rng):
    y = rng.standard_normal((REPS, n_meses))
    y = (y - y.mean(1, keepdims=True)) / y.std(1, keepdims=True)
    mejor = np.zeros(REPS); alguna = np.zeros(REPS, bool)
    # umbral de r para p<0,05 a dos colas con n-2 grados de libertad
    from scipy import stats
    t = stats.t.ppf(0.975, n_meses-2)
    r_umbral = t / np.sqrt(t**2 + n_meses - 2)
    for _ in range(n_variables):
        x = rng.standard_normal((REPS, n_meses))
        x = (x - x.mean(1, keepdims=True)) / x.std(1, keepdims=True)
        r = np.abs((x*y).mean(1))
        mejor = np.maximum(mejor, r)
        alguna |= r > r_umbral
    return mejor, alguna, r_umbral

print("="*76)
print("VEINTICUATRO MESES DE VENTAS Y VARIAS COSAS QUE «PODRIAN EXPLICARLAS»")
print("="*76)
print("Todas las series se sortean por separado. No hay ninguna relacion real.\n")
print(f"{'variables':>11}{'mejor r tipica':>17}{'mejor r, 1 de cada 20':>24}"
      f"{'alguna «significativa»':>25}")
for k in (1, 5, 10, 20, 50, 100):
    mejor, alguna, ru = experimento(24, k, np.random.default_rng(100+k))
    print(f"{k:>11}{np.median(mejor):>17.2f}{np.percentile(mejor,95):>24.2f}"
          f"{alguna.mean():>24.0%}")
print(f"\n  (el umbral de «significativo» para 24 meses es r = {ru:.2f})")

print("\n" + "="*76)
print("Y AL ANO SIGUIENTE: la ganadora, sobre doce meses nuevos")
print("="*76)
N1, N2, K = 24, 12, 20
y1 = rng.standard_normal((REPS, N1)); y2 = rng.standard_normal((REPS, N2))
X1 = rng.standard_normal((REPS, K, N1)); X2 = rng.standard_normal((REPS, K, N2))
def z(a, ax): return (a - a.mean(ax, keepdims=True))/a.std(ax, keepdims=True)
y1, y2, X1, X2 = z(y1,1), z(y2,1), z(X1,2), z(X2,2)
r1 = (X1 * y1[:,None,:]).mean(2)
j = np.abs(r1).argmax(1)
i = np.arange(REPS)
r1g = r1[i, j]
r2g = (X2[i, j] * y2).mean(1)
print(f"  correlacion de la ganadora, el primer ano : {np.median(np.abs(r1g)):.2f} (mediana)")
print(f"  la misma variable, el ano siguiente       : {np.median(np.abs(r2g)):.2f} (mediana)")
print(f"  ¿conserva el signo?                        {np.mean(np.sign(r1g)==np.sign(r2g)):.0%} de las veces")
print(f"  correlacion entre lo de un ano y lo del otro: {np.corrcoef(r1g, r2g)[0,1]:+.3f}")
