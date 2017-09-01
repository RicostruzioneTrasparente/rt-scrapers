#!/bin/bash

curl -sL "http://www.comune.acquacanina.mc.it/albo-pretorio/" | scrape -be "#container > div.wrapper > div.col1 > div.single_post > table > tr" | xml2json | jq '[[.html.body.tr[] | {registro:.td[0].small."$t",tipologia:.td[1].small."$t",titolo:.td[2].small.a."$t",stato:.td[3].small."$t",dal:.td[4].small."$t",al:.td[5].small."$t",URI:.td[2].small.a.href}] | .[] | select(.registro != null)]' | in2csv --no-inference -f json > 43001.csv

curl -sL "http://www.comune.acquacanina.mc.it/atti-generali-cms/regolamento-esecuzione-lavori-e-forniture-in-ecoinomia/" | pup "#container > div.wrapper > div.col1 > div.single_post > div.allegati > div.testoallegato > a attr{href}"