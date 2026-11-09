# Diagramas do TCC

> **Status:** rascunho, montado em 09/11/2026 a partir do código e do banco atuais; aguarda revisão do Daniel.

Cada tipo foi feito numa ferramenta diferente, escolhida depois de comparar um exemplo nas duas (PlantUML × Mermaid).
Todas as figuras são por escopo (uma por módulo ou fluxo, cabendo numa página do Word); visões completas vão para o apêndice.

| Tipo | Pasta | Ferramenta | Figuras | Por quê |
|--|--|--|--|--|
| Casos de uso | [casos-de-uso/](casos-de-uso) | PlantUML | 8 (UC01–UC52) | Mermaid não tem caso de uso UML (ator, fronteira, include/extend) |
| DER | [der/](der) | Mermaid `erDiagram` | 11 + apêndice | Tabela com tipo, chave e comentário; cor por módulo; verbos nas ligações |
| Classes | [classes/](classes) | PlantUML | 7 de domínio + camadas (+ versão de código em `classes/codigo/`) | UML completa, multiplicidades legíveis, layout compacto |
| Sequência | [sequencia/](sequencia) | Mermaid `sequenceDiagram` | 7 | Mesma identidade das figuras anteriores; faixas por fase e números |

As interfaces (prints das telas) estão em [`../../../screenshots/`](../../../screenshots).

## Princípios que valeram para todos
1. **Fonte = código e banco atuais**, nunca a memória nem o diagrama antigo.
2. **Nível documental**, não de implementação: português, conceitos e passos de negócio.
3. **Um escopo por figura**, até ~8 elementos; o total vai para o apêndice.
4. **Cor por módulo igual em DER e classes** (rosa Acesso, amarelo Cadastros, roxo Produto, verde Estoque, azul Vendas,
   laranja Compras, ciano Previsão).
5. **Legenda "como ler" e regras** na figura ou no README, e um **roteiro para a banca** em cada pasta.
6. **Fazer um exemplo antes de gerar todos** e comparar ferramentas: a melhor muda de um tipo para o outro.
7. **Revisar olhando o PNG** (folha de contato com todas as figuras ajuda a ver a consistência).

Cada pasta tem um README com o "como ler", o roteiro da banca, o método reaproveitável e os comandos para gerar de novo.
