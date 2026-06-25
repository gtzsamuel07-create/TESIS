# TESIS
IMPLEMENTACIÓN COMPUTACIONAL PARA EL DISEÑO Y CÁLCULO DE INSTALACIONES ELÉCTRICAS BASADO EN LA NORMA OFICIAL MEXICANA NOM-001-SEDE-2012, INSTALACIONES ELÉCTRICAS (UTILIZACIÓN)

## Programa base de cálculo

Este repositorio ahora incluye un programa base en Python para calcular circuitos derivados con estos criterios iniciales alineados a la NOM-001-SEDE-2012:

- cálculo de corriente para sistemas monofásicos y trifásicos;
- aplicación del 125% para cargas continuas;
- recomendación de interruptor en capacidades estándar;
- selección de conductor de cobre con una tabla base de ampacidades a 75 °C.

### Uso

```bash
python calculadora_nom.py --carga-w 1800 --tension-v 127 --continua
```

Ejemplo de salida:

```json
{
  "carga_w": 1800.0,
  "tension_v": 127.0,
  "fases": 1,
  "factor_potencia": 1.0,
  "carga_continua": true,
  "corriente_calculada_a": 14.17,
  "corriente_diseno_a": 17.72,
  "interruptor_recomendado_a": 20,
  "conductor_recomendado": "12 AWG",
  "ampacidad_conductor_a": 20,
  "referencias": [
    "NOM-001-SEDE-2012 arts. 210, 215, 220, 240 y 310"
  ]
}
```

### Pruebas

```bash
python -m unittest discover -s tests -v
```
