#!/usr/bin/env bash
# Monta o tcc.odt do zero a partir do original (commit 12fbc09), sempre na mesma ordem:
#   1. ajustes pontuais dos cap. 1 a 3 (alterações controladas, ops_cap1a3.py)
#   2. capítulo 4 inteiro (cap4.py)
#   3. capítulo 5 inteiro (cap5.py)
#   4. capítulo 6 inteiro (cap6.py)
# Uso (da pasta tcc/ferramentas): ./montar.sh   -> grava ../tcc.odt
# Atenção: sobrescreve o tcc.odt. Se o Daniel editou o arquivo à mão, commitar antes e incorporar as edições aqui.
set -euo pipefail
cd "$(dirname "$0")"
T=$(mktemp -d)
git show 12fbc09:tcc/tcc.odt > "$T/0.odt"
python3 -I odtrack.py "$T/0.odt" "$T/1.odt" ops_cap1a3.py | tail -1
python3 -I gerar_capitulo.py "$T/1.odt" "$T/2.odt" cap4.py
python3 -I gerar_capitulo.py "$T/2.odt" "$T/3.odt" cap5.py
python3 -I gerar_capitulo.py "$T/3.odt" "$T/4.odt" cap6.py
cp "$T/4.odt" ../tcc.odt
rm -rf "$T"
echo "tcc.odt montado"
