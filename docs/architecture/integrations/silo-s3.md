# Integração — Storage S3 (Silo)

> **Status:** rascunho / a validar · **Atualizado:** 2026-10-28
> **Origem:** `nextflow/docs/PROJECT.md` §10 e `DOCKER.MD` · Decisão: 0006

## Contrato
| Item | Valor |
|--|--|
| Produto | Silo (`pgsty/silo` + `pgsty/mc`), compatível com S3; serviço `storage` no compose |
| Abstração | `IFileStorage` (`UploadAsync`, `DeleteAsync`, `GetPublicUrl`, `GetSignedUrl`) |
| Implementação | `S3FileStorage` (AWSSDK.S3, path style); um cliente interno e outro só para assinar com a URL pública |
| Buckets | `nextflow-public` (leitura anônima só em `products/`) e `nextflow-private` (só URL assinada) |
| Credenciais | usuário próprio da API (`STORAGE_ACCESS_KEY`) com política restrita aos dois buckets |
| Setup | `storage/init.sh`, idempotente, roda a cada `up` (`storage-initial-setup`) |

## Regras
- O banco guarda a **chave** (`products/<id>.png`), nunca a URL.
- Validação do arquivo é do use case (JPG/PNG/WebP, até 5 MB, assinatura dos bytes).
- Troca de imagem: sobe a nova → grava no banco → apaga a antiga; se o banco falhar, apaga a nova.
- Falha ao apagar arquivo antigo só gera aviso no log.

## Ambientes
Dev: `http://localhost:9000` (painel `:9001`). Staging: `https://nextflow-s3.zanni.tech` via proxy de borda.
