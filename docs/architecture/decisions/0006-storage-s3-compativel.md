# 0006 — Arquivos em storage compatível com S3

> **Status:** rascunho / a validar · **Data:** 2026-10-27 · **Origem:** `nextflow/docs/PROJECT.md` §10 (thread de storage)

## Contexto
Imagens eram salvas em disco local (`LocalStorageService`), o que não escala e se perde com o container.

## Decisão
Arquivos ficam num storage S3 (hoje **Silo**, fork comunitário do MinIO). O banco guarda só a **chave** do arquivo; a URL é
montada na leitura. Bucket público por prefixo (imagens de produto) e bucket privado com URL assinada.

## Consequências
- Trocar de produto (AWS S3, R2, outro) mexe só no compose e na configuração.
- Contrato em `integrations/silo-s3.md`.
