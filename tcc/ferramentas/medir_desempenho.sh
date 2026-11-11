#!/usr/bin/env bash
# Mede o tempo de resposta das consultas principais (RNF003) numa API já no ar. Só faz GET: não gera análise nem chama a IA.
# Uso: API=http://backend:8080 SENHA='...' N=100 ./medir_desempenho.sh
# Saída (TSV): consulta, execuções, erros (HTTP diferente de 2xx), média, desvio padrão, p50, p95 e máximo, em ms.
# As requisições são sequenciais (sem carga concorrente), depois de uma execução de aquecimento por rota.
set -euo pipefail
API=${API:-http://localhost:8081}
EMAIL=${EMAIL:-admin@nextflow.com}
N=${N:-100}
: "${SENHA:?informe SENHA}"

TOKEN=$(curl -s -X POST "$API/api/auth/login" -H 'Content-Type: application/json' \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$SENHA\"}" | sed -E 's/.*"token":"([^"]+)".*/\1/')
[ ${#TOKEN} -gt 50 ] || { echo "login falhou"; exit 1; }

printf 'consulta\tn\terros\tmedia_ms\tdesvio_ms\tp50_ms\tp95_ms\tmax_ms\n'
medir() {
  local nome=$1 rota=$2 arq
  arq=$(mktemp)
  curl -s -o /dev/null -H "Authorization: Bearer $TOKEN" "$API$rota"   # aquecimento
  for _ in $(seq 1 "$N"); do
    curl -s -o /dev/null -w '%{http_code} %{time_total}\n' -H "Authorization: Bearer $TOKEN" "$API$rota" >> "$arq"
  done
  awk -v nome="$nome" '
    { if ($1 < 200 || $1 > 299) erros++; t[NR] = $2 * 1000; soma += t[NR]; soma2 += t[NR] * t[NR] }
    END {
      n = NR; media = soma / n; desvio = sqrt(soma2 / n - media * media)
      for (i = 1; i <= n; i++) for (j = i + 1; j <= n; j++) if (t[j] < t[i]) { x = t[i]; t[i] = t[j]; t[j] = x }
      p50 = t[int((n + 1) * 0.50)]; i95 = int(n * 0.95 + 0.999); if (i95 > n) i95 = n
      printf "%s\t%d\t%d\t%.1f\t%.1f\t%.1f\t%.1f\t%.1f\n", nome, n, erros + 0, media, desvio, p50, t[i95], t[n]
    }' "$arq"
  rm -f "$arq"
}

medir 'Listagem de produtos (20 por página)'          '/api/products?offset=0&limit=20'
medir 'Movimentações de estoque (20 por página)'      '/api/stock-movements?offset=0&limit=20'
medir 'Histórico de vendas (20 por página)'           '/api/orders?offset=0&limit=20'
medir 'Painel: indicadores de vendas do mês'          '/api/dashboard/sales-kpis'
medir 'Painel: faturamento de 12 meses'               '/api/dashboard/sales-chart'
medir 'Painel: estoque baixo'                         '/api/dashboard/low-stock'
medir 'Última análise de previsão'                    '/api/forecasts/latest'
