# An example of provider definition

# Mandatory imports
from .Provider import Provider
from rfeed import *

# Optional imports
import requests, mimetypes, logging, re
logging.basicConfig(level=logging.DEBUG)
from bs4 import BeautifulSoup as bs

# Custom provider class inherit from the Provider one defined in providers/Provider.py file
#
# Inherited attributes:
# - output_format
# - tz
# - language
# - feed_base_url
# - docs_base_url
# - specs_base_url
# - options
#
# Inherited methods:
# - dt
#
# Specific methods to customize:
# - opts: using options from csv file properly
# - urls: extract single item urls from index page
# - item: extract and structure data from single item page
#
# WARNING: class name is also the value of provider column in elenco_albi.csv
#
class Task(Provider):

    # Mandatory attributes
    # Datetime format of scraped data
    input_format = "DD/MM/YYYY"

    # Optional attributes
    # ...

    # Transform and prepare options from CSV row (options column)
    def opts(self, opt):
        # From elenco_albi.csv -> options can be read custom options
        # Here you can manage them and store in the self.options dict
        self.options['index_url'] = opt
        return self # Mandatory for chaining

    # Scrape index page and return single item urls
    def urls(self):
        # From the index page you have to write here the scraping rules to fetch single page urls
        # You can return a list of urls (strings) or a generator with the yield operator
        index_page_url = self.options['index_url']
        index_page_response = requests.get(index_page_url)

        # Manage exceptions and return consistent values
        if index_page_response.status_code != 200:
            logging.warning("Index page %s unavailable!" % index_page_url)
            return []

        # Parsing with BeautifulSoup
        index_page_soup = bs(index_page_response.content,"lxml")
        logging.info("Scraping %s:" % index_page_url)

        index_table = index_page_soup.find("table")

        headers = [
            header.text.strip().strip(":")
            for header in index_table.find("tr").findAll("th")
        ]

        results = [
            {
                headers[i]: cell.text.strip()
                for i, cell in enumerate(row.findAll("td"))
            }
            for row in index_table.findAll("tr")[1:]
        ]

        self.options["index_table"] = {
            el["N.Registro"].replace("N.","").strip(): el
            for el in results
        }

        for a in index_table.findAll("a"):
            if a.get("href"):
                yield a.get("href").strip()

    # Scrape a single item page from its url and return structured data as Item() instance (from rfeed)
    def item(self,single_page_url):
        # From the url you can fetch the single item page and scrape data from it
        # You must return an Item() with structured data in it
        # Refer to Halley.py definition for more details
        single_page_response = requests.get(single_page_url)

        if single_page_response.status_code != 200:
            print("Single page %s unavailable!" % single_page_id)
            return None # None items are dropped in final feed

        single_page_soup = bs(single_page_response.content,"lxml")
        logging.debug("- Scraping %s" % single_page_url)

        single_page_table = single_page_soup.find("div", class_="info")

        description = single_page_table.find("div", class_="etichettalunga").text.strip()
        id = re.search("N. ([^ ]+)", description).group(1).strip()
        labels = [cell.text.strip().strip(":") for cell in single_page_table.findAll("div", class_="etichetta")]
        values = [cell.text.strip() for cell in single_page_table.findAll("div", class_="valore")]
        record = dict(zip(labels,values))

        if not self.options["index_table"].get(id):
            self.options["index_table"][id] = {}
        self.options["index_table"][id].update(record)
        document = self.options["index_table"][id]

        # Return scraping data as an Item() instance
        return Item(
            title = document["Titolo"],
            link = single_page_url,
            description = description,
            pubDate = self.dt(document.get("Esecutiva dal") or document.get("Data di pubblicazione") or document.get("Dal")),
            guid = Guid(single_page_url),
            categories = [
                c
                for c in [
                    Category(
                        domain = self.specs_base_url + "#" + "item-category-uid",
                        category = id
                    ),
                    Category(
                        domain = self.specs_base_url + "#" + "item-category-type",
                        category = document["Tipologia pubblicazione"]
                    ) if document.get("Tipologia pubblicazione") else None,
                    Category(
                        domain = self.specs_base_url + "#" + "item-category-pubStart",
                        category = self.dt(document.get("Dal") or document.get("Data di pubblicazione") or document.get("Esecutiva dal"))
                    ),
                    Category(
                        domain = self.specs_base_url + "#" + "item-category-pubEnd",
                        category = self.dt(document["Al"])
                    ) if document.get("Al") else None
                ]
                if c is not None
            ],
            enclosure = [
                Enclosure(
                    url = enclosure.find("a").get("href"),
                    length = 3000,
                    type = mimetypes.guess_type(enclosure.find("a").get("href"))[0] or "application/octet-stream"
                )
                for enclosure in single_page_soup.findAll("div", class_="testoallegato")
            ]
        )

    # Simple and generic wrapper around item() method if a list of urls is passed
    # Unavailable items are filtered out
    def items(self, single_page_urls):
        # Return value of urls() method is passed to items() method,
        # so you can manage here the scraping logic if all items are in the index page
        # and there are no single item pages to fetch
        for single_page_url in single_page_urls:
            item = self.item(single_page_url)
            if item:
                yield item

