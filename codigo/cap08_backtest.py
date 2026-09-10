#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cap08_backtest.py — como fabricar una estrategia ganadora sobre ruido puro.

Los precios de este guion NO CONTIENEN NADA. Se generan sorteando rendimientos
independientes de media cero. Por construccion no hay tendencia, no hay memoria
y no hay nada que predecir. Cualquier estrategia que parezca funcionar aqui
esta funcionando sobre ruido, y lo sabemos porque el ruido lo pusimos nosotros.

Se prueban unos cientos de reglas de las de siempre -cruces de medias moviles y
roturas de rango-, se elige la mejor dentro de muestra y se mira que hace
despues. Es exactamente el procedimiento con el que se construye la mayoria de
los backtests que se ensenan.
"""
import os
import numpy as np

DIAS_ANO = 252
N_DIAS   = 3000                 # ~12 anos
CORTE    = 2000                 # dentro de muestra / fuera de muestra
VOL      = 0.01

def media_movil(x, k):
    c = np.concatenate([[0.0], np.cumsum(x)])
    m = np.full(len(x), np.nan)
    m[k-1:] = (c[k:] - c[:-k]) / k
    return m

def señales(precio):
    """Familia de reglas. Devuelve (nombres, matriz posiciones dias x reglas)."""
    nom, pos = [], []
    rapidas = (2, 3, 5, 8, 10, 15, 20, 25, 30, 40, 50)
    lentas  = (20, 30, 40, 60, 80, 100, 120, 150, 200, 250)
    for f in rapidas:
        mf = media_movil(precio, f)
        for l in lentas:
            if l <= f: continue
            ml = media_movil(precio, l)
            arriba = mf > ml
            for modo in ("largo/fuera", "largo/corto"):
                p = arriba.astype(float) if modo == "largo/fuera" else np.where(arriba, 1.0, -1.0)
                p[np.isnan(mf) | np.isnan(ml)] = 0.0
                nom.append(f"cruce {f}/{l} {modo}"); pos.append(p)
    for k in (10, 20, 40, 60, 100, 150, 200):        # rotura de rango
        mx = np.full(len(precio), np.nan); mn = np.full(len(precio), np.nan)
        for i in range(k, len(precio)):
            mx[i] = precio[i-k:i].max(); mn[i] = precio[i-k:i].min()
        s = np.zeros(len(precio)); act = 0.0
        for i in range(len(precio)):
            if precio[i] > (mx[i] if mx[i] == mx[i] else np.inf): act = 1.0
            elif precio[i] < (mn[i] if mn[i] == mn[i] else -np.inf): act = -1.0
            s[i] = act
        nom.append(f"rotura {k}"); pos.append(s)
    return nom, np.array(pos).T          # dias x reglas

def sharpe(r):
    s = r.std()
    return 0.0 if s == 0 else float(r.mean() / s * np.sqrt(DIAS_ANO))

def una_pasada(rng):
    ret = rng.standard_normal(N_DIAS) * VOL      # <- aqui no hay nada, por construccion
    precio = 100 * np.exp(np.cumsum(ret))
    nom, P = señales(precio)
    P = np.vstack([np.zeros((1, P.shape[1])), P[:-1]])[:N_DIAS]   # sin mirar el futuro
    R = P * ret[:, None]
    sh_in  = np.array([sharpe(R[:CORTE, j]) for j in range(R.shape[1])])
    j = int(np.nanargmax(sh_in))
    sh_out = sharpe(R[CORTE:, j])
    return nom, sh_in, j, sh_out, R[:, j], ret

rng = np.random.default_rng(20260909)
nom, sh_in, j, sh_out, r_gan, ret = una_pasada(rng)
N = len(nom)

print("="*78)
print("UNA PASADA: la mejor estrategia sobre una serie que no contiene nada")
print("="*78)
print(f"  dias simulados        : {N_DIAS:,}  ({N_DIAS/DIAS_ANO:.1f} anos)")
print(f"  reglas probadas       : {N}")
print(f"  dentro de muestra     : dias 1 a {CORTE:,}")
print(f"  fuera de muestra      : dias {CORTE+1:,} a {N_DIAS:,}")
print(f"\n  LA GANADORA: {nom[j]}")
eq = np.cumprod(1 + r_gan[:CORTE])
pico = np.maximum.accumulate(eq)
print(f"    Sharpe dentro de muestra   : {sh_in[j]:+.2f}")
print(f"    rentabilidad anualizada    : {(eq[-1]**(DIAS_ANO/CORTE)-1):+.1%}")
print(f"    dias ganadores             : {(r_gan[:CORTE] > 0).mean():.1%}")
print(f"    peor caida desde maximo    : {(eq/pico-1).min():.1%}")
print(f"    multiplico el capital por  : {eq[-1]:.2f}x")
print(f"\n    Sharpe FUERA de muestra    : {sh_out:+.2f}")

# ---------- la distribucion, no la anecdota ------------------------------------
print("\n" + "="*78)
print("300 SERIES INDEPENDIENTES, TODAS SIN NADA DENTRO")
print("="*78)
IN, OUT = [], []
for i in range(300):
    _, s_in, jj, s_out, _, _ = una_pasada(np.random.default_rng(1000+i))
    IN.append(s_in[jj]); OUT.append(s_out)
IN, OUT = np.array(IN), np.array(OUT)
print(f"  {'':<28}{'mediana':>10}{'p5':>10}{'p95':>10}")
print(f"  {'Sharpe de la ganadora':<28}{np.median(IN):>10.2f}{np.percentile(IN,5):>10.2f}{np.percentile(IN,95):>10.2f}")
print(f"  {'ese mismo, fuera de muestra':<28}{np.median(OUT):>10.2f}{np.percentile(OUT,5):>10.2f}{np.percentile(OUT,95):>10.2f}")
print(f"\n  la ganadora tiene Sharpe > 0,5 dentro de muestra en {(IN>0.5).mean():.0%} de las series")
print(f"  y sigue por encima de 0,5 fuera de muestra en           {(OUT>0.5).mean():.0%}")
print(f"  correlacion entre el Sharpe de dentro y el de fuera: {np.corrcoef(IN,OUT)[0,1]:+.3f}")

# ---------- cuantas hipotesis hay de verdad ------------------------------------
print("\n" + "="*78)
print("CUANTAS HIPOTESIS HAY DE VERDAD (y no son las que se cuentan)")
print("="*78)
T = CORTE / DIAS_ANO
sd = 1/np.sqrt(T)
print(f"  anos dentro de muestra: {T:.2f}   ->  desviacion tipica del Sharpe estimado: {sd:.3f}")
# Maximo de N normales independientes: se calcula EXACTO, no con sqrt(2 ln N).
# sqrt(2 ln N) es solo la asintota; para N pequeno exagera mucho (con N = 4 da
# 1,67 cuando el maximo esperado real es 1,03), y despejar N de ella da un
# numero de hipotesis efectivas unas tres veces menor que el verdadero.
# Corregido el 10-sep-2026: la version anterior daba "4" en vez de ~14.
from scipy.stats import norm
from scipy.integrate import quad
from scipy.optimize import brentq
def max_esperado(n):
    return quad(lambda x: x * n * norm.pdf(x) * norm.cdf(x)**(n - 1), -12, 12)[0]
def max_mediano(n):
    return norm.ppf(0.5 ** (1 / n))
print(f"  si las {N} reglas fueran independientes, el maximo de su Sharpe seria")
print(f"    esperado: {max_esperado(N):.3f} x {sd:.3f} = {max_esperado(N)*sd:.2f}")
print(f"    mediano:  {max_mediano(N):.3f} x {sd:.3f} = {max_mediano(N)*sd:.2f}")
print(f"    (la asintota sqrt(2 ln {N}) daria {np.sqrt(2*np.log(N))*sd:.2f}: sobreestima)")
med = np.median(IN)
print(f"  el maximo mediano observado es         {med:.2f}")
t = med / sd
n_ef = np.log(0.5) / np.log(norm.cdf(t))        # invierte exactamente max_mediano
print(f"  -> hipotesis EFECTIVAS: {n_ef:,.1f}, no {N}")
n_ef_esp = brentq(lambda n: max_esperado(n) - t, 1.01, 1e4)
print(f"     (con el maximo esperado en vez del mediano saldrian {n_ef_esp:,.1f})")
print(f"     las reglas se solapan: un cruce 10/100 y uno 10/120 son casi la misma.")
np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cap08_datos.npz"),
         IN=IN, OUT=OUT, r_gan=r_gan, ret=ret,
         nombre=np.array([nom[j]]), sh_in=np.array([sh_in[j]]), sh_out=np.array([sh_out]))
print("\n  guardado cap08_datos.npz")
