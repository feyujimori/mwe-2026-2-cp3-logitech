from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from garantia.credito import (
    CalculadoraCredito,
    RegraCliente,
    calcular_atraso,
)


def h(horas, minutos=0):
    return timedelta(hours=horas, minutes=minutos)


@pytest.fixture
def calc():
    return CalculadoraCredito()


# ---------- RF02: Varejo ----------

def test_ct01_varejo_atraso_abaixo_da_tolerancia_nao_gera_credito(calc):
    assert calc.calcular("VAREJO", h(1, 59), Decimal("300.00")).credito == Decimal("0.00")


def test_ct02_varejo_atraso_exatamente_2h_nao_gera_credito(calc):
    assert calc.calcular("VAREJO", h(2), Decimal("300.00")).credito == Decimal("0.00")


def test_ct03_varejo_atraso_2h01_gera_10_por_cento(calc):
    assert calc.calcular("VAREJO", h(2, 1), Decimal("300.00")).credito == Decimal("30.00")


def test_ct04_varejo_limite_24h(calc):
    assert calc.calcular("VAREJO", h(24), Decimal("300.00")).credito == Decimal("30.00")
    assert calc.calcular("VAREJO", h(24, 1), Decimal("300.00")).credito == Decimal("75.00")


def test_ct05_varejo_limite_72h(calc):
    assert calc.calcular("VAREJO", h(72), Decimal("300.00")).credito == Decimal("75.00")
    assert calc.calcular("VAREJO", h(72, 1), Decimal("300.00")).credito == Decimal("150.00")


def test_ct06_varejo_credito_limitado_ao_teto_de_500(calc):
    assert calc.calcular("VAREJO", h(80), Decimal("1200.00")).credito == Decimal("500.00")


# ---------- RF03: Corporativo e Cortesia ----------

def test_ct07_corporativo_percentuais_dobrados(calc):
    assert calc.calcular("CORPORATIVO", h(2, 1), Decimal("300.00")).credito == Decimal("60.00")
    assert calc.calcular("CORPORATIVO", h(24, 1), Decimal("300.00")).credito == Decimal("150.00")
    assert calc.calcular("CORPORATIVO", h(72, 1), Decimal("300.00")).credito == Decimal("300.00")


def test_ct08_corporativo_credito_limitado_ao_teto_de_2000(calc):
    assert calc.calcular("CORPORATIVO", h(80), Decimal("5000.00")).credito == Decimal("2000.00")


def test_ct09_cortesia_nao_recebe_credito_mas_e_notificado(calc):
    resultado = calc.calcular("CORTESIA", h(80), Decimal("0.00"))
    assert resultado.credito == Decimal("0.00")
    assert resultado.notificar_atraso is True


# ---------- RF04: novo tipo sem alterar os existentes ----------

class RegraPremiumStub(RegraCliente):
    def calcular(self, atraso, valor_frete):
        return Decimal("999.00")


def test_ct10_novo_tipo_registrado_sem_alterar_regras_existentes(calc):
    calc.registrar("PREMIUM", RegraPremiumStub())
    assert calc.calcular("PREMIUM", h(2, 1), Decimal("300.00")).credito == Decimal("999.00")
    assert calc.calcular("VAREJO", h(2, 1), Decimal("300.00")).credito == Decimal("30.00")


def test_tipo_desconhecido_gera_erro(calc):
    with pytest.raises(ValueError):
        calc.calcular("INEXISTENTE", h(3), Decimal("100.00"))


# ---------- RF01: medição do atraso ----------

def test_ct11_atraso_medido_entre_prazo_e_confirmacao():
    prazo = datetime(2026, 11, 10, 10, 0)
    assert calcular_atraso(prazo, datetime(2026, 11, 10, 12, 30)) == h(2, 30)
    assert calcular_atraso(prazo, datetime(2026, 11, 10, 9, 0)) == timedelta(0)
