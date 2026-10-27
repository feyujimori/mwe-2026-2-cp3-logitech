# 5. Implementação em TDD

Implementem a regra de cálculo do crédito (RF02, RF03 e RF04) em **uma** linguagem à
escolha da dupla: Java, C#, Python ou TypeScript. O Codespace deste repositório já traz
as quatro.

## O que registrar aqui

- Linguagem e framework de teste: Python 3 + pytest
- Comando para executar os testes: `cd implementacao && pip install pytest && python -m pytest -v`
- Casos do plano implementados (IDs): CT01, CT02, CT03, CT04, CT05, CT06, CT07, CT08, CT09, CT10, CT11 (+ teste extra de tipo desconhecido)
- Saída da última execução dos testes:

```
collecting ... collected 12 items

tests/test_credito.py::test_ct01_varejo_atraso_abaixo_da_tolerancia_nao_gera_credito PASSED [  8%]
tests/test_credito.py::test_ct02_varejo_atraso_exatamente_2h_nao_gera_credito PASSED [ 16%]
tests/test_credito.py::test_ct03_varejo_atraso_2h01_gera_10_por_cento PASSED [ 25%]
tests/test_credito.py::test_ct04_varejo_limite_24h PASSED                [ 33%]
tests/test_credito.py::test_ct05_varejo_limite_72h PASSED                [ 41%]
tests/test_credito.py::test_ct06_varejo_credito_limitado_ao_teto_de_500 PASSED [ 50%]
tests/test_credito.py::test_ct07_corporativo_percentuais_dobrados PASSED [ 58%]
tests/test_credito.py::test_ct08_corporativo_credito_limitado_ao_teto_de_2000 PASSED [ 66%]
tests/test_credito.py::test_ct09_cortesia_nao_recebe_credito_mas_e_notificado PASSED [ 75%]
tests/test_credito.py::test_ct10_novo_tipo_registrado_sem_alterar_regras_existentes PASSED [ 83%]
tests/test_credito.py::test_tipo_desconhecido_gera_erro PASSED           [ 91%]
tests/test_credito.py::test_ct11_atraso_medido_entre_prazo_e_confirmacao PASSED [100%]

============================== 12 passed in 0.02s ==============================
```

## Decisões de implementação

- **Strategy** (`RegraCliente`): `RegraPercentualComTeto` serve Varejo (×1, teto R$ 500) e Corporativo (×2, teto R$ 2.000); `RegraCortesia` devolve zero. Tipo novo = nova classe + `calculadora.registrar(...)` (RF04, provado no CT10).
- **Faixas como dados** (`FAIXAS_BASE`), sem padrão de projeto — ver `docs/02-arquitetura.md`.
- Atraso como `timedelta` e dinheiro como `Decimal` arredondado a centavos, para os valores-limite serem exatos.
