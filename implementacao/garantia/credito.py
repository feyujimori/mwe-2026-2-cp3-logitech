"""Regra de crédito da Garantia de Prazo (RF01 a RF04)."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

CENTAVOS = Decimal("0.01")

# Faixas de atraso são DADOS, não comportamento: (limite superior inclusivo, percentual base).
# None = sem limite superior.
FAIXAS_BASE = (
    (timedelta(hours=2), Decimal("0.00")),
    (timedelta(hours=24), Decimal("0.10")),
    (timedelta(hours=72), Decimal("0.25")),
    (None, Decimal("0.50")),
)


def calcular_atraso(prazo_prometido: datetime, confirmacao_entrega: datetime) -> timedelta:
    """RF01: atraso entre o prazo prometido e a confirmação. Nunca negativo."""
    return max(confirmacao_entrega - prazo_prometido, timedelta(0))


def percentual_base(atraso: timedelta) -> Decimal:
    for limite, percentual in FAIXAS_BASE:
        if limite is None or atraso <= limite:
            return percentual
    raise AssertionError("faixa não encontrada")


@dataclass(frozen=True)
class ResultadoGarantia:
    credito: Decimal
    notificar_atraso: bool


class RegraCliente(ABC):
    """Strategy: uma regra por tipo de cliente (RF04)."""

    @abstractmethod
    def calcular(self, atraso: timedelta, valor_frete: Decimal) -> Decimal: ...


class RegraPercentualComTeto(RegraCliente):
    def __init__(self, multiplicador: Decimal, teto: Decimal):
        self._multiplicador = multiplicador
        self._teto = teto

    def calcular(self, atraso, valor_frete):
        credito = valor_frete * percentual_base(atraso) * self._multiplicador
        return min(credito, self._teto)


class RegraCortesia(RegraCliente):
    def calcular(self, atraso, valor_frete):
        return Decimal("0")


def regras_padrao() -> dict:
    return {
        "VAREJO": RegraPercentualComTeto(Decimal("1"), Decimal("500.00")),
        "CORPORATIVO": RegraPercentualComTeto(Decimal("2"), Decimal("2000.00")),
        "CORTESIA": RegraCortesia(),
    }


class CalculadoraCredito:
    def __init__(self, regras: dict | None = None):
        self._regras = dict(regras) if regras is not None else regras_padrao()

    def registrar(self, tipo_cliente: str, regra: RegraCliente) -> None:
        """RF04: um tipo novo entra registrando uma regra, sem alterar as existentes."""
        self._regras[tipo_cliente] = regra

    def calcular(self, tipo_cliente: str, atraso: timedelta, valor_frete: Decimal) -> ResultadoGarantia:
        try:
            regra = self._regras[tipo_cliente]
        except KeyError:
            raise ValueError(f"Tipo de cliente desconhecido: {tipo_cliente}") from None
        credito = regra.calcular(atraso, valor_frete).quantize(CENTAVOS, rounding=ROUND_HALF_UP)
        return ResultadoGarantia(credito=credito, notificar_atraso=atraso > timedelta(0))
