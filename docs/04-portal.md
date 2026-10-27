# 4. Tela do Portal do Cliente (RF10)

A tela é uma função do estado: `tela = f(estado)`. O hook `usePedidoAoVivo(pedidoId)` mantém o estado; cada componente só recebe props e desenha.

## Estados da tela

| Estado | Dados disponíveis | O que a tela exibe |
|---|---|---|
| `carregando` | Só o `pedidoId` | Esqueleto (placeholders) do cabeçalho, do mapa e do saldo |
| `erro` | Mensagem de erro | Aviso "Não foi possível carregar o pedido" e botão "Tentar novamente" |
| `aguardando_coleta` | Pedido, prazo prometido, saldo | Cabeçalho, prazo prometido, saldo; mapa sem veículo com o texto "Aguardando saída do veículo" |
| `em_transito_no_prazo` | Pedido, posição, previsão de chegada, prazo, saldo | Mapa com o veículo, previsão de chegada em verde, saldo |
| `em_transito_atrasado` | Os mesmos + atraso estimado | Mapa, previsão em vermelho, selo "Atrasado – você pode ter direito a crédito", saldo |
| `sem_sinal` | Última posição conhecida e o instante dela | Mapa com a última posição esmaecida e aviso "Última atualização há X min" (telemetria tolera perda: sem posição há mais de 90 s, isto é, 3 pacotes) |
| `conexao_perdida` | Último estado conhecido | Os dados da tela + faixa "Reconectando…" enquanto o SSE tenta reconectar |
| `entregue_com_credito` | Pedido, horário da entrega, crédito, número da nota, saldo atualizado | Confirmação da entrega, valor do crédito, número da nota de crédito, saldo novo |
| `entregue_sem_credito` | Pedido, horário da entrega, saldo | Confirmação da entrega (no prazo, na tolerância, cliente Cortesia ou ausência comprovada, com o motivo) e saldo |

## Árvore de componentes

```
<AcompanhamentoPedido pedidoId>
  ├── <EsqueletoAcompanhamento />            (estado carregando)
  ├── <MensagemErro />                       (estado erro)
  └── <PainelPedido>                         (demais estados)
        ├── <AvisoConexao />
        ├── <CabecalhoPedido />
        ├── <MapaVeiculo>
        │     └── <MarcadorVeiculo />
        ├── <PrevisaoChegada>
        │     └── <SeloAtraso />
        ├── <ResultadoEntrega />
        └── <SaldoCreditos />
```

| Componente | Props recebidas | Responsabilidade |
|---|---|---|
| `AcompanhamentoPedido` | `pedidoId` | Usa `usePedidoAoVivo(pedidoId)` (carga inicial via HTTP + assinatura SSE) e escolhe o que renderizar conforme `estado.tipo` |
| `EsqueletoAcompanhamento` | — | Placeholders enquanto carrega |
| `MensagemErro` | `mensagem`, `onTentarNovamente` | Mostra o erro e permite recarregar |
| `PainelPedido` | `estado` | Distribui os dados do estado para os filhos |
| `AvisoConexao` | `status: 'online' \| 'reconectando' \| 'sem_sinal'`, `ultimaAtualizacao` | Faixa de aviso de conexão SSE ou de telemetria parada |
| `CabecalhoPedido` | `numeroPedido`, `prazoPrometido`, `status` | Identificação do pedido e situação |
| `MapaVeiculo` | `posicao \| null`, `destino`, `desatualizada: boolean` | Desenha o mapa e o destino |
| `MarcadorVeiculo` | `latitude`, `longitude`, `desatualizada` | Ícone do veículo (esmaecido se sem sinal) |
| `PrevisaoChegada` | `previsao`, `prazoPrometido` | Mostra a previsão e calcula se está no prazo |
| `SeloAtraso` | `atrasado: boolean` | Selo vermelho de atraso |
| `ResultadoEntrega` | `entregueEm`, `credito \| null`, `numeroNota \| null`, `motivoSemCredito \| null` | Resultado da garantia após a entrega |
| `SaldoCreditos` | `saldo` (em centavos), `atualizadoEm` | Saldo de créditos formatado em R$ |

## Origem dos dados

| Dado | Origem | Como chega |
|---|---|---|
| Pedido e prazo prometido | Pedidos e Frete | HTTP GET no Portal BFF na carga inicial |
| Posição do veículo | Telemetria (UDP do veículo → evento `PosicaoAtualizada` no RabbitMQ) | BFF assina o evento e empurra via **SSE** (`event: posicao`) |
| Previsão de chegada | Frete (recalculada a partir da posição) | HTTP na carga inicial; atualizações via SSE (`event: previsao`) |
| Resultado da entrega e crédito | Garantia (`CreditoConcedido`) e Faturamento (`NotaDeCreditoEmitida`) | Via SSE (`event: entrega`, `event: credito`) |
| Saldo de créditos | Faturamento | HTTP na carga inicial; via SSE (`event: saldo`) a cada nota emitida |

Atualização ao vivo: o navegador abre `new EventSource('/api/pedidos/{id}/eventos')`. O BFF mantém a conexão aberta e, a cada evento do broker relativo àquele pedido/cliente, escreve uma mensagem SSE. O hook aplica cada evento num *reducer* (`estado = reducer(estado, evento)`) e o React redesenha. Se a conexão cai, o `EventSource` reconecta sozinho (com `Last-Event-ID`) e a tela mostra `conexao_perdida` até voltar.
