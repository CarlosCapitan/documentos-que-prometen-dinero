# Documentos que prometen dinero
### Las cinco preguntas que nadie le hace al número que sale bien

Repositorio de código del libro. **Todas las cifras y todas las figuras del
texto salen de ejecutar esto.** Un libro que enseña a desconfiar de los números
no puede pedir que te fíes de los suyos.

> **Aviso.** Este repositorio es material divulgativo. No es asesoramiento en
> materia de inversión ni de criptoactivos, ni una recomendación, ni una oferta
> de ningún producto, fondo, servicio o juego. Las simulaciones son
> simulaciones: ninguna de sus reglas es una estrategia para usar.

```
codigo/    un guion por capítulo, más rutas.py (todas las rutas, en un sitio)
datos/     datos fijos del capítulo 9 (ver datos/LEAME.md)
figuras/   generadas por el código, nunca a mano
```

## Empezar

```bash
git clone https://github.com/CarlosCapitan/documentos-que-prometen-dinero
cd documentos-que-prometen-dinero
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Reproducir todo

Menos de dos minutos en un portátil normal.

```bash
python codigo/figura_01.py          # cap. 1 · veinte columnas de azar
python codigo/cap02_tiendas.py      # cap. 2 · un plan de mejora que no hace nada
python codigo/cap05_montecarlo.py   # cap. 5 · cartera independiente frente a ciclo común
python codigo/figura_05.py          #          (necesita el paso anterior)
python codigo/cap06_cuartiles.py    # cap. 6 · cuántos fondos pueden llamarse «primer cuartil»
python codigo/figura_06.py
python codigo/cap07_rachas.py       # cap. 7 · rachas y supervivientes, con cero talento
python codigo/cap08_backtest.py     # cap. 8 · 207 reglas sobre precios sorteados
python codigo/figuras_78.py         #          (necesita el paso anterior)
python codigo/cap09_figura.py       # cap. 9 · la ventaja que no es tuya
```

Las simulaciones usan semillas fijas: los números salen idénticos en cada
ejecución. Si en tu máquina sale otra cosa, es un error, y me interesa saberlo.

## De dónde sale cada dato

| capítulo | datos |
|---|---|
| 1, 2, 5, 7, 8 | ninguno: simulaciones donde la respuesta la ponemos nosotros |
| 6 | fronteras de rentabilidad publicadas por PitchBook (Benchmarks Q4 2024, capital riesgo global), transcritas en el guion con su fuente |
| 9 | dos tablas pequeñas de resultados ya medidos, incluidas en `datos/` |

Los datos del capítulo 9 proceden de un mercado de predicción extranjero que no
tiene autorización para operar en España. Se incluyen solo para reproducir las
cifras del libro. Este repositorio no contiene enlaces, instrucciones ni
herramientas para acceder a esa plataforma.

## Licencia

La licencia MIT (`LICENSE`, texto estándar en inglés) cubre el código de
`codigo/`, las figuras que genera y las tablas de resultados de `datos/`.

No cubre el texto del libro «Documentos que prometen dinero», que no está en
este repositorio y cuyos derechos se reserva el autor.

Las fronteras de rentabilidad del capítulo 6 son cifras publicadas por PitchBook
(Benchmarks Q4 2024): se citan con su fuente y se rigen por las condiciones de
su editor.
