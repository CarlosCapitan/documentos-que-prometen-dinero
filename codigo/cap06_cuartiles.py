#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cap06_cuartiles.py — cuantos fondos pueden decir con razon que son primer cuartil.

Por definicion, uno de cada cuatro. Ese es el punto de partida y el unico
numero que la palabra "cuartil" garantiza.

Pero un gestor no presenta UN numero: elige cual presenta. Puede elegir la
metrica (TIR, TVPI, DPI: miden cosas distintas y ordenan distinto), y puede
elegir la anada con la que se compara, porque "anada" admite al menos tres
definiciones legitimas -ano del primer cierre, del primer desembolso o del
cierre final- y las tres pueden caer en anos distintos.

Ninguna de esas elecciones es mentira. Cada una, por separado, es defendible.

DATOS REALES: las fronteras por anada son las de PitchBook Benchmarks, TIR neta
del capital riesgo global, a cierre de 2024. No estan inventadas.

SUPUESTOS, que hay que declarar porque no son datos:
  · correlacion entre metricas: 0,85 (miden lo mismo con distinto criterio)
  · ambiguedad de anada: mas menos un ano
"""
import numpy as np
from scipy.stats import norm

# --- HECHO: PitchBook Benchmarks, VC global, TIR neta por anada (Q4 2024) -----
#     percentiles 90, 75, 50, 25, 10
FRONTERAS = {
    2010: (41.35, 22.87, 12.84,  2.17, -5.10),
    2012: (43.19, 28.10, 17.50, 11.04,  1.49),
    2014: (32.75, 23.12, 15.55, 10.47,  5.05),
    2016: (35.46, 25.23, 16.23, 10.20,  4.90),
    2018: (32.16, 22.20, 12.67,  6.10,  3.24),
    2020: (25.21, 17.05, 10.21,  5.20,  0.28),
}
PCT = np.array([90, 75, 50, 25, 10]) / 100.0
ANADAS = sorted(FRONTERAS)

def cuantil(anada, p):
    """TIR en el percentil p de esa anada, interpolando entre los publicados."""
    v = np.array(FRONTERAS[anada])[::-1]      # de menor a mayor
    q = PCT[::-1]
    return np.interp(p, q, v)

def percentil(anada, tir):
    """En que percentil cae una TIR dentro de esa anada."""
    v = np.array(FRONTERAS[anada])[::-1]; q = PCT[::-1]
    return float(np.interp(tir, v, q, left=0.02, right=0.98))

print("="*80)
print("LAS FRONTERAS REALES  ·  PitchBook Benchmarks, TIR neta, VC global, Q4 2024")
print("="*80)
print(f"{'anada':>7}{'decil sup':>12}{'1er cuartil':>13}{'MEDIANA':>11}{'3er cuartil':>13}{'decil inf':>12}")
for a in ANADAS:
    d90, q1, me, q3, d10 = FRONTERAS[a]
    print(f"{a:>7}{d90:>11.2f}%{q1:>12.2f}%{me:>10.2f}%{q3:>12.2f}%{d10:>11.2f}%")
med = np.mean([FRONTERAS[a][2] for a in ANADAS])
q1m = np.mean([FRONTERAS[a][1] for a in ANADAS])
print(f"\n  «este tipo de fondos da un 20-25 %» describe la frontera del PRIMER CUARTIL")
print(f"  (media {q1m:.1f} %), no la experiencia tipica (mediana media {med:.1f} %).")
print(f"  En la anada 2010 el decil superior saco {41.35-(-5.10):.0f} puntos al inferior.")

# --- la simulacion: cuantos pueden decir que son primer cuartil ---------------
RHO   = 0.85          # SUPUESTO
NFOND = 200_000
rng = np.random.default_rng(20260909)

print("\n" + "="*80)
print("CUANTOS PUEDEN DECIR, CON RAZON, QUE SON PRIMER CUARTIL")
print("="*80)

def simula(anada, usar_metricas, usar_anadas, rng):
    """Devuelve la fraccion de fondos que alcanzan el primer cuartil en AL MENOS
    una presentacion legitima."""
    u = rng.random(NFOND)
    tir = np.array([cuantil(anada, p) for p in u])          # su TIR real
    vecinas = [a for a in ANADAS if abs(a-anada) <= 2] if usar_anadas else [anada]

    K = 3 if usar_metricas else 1
    z0 = norm.ppf(np.clip(u, 1e-6, 1-1e-6))
    mejor = np.zeros(NFOND)
    for k in range(K):
        if k == 0:
            zk = z0                                          # la TIR, tal cual
        else:                                                # otra metrica
            zk = RHO*z0 + np.sqrt(1-RHO**2)*rng.standard_normal(NFOND)
        uk = norm.cdf(zk)
        tk = np.array([cuantil(anada, p) for p in uk])
        for v in vecinas:
            pk = np.array([percentil(v, t) for t in tk])
            mejor = np.maximum(mejor, pk)
    return (mejor >= 0.75).mean(), tir

print(f"{'presentaciones permitidas':<46}{'pueden decirlo':>16}")
print("-"*80)
for etq, met, ana in (("solo su TIR, solo su anada  (lo honesto)", False, False),
                      ("+ elegir entre 3 metricas", True, False),
                      ("+ elegir la anada (mas menos un ano)", False, True),
                      ("+ las dos cosas: 3 metricas x 3 anadas", True, True)):
    fr = np.mean([simula(a, met, ana, np.random.default_rng(1000+a))[0]
                  for a in (2014, 2016, 2018)])
    print(f"{etq:<46}{fr:>15.1%}")

print("\n  Ninguna de esas elecciones es mentira. Cada una, por separado, es")
print("  defendible. Nueve combinaciones defendibles convierten «uno de cada")
print("  cuatro» en algo muy distinto.")
print("\n  Y sale parecido a lo que midio quien tenia los datos de verdad:")
print("    Harris y Stucke (2012), academicos:  «la MITAD de todos los fondos»")
print("    Gottschalg / PERACS, 550 fondos:      66 % cambiando de base de datos,")
print("                                          77 % anadiendo la anada")
print("    (PERACS vende servicios de benchmarking: tiene interes en el resultado)")

# --- la mediana no es la media, y el gestor no repite -------------------------
print("\n" + "="*80)
print("DOS COSAS MAS QUE HAY QUE PREGUNTARLE A LA CIFRA")
print("="*80)
print("1. ¿Es media o mediana?  Kaplan y Schoar (2005), 746 fondos:")
print("     PME media 0,96  frente a  PME mediana 0,74.")
print("   La media la levantan unos pocos fondos enormes. La mediana es")
print("   la experiencia del fondo del medio, que es la que te va a tocar.")
print("\n2. ¿El cuartil anterior predice el siguiente?")
print("     Harris, Jenkinson, Kaplan y Stucke (2023), datos Burgiss:")
print("     con la informacion DISPONIBLE AL CAPTAR el fondo siguiente, en")
print("     buyout post-2000 la persistencia DESAPARECE: el resultado es")
print("     estadisticamente indistinguible sea cual sea el cuartil previo,")
print("     y los gestores primerizos rinden igual que cualquier cuartil.")
print("     En venture capital si sobrevive algo: PME 1,70 en el cuartil")
print("     superior frente a 0,91 en el inferior.")
