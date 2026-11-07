# Deploy

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** `nextflow/docs/DOCKER.MD` §2 e `nextflow-front/docs/DOCKER.md` §2

## Ambientes
Só existe **homologação (staging)**, numa VM pessoal do Daniel, atrás de um nginx de borda (rede `proxy-net`).
Não há produção nem pipeline de CI/CD.

| Serviço | Endereço |
|--|--|
| Front | `https://nextflow.zanni.tech` (alias `nextflow-web`) |
| API | `https://nextflow-api.zanni.tech` (alias `nextflow-api`, health `/health`) |
| Storage | `https://nextflow-s3.zanni.tech` (alias `nextflow-s3:9000`) |

## Passos (manual)
1. Redes: `nextflow-staging-network` e `proxy-net`.
2. API: exportar as variáveis obrigatórias (banco, `JWT_KEY`, `STORAGE_*`, `STORAGE_PUBLIC_URL`, `CORS_ORIGINS`,
   opcionais `AI_*` e `SEED_DEMO_*`; lista completa em `nextflow/docs/DOCKER.MD`) e rodar
   `docker compose -f compose.staging.yaml up -d --build`.
3. Front: `VITE_API_URL=https://nextflow-api.zanni.tech` no build (fica embutido no JS) e
   `docker compose -f compose.staging.yaml up -d --build`.
4. Conferir `/health` da API e o login no front.

## Regras
- Staging e produção usam imagens buildadas, nunca hot reload.
- Segredos são injetados na execução; nunca versionados.

## Perguntas em aberto
- Vai existir CI/CD (GitHub Actions) até a banca?
- A banca usa o staging ou uma máquina local?
- Backup do banco antes de deploy (`backups/` tem dumps manuais)?
