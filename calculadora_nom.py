from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


INTERRUPTORES_ESTANDAR_A = (15, 20, 30, 40, 50, 60, 70, 80, 90, 100)
CONDUCTORES_COBRE_A_75C = (
    ("14 AWG", 15),
    ("12 AWG", 20),
    ("10 AWG", 30),
    ("8 AWG", 50),
    ("6 AWG", 65),
    ("4 AWG", 85),
    ("3 AWG", 100),
)
REFERENCIAS_NORMATIVAS = (
    "NOM-001-SEDE-2012 arts. 210, 215, 220, 240 y 310",
)


@dataclass(frozen=True)
class ResultadoCalculo:
    carga_w: float
    tension_v: float
    fases: int
    factor_potencia: float
    carga_continua: bool
    corriente_calculada_a: float
    corriente_diseno_a: float
    interruptor_recomendado_a: int
    conductor_recomendado: str
    ampacidad_conductor_a: int
    referencias: tuple[str, ...]


def _validar_entrada(carga_w: float, tension_v: float, fases: int, factor_potencia: float) -> None:
    if carga_w <= 0:
        raise ValueError("La carga debe ser mayor que cero.")
    if tension_v <= 0:
        raise ValueError("La tensión debe ser mayor que cero.")
    if fases not in (1, 3):
        raise ValueError("Solo se admiten sistemas monofásicos o trifásicos.")
    if not 0 < factor_potencia <= 1:
        raise ValueError("El factor de potencia debe estar entre 0 y 1.")


def _corriente_carga(carga_w: float, tension_v: float, fases: int, factor_potencia: float) -> float:
    if fases == 1:
        return carga_w / (tension_v * factor_potencia)
    return carga_w / (math.sqrt(3) * tension_v * factor_potencia)


def _seleccionar_interruptor(corriente_diseno_a: float) -> int:
    for interruptor in INTERRUPTORES_ESTANDAR_A:
        if interruptor >= corriente_diseno_a:
            return interruptor
    raise ValueError("La corriente calculada excede el alcance de esta versión base del programa.")


def _seleccionar_conductor(interruptor_a: int) -> tuple[str, int]:
    for conductor, ampacidad in CONDUCTORES_COBRE_A_75C:
        if ampacidad >= interruptor_a:
            return conductor, ampacidad
    raise ValueError("No se encontró un conductor válido en la tabla base.")


def calcular_circuito(
    carga_w: float,
    tension_v: float,
    fases: int = 1,
    factor_potencia: float = 1.0,
    carga_continua: bool = False,
) -> ResultadoCalculo:
    _validar_entrada(carga_w, tension_v, fases, factor_potencia)
    corriente_calculada = _corriente_carga(carga_w, tension_v, fases, factor_potencia)
    corriente_diseno = corriente_calculada * (1.25 if carga_continua else 1.0)
    interruptor = _seleccionar_interruptor(corriente_diseno)
    conductor, ampacidad = _seleccionar_conductor(interruptor)
    return ResultadoCalculo(
        carga_w=carga_w,
        tension_v=tension_v,
        fases=fases,
        factor_potencia=factor_potencia,
        carga_continua=carga_continua,
        corriente_calculada_a=round(corriente_calculada, 2),
        corriente_diseno_a=round(corriente_diseno, 2),
        interruptor_recomendado_a=interruptor,
        conductor_recomendado=conductor,
        ampacidad_conductor_a=ampacidad,
        referencias=REFERENCIAS_NORMATIVAS,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cálculo base de circuitos derivados conforme a NOM-001-SEDE-2012."
    )
    parser.add_argument("--carga-w", type=float, required=True, help="Carga total en watts.")
    parser.add_argument("--tension-v", type=float, required=True, help="Tensión del sistema en volts.")
    parser.add_argument("--fases", type=int, choices=(1, 3), default=1, help="Número de fases del sistema.")
    parser.add_argument(
        "--factor-potencia",
        type=float,
        default=1.0,
        help="Factor de potencia de la carga, entre 0 y 1.",
    )
    parser.add_argument(
        "--continua",
        action="store_true",
        help="Aplica el factor de 125%% para cargas continuas.",
    )
    args = parser.parse_args()
    resultado = calcular_circuito(
        carga_w=args.carga_w,
        tension_v=args.tension_v,
        fases=args.fases,
        factor_potencia=args.factor_potencia,
        carga_continua=args.continua,
    )
    print(json.dumps(asdict(resultado), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
