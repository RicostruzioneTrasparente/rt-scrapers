# rt-scrapers
Curated list of sources for scrapers and related issue tracker. Multi-threading!

Contenuto:

- `sources.json`: tutti i feed di albopop relativi agli albi pretori scrapati e indicizzati;
- `elenco_albi.csv`: tutti gli albi pretori scrapati regolarmente;
- `scraper.py`: scraper universale per gli albi pretori;
- `test.py`: strumento di test dello scraper (output in console);
- `providers/`: regole di scraping per provider.

## Come proporre nuove fonti

Apri una issue [qui](https://github.com/RicostruzioneTrasparente/rt-scrapers/issues/new), indica nel titolo l'amministrazione pubblica e la sezione del sito che ti interessa monitorare (es. l'albo pretorio), seleziona l'etichetta "New source" e inserisci tutte le informazioni utili che già conosci. [Ecco le nuove fonti](https://github.com/RicostruzioneTrasparente/rt-scrapers/labels/new%20source) su cui stiamo lavorando.

## Come correggere / aggiornare una fonte

Apri una issue [qui](https://github.com/RicostruzioneTrasparente/rt-scrapers/issues/new), indica nel titolo la fonte che vuoi modificare o in cui hai trovato un errore, seleziona l'etichetta "Update" e inserisci la correzioni suggerita. [Ecco le modifiche in attesa](https://github.com/RicostruzioneTrasparente/rt-scrapers/labels/update) di essere applicate.

## Come sviluppare uno scraper

Individua una fonte ancora non monitorata (se c'è ha il campo `feed` vuoto, se non c'è suggeriscine l'aggiunta) e apri una issue [qui](https://github.com/RicostruzioneTrasparente/rt-scrapers/issues/new) indicandola nel titolo e proponendoti come maintainer.

Sviluppa il tuo scraper in totale libertà, se hai bisogno di chiarimenti usa la issue dedicata alla tua fonte, aggiungendo l'etichetta "help wanted". Assicurati di aver letto interamente le [specifiche del feed RSS](http://albopop.it/specs/) prima di rilasciare lo scraper. Se vuoi usare il framework qui proposto, scrivi e testa le regole di scraping relative al tuo provider nella cartella `providers/` (leggi i commenti nel [file `Halley.py`](https://github.com/RicostruzioneTrasparente/rt-scrapers/providers/blob/develop/Halley.py)).

Quando il tuo scraper è pronto segnalalo nella issue precedentemente aperta indicando l'url del feed, l'url del repository dello scraper e i tuoi dati di maintainer: nome, indirizzo mail, sito web. [Ecco gli scraper](https://github.com/RicostruzioneTrasparente/rt-scrapers/labels/new%20scraper) in sviluppo.

Non appena il file sources.json sarà aggiornato con il tuo nuovo feed i prodotti del lavoro del tuo scraper cominceranno a essere indicizzati ed entreranno a far parte della piattaforma di monitoraggio. In caso di anomalie o malfunzionamenti sarai contattato alla mail fornita.

## Domande, curiosità o dubbi?

Apri pure una issue [qui](https://github.com/RicostruzioneTrasparente/rt-scrapers/issues/new) usando l'etichetta "Question", queste sono le domande a cui [stiamo rispondendo](https://github.com/RicostruzioneTrasparente/rt-scrapers/labels/question) e a cui [abbiamo risposto](https://github.com/RicostruzioneTrasparente/rt-scrapers/issues?utf8=%E2%9C%93&q=is%3Aclose%20label%3Aquestion%20).

## Ulteriori informazioni

Progetto "Ricostruzione Trasparente": http://www.ricostruzionetrasparente.it/.
