# 3. Plano de testes

## Pirâmide de testes

| Nível | Quantidade de casos | O que cobre |
|---|---|---|
| Unidade | 13 (CT01 a CT13) | Regras puras: cálculo do atraso (RF01), faixas, percentuais e tetos (RF02/RF03), extensão por novo tipo (RF04), regra de ausência comprovada (RF05), adapter do WhatsApp (RF07) e política de retentativa (RF08) |
| Integração | 3 (CT14 a CT16) | O que só um banco ou broker real prova: numeração sem repetição sob concorrência (RF06/RNF03), idempotência da confirmação duplicada (RF09) e não perda da confirmação com o consumidor fora do ar (RNF01) |
| Ponta a ponta | 2 (CT17 e CT18) | Fluxo completo confirmação → crédito → nota → notificação em até 5 min (RNF02) e atualização ao vivo no Portal (RF10) |

Por que essa proporção: o maior risco da Garantia de Prazo é **errar o valor do crédito** — dinheiro devolvido a mais ou a menos. Essas regras têm muitos valores-limite e são puras, então ficam em testes de unidade, rápidos e numerosos. Integração fica restrita aos requisitos que dependem de concorrência ou entrega de mensagens, porque um dublê esconderia exatamente o problema (ex.: um mock de banco nunca mostra número repetido). Ponta a ponta é lento e frágil (sobe todos os contêineres), então só cobre os dois requisitos que são, por natureza, do sistema inteiro.

## Casos de teste

Convenção: atraso até 2 h **inclusive** não gera crédito; os limites 24 h e 72 h pertencem à faixa de baixo. "Retentado até 3 vezes" = 1 envio + 3 retentativas = 4 chamadas no total.

| ID | Requisito | Pré-condição | Entrada | Resultado esperado | Nível | Dublê | Justificativa do dublê |
|---|---|---|---|---|---|---|---|
| CT01 | RF02 | Cliente Varejo, frete de R$ 300,00 | Atraso de 1h59 | Crédito de R$ 0,00 | Unidade | Nenhum | Regra pura, sem dependência externa |
| CT02 | RF02 | Cliente Varejo, frete de R$ 300,00 | Atraso de exatamente 2h00 | Crédito de R$ 0,00 (limite da tolerância) | Unidade | Nenhum | Regra pura |
| CT03 | RF02 | Cliente Varejo, frete de R$ 300,00 | Atraso de 2h01 | Crédito de R$ 30,00 (10%) | Unidade | Nenhum | Regra pura |
| CT04 | RF02 | Cliente Varejo, frete de R$ 300,00 | Atraso de 24h00 e de 24h01 | R$ 30,00 (10%) e R$ 75,00 (25%) | Unidade | Nenhum | Regra pura |
| CT05 | RF02 | Cliente Varejo, frete de R$ 300,00 | Atraso de 72h00 e de 72h01 | R$ 75,00 (25%) e R$ 150,00 (50%) | Unidade | Nenhum | Regra pura |
| CT06 | RF02 | Cliente Varejo, frete de R$ 1.200,00 | Atraso de 80h | R$ 500,00 (50% = 600, limitado ao teto) | Unidade | Nenhum | Regra pura |
| CT07 | RF03 | Cliente Corporativo, frete de R$ 300,00 | Atraso de 2h01, 24h01 e 72h01 | R$ 60,00 (20%), R$ 150,00 (50%) e R$ 300,00 (100%) | Unidade | Nenhum | Regra pura |
| CT08 | RF03 | Cliente Corporativo, frete de R$ 5.000,00 | Atraso de 80h | R$ 2.000,00 (100% = 5.000, limitado ao teto) | Unidade | Nenhum | Regra pura |
| CT09 | RF03 | Cliente Cortesia, frete de R$ 0,00 | Atraso de 80h | Crédito de R$ 0,00 **e** indicação de notificar atraso = verdadeiro | Unidade | Nenhum | Regra pura |
| CT10 | RF04 | Calculadora com as regras padrão | Registrar um tipo novo "PREMIUM" com regra própria e calcular Varejo, frete R$ 300, atraso 2h01 | PREMIUM usa a regra nova; Varejo continua R$ 30,00, sem alterar nenhuma classe existente | Unidade | Stub | Regra do tipo novo é um stub que devolve valor fixo: só interessa provar que ela é usada e que as antigas não mudam |
| CT11 | RF01 | Prazo prometido 10/11 às 10h00 | Entrega às 12h30; e outra às 09h00 | Atraso de 2,5 h; e atraso de 0 h (entrega antecipada não gera atraso negativo) | Unidade | Nenhum | Cálculo puro sobre duas datas |
| CT12 | RF05 | Endereço de entrega conhecido; posições da telemetria em memória | Veículo parado a 200 m por 10 min antes da ausência; a 201 m por 10 min; a 200 m por 9min59 | Comprovada; não comprovada; não comprovada | Unidade | Stub | Stub do repositório de posições devolve a sequência de posições do cenário; o teste verifica o resultado da regra, não a chamada |
| CT13 | RF07, RF08 | Cliente com canal WhatsApp; cliente do parceiro falha sempre | Enviar notificação | Parceiro chamado 4 vezes (1 + 3 retentativas) no formato da API do parceiro; mensagem publicada uma vez na fila de falhas | Unidade | Mock + Spy | Spy no cliente do parceiro para contar chamadas e conferir o formato traduzido pelo adapter; Mock da fila de falhas para verificar que `publicar` foi chamada uma vez (o que se verifica é a interação, não um valor de retorno) |
| CT14 | RF06, RNF03 | Faturamento com PostgreSQL real em contêiner | 1.000 emissões de nota concorrentes | 1.000 notas com números distintos, de 1 a 1.000, sem buracos | Integração | Nenhum | O defeito procurado (corrida no banco) só aparece com o banco real; um dublê esconderia o problema |
| CT15 | RF09 | Garantia com banco e RabbitMQ reais | Mesma `EntregaConfirmada` (mesmo id) publicada duas vezes | Uma apuração, um `CreditoConcedido`, uma nota de crédito | Integração | Stub | Stub HTTP de Frete e Telemetria com prazo, valor e "ausência não comprovada" fixos; banco e broker são reais porque é neles que a idempotência acontece |
| CT16 | RNF01 | Consumidor da Garantia parado | Publicar `EntregaConfirmada`, reiniciar o broker e depois subir a Garantia | Mensagem processada após a subida; crédito gerado | Integração | Nenhum | O que se testa é a durabilidade da fila real |
| CT17 | RNF02, RF06, RF07 | Todos os serviços no `docker compose`; cliente Varejo com e-mail | Confirmação de entrega com 30 h de atraso, frete R$ 300 | Nota de R$ 75,00 emitida e e-mail registrado em até 5 min | Ponta a ponta | Stub | Só o servidor de e-mail externo é um stub (ex.: MailHog), para não enviar e-mail real |
| CT18 | RF10 | Portal aberto para um pedido em trânsito | Telemetria publica nova posição; Faturamento emite nota | Mapa e saldo atualizam na tela sem recarregar | Ponta a ponta | Nenhum | Verifica o caminho real broker → BFF → SSE → navegador |

## Mutante que o plano detecta

| Mutante | Caso que o detecta | Por quê |
|---|---|---|
| Trocar `atraso <= 2h` por `atraso < 2h` na tolerância | CT02 | Com o mutante, exatamente 2h00 sai da tolerância e gera R$ 30,00; o CT02 espera R$ 0,00 |
| Trocar o teto do Varejo de 500 para 5.000 | CT06 | O crédito passa a ser R$ 600,00 em vez de R$ 500,00 |
| Trocar o multiplicador do Corporativo de 2 para 1 | CT07 | 2h01 com frete R$ 300 passa a dar R$ 30,00 em vez de R$ 60,00 |
