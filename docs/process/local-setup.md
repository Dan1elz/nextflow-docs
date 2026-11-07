# Setup local

> **Status:** conferido contra os arquivos reais · **Atualizado:** 2026-11-07
> **Origem:** `nextflow/compose.development.yaml`, `nextflow/.env.example`, `nextflow/docs/local-setup.md`,
> `nextflow-front/compose.development.yaml`, `nextflow-front/docs/local-setup.md`.
> Passo a passo completo de uma máquina nova: `../HANDOFF.md`, seção "Setup do zero".

## Pré-requisitos
WSL 2 (Ubuntu) com os repos dentro do Linux, Docker Desktop com integração WSL, Git com chave SSH no GitHub. Opcionais:
.NET 10 SDK (testes, migrations, `dotnet run`) e Node.js (`npm run dev` fora do Docker).

## Layout
```
~/Projetos/nextflow/
  nextflow/         API .NET   (git@github.com:Dan1elz/nextflow.git, branch homolog)
  nextflow-front/   React      (git@github.com:Dan1elz/nextflow-front.git, branch homolog)
  nextflow-docs/    docs       (git@github.com:Dan1elz/nextflow-docs.git, branch main)
```

## Passo a passo
1. API: em `nextflow/`, `docker compose -f compose.development.yaml up -d --build`. Sem `.env` (padrões do compose).
   Sobe API `:8081`, PostgreSQL `:5435`, storage S3 `:9010` (painel `:9011`) e o `storage-initial-setup` (termina com
   `Exited (0)` e "Storage pronto.": é o normal). Não há rede compartilhada a criar.
2. Migrations e seeders rodam no startup. Seed demo ligado (`Seed:Demo:Enabled`, `SEED_DEMO_ENABLED=true`) com 36 meses
   de histórico (`Seed:Demo:HistoryMonths` no `appsettings.Development.json`): o primeiro startup leva de 3 a 5 min.
3. Front: em `nextflow-front/`, `docker compose -f compose.development.yaml up -d --build` e abra
   `http://localhost:5174` (hot reload; API padrão `http://localhost:8081`).
4. Opcional: front buildado no nginx pelo compose do back, `--profile front`, em `http://localhost:8082`.

## Login inicial
`admin@nextflow.com`, criado pelo `UsersSeeder` com o banco vazio. Senha de dev: constante `DevelopmentPassword` em
`nextflow/nextflow.Infrastructure/Seeders/UsersSeeder.cs`. Fora do dev a senha vem de `Seed__Admin__Password`
(`SEED_ADMIN_PASSWORD` nos compose de staging e da VM; no compose de dev ela é ignorada).

## Perguntas em aberto
- Há um script único que suba tudo (API + front)? Hoje não: são dois `docker compose up`.
