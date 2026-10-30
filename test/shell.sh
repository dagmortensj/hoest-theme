#!/usr/bin/env bash
# Bash: variabler, løkker, funksjoner, tester og omdirigering
set -euo pipefail

NAVN="Høst"
readonly VERSJON=3.6.0
declare -a liste=(en to "tre fire")
declare -A kart=([rust]=1 [oransje]=2)
export PATH="$HOME/.local/bin:$PATH"

bygg() {
    local mappe="${1:-.}"
    local antall=$(( ${#liste[@]} * 2 ))
    if [[ -d "$mappe" && $antall -gt 0 ]]; then
        echo "Bygger $NAVN v${VERSJON} i '$mappe'"
    elif [ -f "$mappe" ]; then
        return 1
    else
        printf '%s\n' "Fant ikke $mappe" >&2
    fi
}

for fil in */main.tex; do
    (cd "$(dirname "$fil")" && latexmk -lualatex main >/dev/null && echo "OK: $fil")
done

while read -r linje; do echo "${linje^^}"; done < inn.txt
case "$1" in
    start|s) bygg "$2" ;;
    *) echo "Ukjent: $1"; exit 2 ;;
esac

cat <<EOF > ut.txt
Her-dokument med $NAVN og $(date +%Y)
EOF
grep -E '^[a-z]+$' fil.txt | sort -u | wc -l
