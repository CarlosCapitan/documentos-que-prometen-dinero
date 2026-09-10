#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
montecarlo.py — el argumento del apendice del paper de 2018, y su nula.

El paper sostiene (citando simulaciones de Monte Carlo) que invertir en muchas
companias "pone la ley de los grandes numeros de tu parte" y que una cartera de
100+ maximiza la probabilidad de un 3,8x.

Ese argumento supone extracciones INDEPENDIENTES de una distribucion FIJA.
Este guion mide que le pasa cuando se anade lo unico que de verdad hay en el
mundo real: un factor comun de ciclo, compartido por toda la cartera.

La distribucion marginal es la MISMA en los dos casos (misma media). Lo unico
que cambia es la independencia.
"""
import os
import numpy as np

RES = {}   # resultados para figura_05.py: (objetivo o "sd", sigma) -> lista por tamano de cartera

RNG = np.random.default_rng(20260909)
NPORT = 60_000                       # carteras simuladas por celda
CARTERAS = (5, 10, 25, 50, 100, 200, 500, 1000)

# --- distribucion de resultados de una startup -------------------------------
# Calibrada con las tasas de perdida que el PROPIO paper cita:
#   "64% of financings return <1x"  /  "around 65% return less than the outlay"
# Tramos: 35 % perdida total, 30 % entre 0x y 1x, y el resto reparte la cola.
# El peso de la cola se ajusta para que la MEDIA sea 3,8x, que es exactamente
# el objetivo que el paper persigue. Es la lectura mas generosa posible.
P_CERO, P_PARCIAL, P_MEDIO, P_ALTO = 0.35, 0.30, 0.25, 0.075
P_COLA = 1 - (P_CERO + P_PARCIAL + P_MEDIO + P_ALTO)     # 0.025

def media_con_cola(tope):
    return (P_PARCIAL*0.5 + P_MEDIO*3.0 + P_ALTO*12.5 + P_COLA*(20+tope)/2)

lo, hi = 20.0, 1000.0
for _ in range(200):                                  # ajusta el tope de la cola
    mid = (lo+hi)/2
    if media_con_cola(mid) < 3.8: lo = mid
    else: hi = mid
TOPE = (lo+hi)/2
MEDIA = media_con_cola(TOPE)

def sortea_base(n, rng):
    u = rng.random(n); x = np.empty(n)
    a, b, c, d = P_CERO, P_CERO+P_PARCIAL, P_CERO+P_PARCIAL+P_MEDIO, P_CERO+P_PARCIAL+P_MEDIO+P_ALTO
    m = u < a;                     x[m] = 0.0
    m = (u >= a) & (u < b);        x[m] = rng.uniform(0, 1, m.sum())
    m = (u >= b) & (u < c);        x[m] = rng.uniform(1, 5, m.sum())
    m = (u >= c) & (u < d);        x[m] = rng.uniform(5, 20, m.sum())
    m = u >= d;                    x[m] = rng.uniform(20, TOPE, m.sum())
    return x

def carteras(n_emp, n_port, sigma_c, rng):
    """Multiplo medio de n_port carteras de n_emp companias.
    sigma_c = 0  -> extracciones independientes (el supuesto del paper)
    sigma_c > 0  -> factor de ciclo comun a toda la cartera, con E[C] = 1"""
    base = sortea_base(n_emp*n_port, rng).reshape(n_port, n_emp)
    if sigma_c > 0:
        C = rng.lognormal(-0.5*sigma_c**2, sigma_c, size=(n_port, 1))
        base = base * C
    return base.mean(axis=1)

print("="*78)
print("EL ARGUMENTO DEL APENDICE, Y SU NULA")
print("="*78)
print(f"distribucion de una startup: 35 % a cero, 30 % entre 0x y 1x (65 % < 1x,")
print(f"como cita el paper), cola hasta {TOPE:.0f}x.  media = {MEDIA:.3f}x")
print(f"carteras simuladas por celda: {NPORT:,}\n")

SIGMAS = [(0.0, "independiente (el supuesto)"),
          (0.30, "ciclo suave    (sigma=0,30)"),
          (0.50, "ciclo moderado (sigma=0,50)"),
          (0.80, "ciclo fuerte   (sigma=0,80)")]

for objetivo, etq in ((1.0, "P(recuperar lo invertido, >= 1x)"),
                      (3.8, "P(alcanzar el objetivo, >= 3,8x)")):
    print("-"*78)
    print(etq)
    print("-"*78)
    print(f"{'companias':>10}" + "".join(f"{e.split('(')[0].strip():>18}" for _, e in SIGMAS))
    for n in CARTERAS:
        fila = []
        for s, _ in SIGMAS:
            r = carteras(n, NPORT, s, np.random.default_rng(20260909+n))
            fila.append((r >= objetivo).mean())
        for (s, _), v in zip(SIGMAS, fila):
            RES.setdefault((objetivo, s), []).append(v)
        print(f"{n:>10}" + "".join(f"{v*100:17.1f}%" for v in fila))
    print()

print("-"*78)
print("DESVIACION TIPICA DEL MULTIPLO DE LA CARTERA (el riesgo que no se va)")
print("-"*78)
print(f"{'companias':>10}" + "".join(f"{e.split('(')[0].strip():>18}" for _, e in SIGMAS))
for n in CARTERAS:
    fila = []
    for s, _ in SIGMAS:
        r = carteras(n, NPORT, s, np.random.default_rng(20260909+n))
        fila.append(r.std())
    for (s, _), v in zip(SIGMAS, fila):
        RES.setdefault(("sd", s), []).append(v)
    print(f"{n:>10}" + "".join(f"{v:17.3f} " for v in fila))

print("\n" + "="*78)
print("CORRELACION ENTRE DOS COMPANIAS CUALESQUIERA DE LA MISMA CARTERA")
print("="*78)
for s, etq in SIGMAS:
    if s == 0: print(f"  {etq:<30} rho = 0 por construccion"); continue
    a = sortea_base(400_000, np.random.default_rng(1))
    b = sortea_base(400_000, np.random.default_rng(2))
    C = np.random.default_rng(3).lognormal(-0.5*s**2, s, 400_000)
    print(f"  {etq:<30} rho = {np.corrcoef(a*C, b*C)[0,1]:.3f}")

print("\n" + "="*78)
print("ANCLAJE EMPIRICO: cuanto vale sigma en el mundo real")
print("="*78)
# TVPI neto del VC europeo, anadas adyacentes, misma fecha de corte (31-12-2024,
# PitchBook Benchmarks). Tres anadas seguidas de la misma clase de activo.
TVPI = {2018: 1.70, 2019: 1.18, 2020: 1.23}
v = np.log(list(TVPI.values()))
print("  TVPI neto VC Europa: " + ", ".join(f"{a}: {t:.2f}x" for a, t in TVPI.items()))
print(f"  desviacion tipica del logaritmo entre esas tres anadas: {v.std(ddof=1):.3f}")
print("  Y eso son valoraciones provisionales a una misma fecha, no resultados")
print("  realizados: subestima la dispersion verdadera. sigma = 0,30 es")
print("  conservador; 0,50 es razonable para un ciclo completo.")

print("\n" + "="*78)
print("EL SUELO: la probabilidad de perder con INFINITAS companias")
print("="*78)
# Con infinitas companias la media de la cartera converge a MEDIA * C, porque el
# azar propio de cada compania se promedia y el factor de ciclo C no. Asi que
# P(perder) -> P(MEDIA * C < 1) = P(C < 1/MEDIA), con C lognormal(-s^2/2, s).
# Es un calculo exacto, no una simulacion. (Anadido el 10-sep-2026: el texto
# decia que 1.000 companias no mejoraban a 100; mejoran, pero muy cerca del suelo.)
from math import erf, log, sqrt
Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
for s, etq in SIGMAS:
    if s == 0: print(f"  {etq:<30} suelo = 0 (la ley de los grandes numeros funciona)"); continue
    suelo = Phi((log(1 / MEDIA) + 0.5 * s**2) / s)
    print(f"  {etq:<30} suelo = {suelo*100:.3f} %")

# --- guarda los resultados para la figura (figura_05.py los lee) --------------
SAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cap05_datos.npz")
np.savez(SAL, N=np.array(CARTERAS), sigmas=np.array([s for s, _ in SIGMAS]),
         p_recuperar=np.array([RES[(1.0, s)] for s, _ in SIGMAS]),
         sd=np.array([RES[("sd", s)] for s, _ in SIGMAS]),
         suelo_08=Phi((log(1 / MEDIA) + 0.5 * 0.8**2) / 0.8))
print(f"\n  guardado {os.path.basename(SAL)}")
