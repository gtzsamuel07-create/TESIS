import unittest

from calculadora_nom import calcular_circuito


class CalcularCircuitoTest(unittest.TestCase):
    def test_calcula_circuito_monofasico_basico(self) -> None:
        resultado = calcular_circuito(carga_w=1800, tension_v=127)

        self.assertEqual(resultado.interruptor_recomendado_a, 15)
        self.assertEqual(resultado.conductor_recomendado, "14 AWG")
        self.assertEqual(resultado.ampacidad_conductor_a, 15)
        self.assertAlmostEqual(resultado.corriente_calculada_a, 14.17, places=2)
        self.assertAlmostEqual(resultado.corriente_diseno_a, 14.17, places=2)

    def test_calcula_circuito_continuo_incrementa_capacidad(self) -> None:
        resultado = calcular_circuito(carga_w=1800, tension_v=127, carga_continua=True)

        self.assertEqual(resultado.interruptor_recomendado_a, 20)
        self.assertEqual(resultado.conductor_recomendado, "12 AWG")
        self.assertAlmostEqual(resultado.corriente_diseno_a, 17.72, places=2)

    def test_calcula_circuito_trifasico(self) -> None:
        resultado = calcular_circuito(carga_w=12000, tension_v=220, fases=3, carga_continua=True)

        self.assertEqual(resultado.interruptor_recomendado_a, 40)
        self.assertEqual(resultado.conductor_recomendado, "8 AWG")
        self.assertAlmostEqual(resultado.corriente_calculada_a, 31.49, places=2)

    def test_valida_parametros(self) -> None:
        with self.assertRaises(ValueError):
            calcular_circuito(carga_w=0, tension_v=127)

        with self.assertRaises(ValueError):
            calcular_circuito(carga_w=1000, tension_v=127, factor_potencia=0)


if __name__ == "__main__":
    unittest.main()
