# 5. Uso de assistentes de IA

| Entrega | O que foi pedido | O que o assistente sugeriu | Decisão da dupla | Motivo |
|---|---|---|---|---|
| 1. Domínio | Proposta de bounded contexts e mapa de contexto a partir do enunciado | Sete contextos, com a Garantia de Prazo como contexto novo e o RF05 no Rastreamento | Aceito | Mantém a Garantia sem lógica de GPS e dá um dono único a cada requisito |
| 2. Arquitetura | Protocolos e padrões | UDP para telemetria, AMQP com fila durável para a confirmação, SSE para o Portal; Strategy, Adapter, Retry + DLQ, Idempotent Consumer, Outbox | Aceito | Cada escolha está ligada a um requisito (RNF01, RF07, RF08, RF09, RF10) |
| 2. Arquitetura | Numeração das notas | Primeiro `SEQUENCE` do PostgreSQL; depois linha de contador travada com `UPDATE ... RETURNING` | Aceito o contador travado; `SEQUENCE` descartada | `SEQUENCE` pode deixar buracos em rollback e o requisito pede numeração sequencial |
| 2. Arquitetura | Onde não aplicar padrão | Chain of Responsibility para as faixas de atraso | Descartado | Faixas são dados (limite, percentual), não comportamento diferente |
| 3. Testes | Casos com valores-limite e dublês | 18 casos com limites 2h00/2h01, 24h00/24h01, 72h00/72h01 e tetos | Aceito | Cobre as fronteiras exatas do RF02/RF03 |
| 3. Testes | Interpretação de "retentada até 3 vezes" | 1 envio + 3 retentativas = 4 chamadas | Aceito e registrado no plano | O enunciado é ambíguo; deixamos a convenção explícita |
| 4. Portal | Estados e componentes | 9 estados, incluindo `sem_sinal` e `conexao_perdida` | Aceito | A telemetria tolera perda, então a tela precisa mostrar dado desatualizado |
| 5. Implementação | Código da regra em Python + testes pytest | Strategy com `RegraPercentualComTeto` reaproveitada para Varejo e Corporativo | Aceito | Evita duplicar a lógica; o teste CT10 prova o RF04 |
