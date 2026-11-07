# Resposta a incidentes

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** proposta inicial, sem fonte anterior (não há processo hoje)

## Hoje
Não há monitoramento, alerta nem plantão. O único ambiente publicado é o staging.

## Roteiro mínimo (proposta)
1. Confirmar: `GET /health` da API e login no front.
2. Logs: `docker compose -f compose.staging.yaml logs -f <serviço>` (API, banco, storage).
3. Causas conhecidas: storage sem subir (ver `storage-initial-setup`), migration ou seeder com falha (derruba o startup),
   chave de IA inválida (análise fica `CompletedWithoutAi`, não é incidente), `VITE_API_URL` errada no build do front.
4. Restaurar: subir de novo com a imagem anterior; banco a partir de dump em `backups/`.
5. Registrar o que aconteceu (data, causa, correção) em `process/incidents/AAAA-MM-DD-titulo.md`.

## Perguntas em aberto
- Isso é necessário para o TCC ou fica como esboço?
