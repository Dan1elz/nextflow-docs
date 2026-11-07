# AGENTS.md — como trabalhar nesta documentação

Instruções para qualquer agente de IA (Claude Code, Codex, Cursor etc.) que leia ou edite esta pasta.

## Papel desta pasta
- Fonte de verdade do **produto**: visão, regras de negócio, decisões, arquitetura de alto nível e processos.
- **Fronteira:** documentação de produto, módulo, regra, decisão e processo fica aqui; padrão de código, setup de um
  repositório e skills de stack ficam no repositório de código (`AGENTS.md`, `docs/engineering-guidelines.md`,
  `docs/local-setup.md`). Aqui se descreve o **quê** e o **porquê**; lá, o **como**.
- Idioma: português do Brasil. Nomes de código citados como estão no código (inglês).

## Regras
1. **Nada é verdade sem validação.** Todo documento começa com o bloco de status (ver `README.md`). Ao extrair algo do
   código ou de um doc antigo, marque `rascunho / a validar` e registre a origem.
2. **Toda regra de negócio tem ID, fonte e data.** Formato: `| ID | Regra | Fonte | Data | Status |`. IDs não são reaproveitados;
   regra substituída fica como `obsoleto` com referência à nova.
3. **Uma decisão por arquivo**, numerada (`0001-titulo-curto.md`), no template de `architecture/decisions/0000-template.md`.
   Decisão que afeta o produto inteiro vai em `architecture/decisions/`; decisão de um módulo vai em `modules/<módulo>/decisions/`.
4. **Não invente regra.** Se o código faz algo e não há decisão, registre como "comportamento atual" e abra uma pergunta
   em "Perguntas em aberto" do documento. Não "corrija" a regra no texto.
5. **Features** (`modules/<módulo>/features/`) são o changelog do módulo: um arquivo por entrega de alto impacto
   (`AAAA-MM-DD-titulo.md`), escrito quando a entrega acontece. Não reescreva features antigas.
6. Mudou uma regra ou decisão? Atualize também o `overview.md` do módulo e o `product-overview.md` se o impacto for visível.
7. Diagramas em Mermaid dentro de Markdown (versionáveis). Imagem só quando Mermaid não der conta.
8. Sem segredos: nunca escreva chaves, senhas reais ou URLs com credencial.

## Skills de entrevista (`.agents/skills/`)
Use-as para **conduzir o Daniel** em vez de escrever sozinho: `prd` (produto e requisitos), `hld` (arquitetura de alto nível),
`fdd` (desenho de uma feature), `c4` (diagramas C4) e `mermaid` (qualquer diagrama). Pergunte pouco por vez, sempre com
uma recomendação embasada, e registre as respostas nos documentos com data.
