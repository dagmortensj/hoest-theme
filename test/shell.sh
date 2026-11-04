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

# Vanskelige tilfeller: aritmetikk, parameterutvidelse, tester, rør og sitering
teller=0; ((teller += 1)); ((teller **= 2)); ((teller <<= 1)); ((teller |= 1)); : $((teller % 2 == 0 ? 1 : -1))
tekst="a + b == c"; tekst+=" og $teller"; rå='ingen $utvidelse \n'; ekko=$'tab\tog nylinje\n'
echo "${tekst//==/!=} ${tekst:2:5} ${#tekst} ${tekst^} ${tekst,,} ${rå@Q} ${liste[-1]} ${!kart[@]} ${ukjent:-standard}"
[[ $teller -ge 1 && ( $tekst == a* || $tekst =~ ^[a-z]+\ \+ ) ]] && echo ja || echo nei
[ "$teller" -ne 0 -a -n "$tekst" ] || [ ! -z "${tom:+x}" ]; test -r fil.txt -o -w fil.txt
if (( teller > 10 )); then :; elif [[ -z $tekst ]]; then exit 1; fi
til() { local -n ref=$1; ref=$(( ref * 2 )); return $(( ref > 100 ? 1 : 0 )); }
mapfile -t linjer < <(printf '%s\n' "${liste[@]}" | sed -E 's/(en|to)/\U&/g; s/^/> /' | tr -d '\r')
for ((i = 0; i < ${#linjer[@]}; i++)); do [[ ${linjer[i]} =~ ^\> ]] && { echo "${linjer[i]#> }"; continue; }; done
while IFS=: read -r bruker _ uid _; do (( uid >= 1000 )) && echo "$bruker"; done < /etc/passwd 2>/dev/null
kommando="ls -la"; eval "$kommando" | awk -F' ' 'NR > 1 && $5 ~ /[0-9]+/ { sum += $5 } END { print sum }'
find . -name '*.tex' -newer main.tex -exec grep -l '\\section' {} + 2>&1 | tee logg.txt >/dev/null
trap 'echo "avbrutt ved linje $LINENO" >&2; exit 130' INT TERM; set +e; false; echo "status $? ${ekko}"
