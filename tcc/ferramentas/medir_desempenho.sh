#!/usr/bin/env bash
# Mede o tempo médio de resposta das consultas principais (RNF003) numa API já no ar.
# Uso: API=http://127.0.0.1:18081 SENHA='...' N=20 ./medir_desempenho.sh
# Só faz GET (não gera análise nem chama a IA). Saída: consulta | execuções | média ms | máx ms
set -euo pipefail
API=${API:-http://localhost:8081}
EMAIL=${EMAIL:-admin@nextflow.com}
N=${N:-20}
: "${SENHA:?informe SENHA}"

TOKEN=$(curl -s -X POST "$API/api/auth/login" -H 'Content-Type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$SENHA\"}" | sed -E 's/.*"token":"([^"]+)".*/\1/')
[ ${#TOKEN} -gt 50 ] || { echo "login falhou"; exit 1; }

medir() {
  local nome=$1 rota=$2 soma=0 max=0 t
  curl -s -o /dev/null -H "Authorization: Bearer $TOKEN" "$API$rota"   # aquecimento
  for _ in $(seq 1 "$N"); do
    t=$(curl -s -o /dev/null -w '%{time_total}' -H "Authorization: Bearer $TOKEN" "$API$rota")
    t=$(awk -v t="$t" 'BEGIN{printf "%d", t*1000}')
    soma=$((soma + t)); [ "$t" -gt "$max" ] && max=$t
  done
  printf '%s | %d | %d | %d\n' "$nome" "$N" $((soma / N)) "$max"
}

medir 'Listagem de produtos (20 por página)'        '/api/products?offset=0&limit=20'
medir 'Movimentações de estoque (20 por página)'    '/api/stock-movements?offset=0&limit=20'
medir 'Histórico de vendas (20 por página)'         '/api/orders?offset=0&limit=20'
medir 'Painel: indicadores de vendas do mês'        '/api/dashboard/sales-kpis'
medir 'Painel: faturamento de 12 meses'             '/api/dashboard/sales-chart'
medir 'Painel: estoque baixo'                       '/api/dashboard/low-stock'
medir 'Última análise de previsão (42 recomendações)' '/api/forecasts/latest'
