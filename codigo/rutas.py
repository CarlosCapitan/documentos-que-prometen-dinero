#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rutas.py — todas las rutas del repositorio, en un solo sitio.

Nada de rutas absolutas en los guiones: se calculan desde la posicion de este
fichero, asi que el repositorio funciona clonado donde sea.

Los datos que el libro no genera por si mismo (los del capitulo 9) van ya
incluidos en datos/, como copia fija de lo medido. El repositorio no contiene
enlaces ni herramientas para descargarlos de su origen.
"""
import os

RAIZ    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGURAS = os.path.join(RAIZ, "figuras")
DATOS   = os.path.join(RAIZ, "datos")
os.makedirs(FIGURAS, exist_ok=True)

def figura(nombre):
    """Ruta de salida de una figura."""
    return os.path.join(FIGURAS, nombre)

def datos(nombre):
    """Ruta de un fichero de datos incluido en el repositorio."""
    ruta = os.path.join(DATOS, nombre)
    if not os.path.exists(ruta):
        raise SystemExit(f"No encuentro {nombre} en {DATOS}. Deberia venir con el repositorio.")
    return ruta
