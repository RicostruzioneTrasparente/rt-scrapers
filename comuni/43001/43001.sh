#!/bin/bash

set -x

comune="43001"

cartella=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

rm "$cartella"/allegati.csv

curl -sL "http://www.comune.acquacanina.mc.it/albo-pretorio/" | scrape -be "#container > div.wrapper > div.col1 > div.single_post > table > tr" | xml2json | jq '[[.html.body.tr[] | {registro:.td[0].small."$t",tipologia:.td[1].small."$t",titolo:.td[2].small.a."$t",stato:.td[3].small."$t",dal:.td[4].small."$t",al:.td[5].small."$t",URI:.td[2].small.a.href}] | .[] | select(.registro != null)]' | in2csv --no-inference -f json > "$cartella"/"$comune"_temp.csv

pagine=$(csvsql --query 'select URI from "'"$comune"'"' "$cartella"/"$comune".csv | tail -n +2 | tr "\n" " ")

echo "allegato" > "$cartella"/allegati.csv

for i in $pagine; do
    urlAllegati=$(curl -sL "$i" | pup "#container > div.wrapper > div.col1 > div.single_post > div.allegati > div.testoallegato > a attr{href}" | paste -s -d '|' | sed 's/ ,/,/g')
    echo $urlAllegati >>  "$cartella"/allegati.csv
done;

paste -d "," "$cartella"/"$comune"_temp.csv "$cartella"/allegati.csv > "$cartella"/"$comune".csv
