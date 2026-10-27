# CP3: Garantia de Prazo LogiTech

**Microservice and Web Engineering & IT Services** · Sistemas de Informação · FIAP
Prof. José Romualdo · Checkpoint 3 · 27/10/2026 · Atividade em dupla · Duração: 2h30

## Dupla

| Nome | RM |
|---|---|
|Felipe Yuji Mori|559674|
| | |

## Contexto

A LogiTech vai lançar a **Garantia de Prazo**: se a entrega atrasar, o cliente recebe
crédito automático. O comercial anunciou o produto na segunda-feira e precisa do
desenho técnico até o fim da semana.

A plataforma já tem os serviços que vocês conhecem ao longo do semestre: telemetria da
frota, Pedidos (Java), Faturamento (C#), Frete (Python), Notificações (Node/TypeScript)
e o Portal do Cliente (React). A tarefa da dupla é modelar a Garantia de Prazo sobre essa
plataforma, desenhar a arquitetura, planejar os testes e, se houver tempo, começar a
implementação.

## Requisitos funcionais

| ID | Requisito |
|---|---|
| RF01 | O atraso é medido em horas, entre o prazo prometido pelo serviço de Frete e a confirmação da entrega |
| RF02 | Cliente **Varejo**: atraso de até 2 h não gera crédito; acima de 2 h e até 24 h, 10% do frete; acima de 24 h e até 72 h, 25% do frete; acima de 72 h, 50% do frete. O crédito máximo é de R$ 500 por pedido |
| RF03 | Cliente **Corporativo**: os percentuais do RF02 dobram e o crédito máximo é de R$ 2.000 por pedido. Cliente **Cortesia** (frete zero) não recebe crédito, mas é notificado do atraso |
| RF04 | Um novo tipo de cliente, previsto para o próximo trimestre, não pode exigir alteração nas regras dos tipos já existentes |
| RF05 | Não há crédito quando a ausência do destinatário for comprovada pela telemetria: veículo parado a até 200 m do endereço por pelo menos 10 min antes do registro da ausência |
| RF06 | Cada crédito gera uma nota de crédito no Faturamento, com número sequencial e nunca repetido |
| RF07 | O cliente é notificado pelo canal preferido: e-mail, pelo serviço atual, ou WhatsApp, por uma empresa parceira nova cuja API tem formato diferente do serviço atual |
| RF08 | Uma falha de envio de notificação é retentada até 3 vezes. A falha final não pode ser descartada em silêncio |
| RF09 | Se a mesma confirmação de entrega chegar duas vezes, só um crédito é gerado |
| RF10 | O Portal do Cliente mostra a posição do veículo, a previsão de chegada e o saldo de créditos, com atualização ao vivo |

## Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF01 | A telemetria dos veículos chega a cada 30 s e tolera perda de pacotes. A confirmação de entrega não tolera perda |
| RNF02 | O crédito é emitido em até 5 min após a confirmação da entrega |
| RNF03 | Nenhum número de nota de crédito se repete em 1.000 emissões concorrentes |
| RNF04 | Cada serviço roda em contêiner, e o conjunto sobe com um único comando |

## Entregas

Cada entrega tem um arquivo próprio em `docs/`, já com a estrutura esperada. Preencham
o arquivo e apaguem as instruções entre `<!-- -->` que não forem mais necessárias.

| Tempo sugerido | Entrega | Arquivo |
|---|---|---|
| 0:00 a 0:10 | Leitura do problema e criação do repositório da dupla | |
| 0:10 a 0:40 | **1. Modelagem do domínio** | [`docs/01-dominio.md`](docs/01-dominio.md) |
| 0:40 a 1:10 | **2. Arquitetura** | [`docs/02-arquitetura.md`](docs/02-arquitetura.md) |
| 1:10 a 1:50 | **3. Plano de testes** | [`docs/03-testes.md`](docs/03-testes.md) |
| 1:50 a 2:00 | **4. Tela do Portal do Cliente** | [`docs/04-portal.md`](docs/04-portal.md) |
| 2:00 a 2:25 | **5. Implementação em TDD** (necessária para a nota máxima) | [`implementacao/`](implementacao/README.md) |
| 2:25 a 2:30 | Último commit e envio do link | |

Durante toda a atividade, registrem o uso de assistentes de IA em
[`docs/05-uso-de-ia.md`](docs/05-uso-de-ia.md).

## Regras

1. Criem o repositório da dupla com **Use this template** e deixem-no **público**.
2. Façam **pelo menos um commit até 1h10 de atividade**, com a modelagem preenchida.
3. Usem Conventional Commits (`docs: ...`, `test: ...`, `feat: ...`, `refactor: ...`).
4. Commits feitos depois do horário de encerramento não são considerados.
5. Ao final, enviem o link do repositório pelo formulário: **[link do Forms]**.

## Critérios de avaliação

| Entrega | O que é avaliado |
|---|---|
| Modelagem | Cada requisito tem um único contexto responsável; as fronteiras entre contextos são coerentes com a linguagem do negócio |
| Arquitetura | Protocolo de cada comunicação justificado pelo requisito que ela atende; padrão de projeto aplicado onde o requisito pede e justificado; decisão explícita de onde não aplicar padrão; solução para o RF09 |
| Testes | Casos rastreados até o requisito; valores-limite exatos; dublê de teste coerente com o que o caso verifica; proporção da pirâmide justificada |
| Tela | Tela descrita como função do estado, com os estados possíveis e os componentes que os exibem |
| Implementação | Testes escritos antes do código, visíveis no histórico de commits; testes executando e passando; regras do RF02 ao RF04 cobertas |
| Uso de IA | Registro do que foi sugerido pelo assistente e do que a dupla aceitou ou descartou, com o motivo |
