# Prints das telas

> **Status:** gerado em 08/11/2026 a partir do ambiente de dev (seed demo da loja de doces, 2 lojas), para a documentação do TCC.

Uma print por tela, em desktop 1440 px (página inteira) nos temas claro e escuro, e as principais no celular (390 px, 2×).
Diálogos e gavetas saem com a janela normal. `report.json` lista, por tela, erros de console e respostas 4xx/5xx (vazio nesta rodada).

## Como gerar de novo
Com a API e o front de dev no ar (`http://127.0.0.1:5174`, API `http://localhost:8081`), no repositório do front:

```bash
npm run screenshots
```

Opções: `--only 10-previsao,20-venda-rapida` (só algumas telas), `--themes light` (só um tema), `--out <pasta>`.
O script fica em `nextflow-front/scripts/screenshots.mjs` e usa ids reais do banco de dev para as telas de detalhe.

## Telas
| Tela | Claro | Escuro | Celular |
|--|--|--|--|
| Login | [claro](light/00-login.png) | [escuro](dark/00-login.png) | — |
| Painel (dashboard) | [claro](light/01-painel.png) | [escuro](dark/01-painel.png) | [celular](mobile/01-painel.png) |
| Painel › Estoque baixo (ver mais) | [claro](light/02-painel-estoque-baixo.png) | [escuro](dark/02-painel-estoque-baixo.png) | — |
| Painel › Lotes vencendo (ver mais) | [claro](light/03-painel-lotes-vencendo.png) | [escuro](dark/03-painel-lotes-vencendo.png) | — |
| Previsão de demanda (IA) | [claro](light/10-previsao.png) | [escuro](dark/10-previsao.png) | [celular](mobile/10-previsao.png) |
| Previsão › detalhe da recomendação | [claro](light/11-previsao-detalhe.png) | [escuro](dark/11-previsao-detalhe.png) | — |
| Previsão › histórico de análises | [claro](light/12-previsao-historico.png) | [escuro](dark/12-previsao-historico.png) | — |
| Previsão › precisão | [claro](light/13-previsao-precisao.png) | [escuro](dark/13-previsao-precisao.png) | — |
| Venda rápida | [claro](light/20-venda-rapida.png) | [escuro](dark/20-venda-rapida.png) | [celular](mobile/20-venda-rapida.png) |
| Histórico de vendas | [claro](light/21-historico-vendas.png) | [escuro](dark/21-historico-vendas.png) | — |
| Histórico › detalhe da venda | [claro](light/22-historico-vendas-detalhe.png) | [escuro](dark/22-historico-vendas-detalhe.png) | — |
| Pedidos de compra | [claro](light/30-pedidos-compra.png) | [escuro](dark/30-pedidos-compra.png) | [celular](mobile/30-pedidos-compra.png) |
| Novo pedido de compra | [claro](light/31-pedido-compra-novo.png) | [escuro](dark/31-pedido-compra-novo.png) | — |
| Pedido de compra (pendente) | [claro](light/32-pedido-compra-visualizar.png) | [escuro](dark/32-pedido-compra-visualizar.png) | — |
| Editar pedido de compra (orçamento) | [claro](light/33-pedido-compra-editar.png) | [escuro](dark/33-pedido-compra-editar.png) | — |
| Promoções | [claro](light/40-promocoes.png) | [escuro](dark/40-promocoes.png) | — |
| Produtos | [claro](light/50-produtos.png) | [escuro](dark/50-produtos.png) | [celular](mobile/50-produtos.png) |
| Novo produto | [claro](light/51-produto-novo.png) | [escuro](dark/51-produto-novo.png) | — |
| Produto › variações | [claro](light/52-produto-visualizar.png) | [escuro](dark/52-produto-visualizar.png) | [celular](mobile/52-produto-visualizar.png) |
| Produto › estoque por local | [claro](light/52b-produto-estoque.png) | [escuro](dark/52b-produto-estoque.png) | — |
| Produto › lotes | [claro](light/52c-produto-lotes.png) | [escuro](dark/52c-produto-lotes.png) | — |
| Produto › previsão | [claro](light/52d-produto-previsao.png) | [escuro](dark/52d-produto-previsao.png) | — |
| Editar produto | [claro](light/53-produto-editar.png) | [escuro](dark/53-produto-editar.png) | — |
| Categorias | [claro](light/54-categorias.png) | [escuro](dark/54-categorias.png) | — |
| Coleções | [claro](light/55-colecoes.png) | [escuro](dark/55-colecoes.png) | — |
| Calendário de eventos | [claro](light/56-calendario.png) | [escuro](dark/56-calendario.png) | — |
| Movimentações de estoque (kardex) | [claro](light/57-movimentacoes.png) | [escuro](dark/57-movimentacoes.png) | — |
| Clientes | [claro](light/60-clientes.png) | [escuro](dark/60-clientes.png) | — |
| Cliente | [claro](light/61-cliente-visualizar.png) | [escuro](dark/61-cliente-visualizar.png) | — |
| Novo cliente | [claro](light/62-cliente-novo.png) | [escuro](dark/62-cliente-novo.png) | — |
| Fornecedores | [claro](light/63-fornecedores.png) | [escuro](dark/63-fornecedores.png) | — |
| Fornecedor | [claro](light/64-fornecedor-visualizar.png) | [escuro](dark/64-fornecedor-visualizar.png) | — |
| Novo fornecedor | [claro](light/65-fornecedor-novo.png) | [escuro](dark/65-fornecedor-novo.png) | — |
| Usuários | [claro](light/66-usuarios.png) | [escuro](dark/66-usuarios.png) | — |
| Usuário | [claro](light/67-usuario-visualizar.png) | [escuro](dark/67-usuario-visualizar.png) | — |
| Novo usuário | [claro](light/68-usuario-novo.png) | [escuro](dark/68-usuario-novo.png) | — |
| Lojas e locais | [claro](light/70-lojas-e-locais.png) | [escuro](dark/70-lojas-e-locais.png) | — |
| Política de estoque (ABC) | [claro](light/71-politica-estoque.png) | [escuro](dark/71-politica-estoque.png) | — |
| Agendamento da previsão | [claro](light/72-agendamento-previsao.png) | [escuro](dark/72-agendamento-previsao.png) | — |
| Meu perfil | [claro](light/73-perfil.png) | [escuro](dark/73-perfil.png) | — |

## Observações
- Os números vêm do seed demo e da última análise gerada no dev (08/11/2026 às 19:59). Para a print da previsão mostrar a
  compra dividida por loja (RN-DF27), gerar uma análise nova antes de rodar o script.
- O horário do agendamento aparece com AM/PM por causa do campo de hora nativo do Chromium headless; no navegador em pt-BR é 24 h.
