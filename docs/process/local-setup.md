# Setup local

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** `nextflow/docs/DOCKER.MD` e `nextflow-front/docs/DOCKER.md`

## Pré-requisitos
Docker Desktop, .NET 10 SDK (para `dotnet run` fora do Docker), Node.js (para `npm run dev` fora do Docker), Git.

## Passo a passo
1. Rede compartilhada (uma vez):
   `docker network inspect nextflow-development-network >/dev/null 2>&1 || docker network create nextflow-development-network`
2. API: em `nextflow/`, copie `.env.example` para `.env` e rode `docker compose -f compose.development.yaml up -d --build`.
   Sobe API (`:8080`), PostgreSQL (`:5432`), storage S3 (`:9000`, painel `:9001`) e o `storage-initial-setup`
   (termina com `Exited (0)` e "Storage pronto.": é o normal).
3. Front: em `nextflow-front/`, copie `.env.example` para `.env` (`VITE_API_URL=http://localhost:8080`) e rode
   `docker compose -f compose.development.yaml up -d --build`. Acesse `http://localhost:5173`.
4. Migrations e seeders rodam no startup da API. Com `Seed:Demo:Enabled=true` (padrão no dev) é criada a loja de
   demonstração (~30 s). A IA é opcional: sem `AI_API_KEY`, a previsão roda só com o cálculo.

## Login inicial
Criado pelo `UsersSeeder`. **A documentar:** usuário e senha de dev (não registrar senha real aqui).

## Perguntas em aberto
- Há um script único que suba tudo (API + front)?
