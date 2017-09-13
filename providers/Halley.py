# Halley provider definition

# Mandatory imports
from .Provider import Provider
from rfeed import *

# Optional imports
import requests, mimetypes, logging
logging.basicConfig(level=logging.INFO)
from bs4 import BeautifulSoup as bs

# Halley provider class inherit from the Provider one defined in providers/Provider.py file
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
class Halley(Provider):

    # Mandatory attributes
    input_format = "DD/MM/YYYY"

    # Optional attributes
    # ...

    # Transform and prepare options from CSV row (options column)
    def opts(self, opt):
        self.options["base_url"] = "http://halleyweb.com/%s/mc/" % opt
        return self # Mandatory for chaining

    # Scrape index page and return single item urls
    def urls(self):

        index_page_url = self.options["base_url"] + "/mc_gridev_messi_datigrid.php"
        index_page_response = requests.get(index_page_url)

        # Manage exceptions and return consistent values
        if index_page_response.status_code != 200:
            logging.warning("Index page %s unavailable!" % index_page_url)
            return []

        # Parsing with BeautifulSoup
        index_page_soup = bs(index_page_response.content,"lxml")
        logging.info("Scraping %s:" % index_page_url)

        # Very simple scraping of single item urls
        for row in index_page_soup.findAll("row"):

            single_page_id = row['id'].strip()
            single_page_url =  self.options["base_url"] + "/mc_gridev_dettaglio.php?id_pubbl=%s" % single_page_id

            yield single_page_url

    # Scrape a single item page from its url and return structured data as Item() instance (from rfeed)
    def item(self,single_page_url):

        single_page_response = requests.get(single_page_url)

        if single_page_response.status_code != 200:
            print("Single page %s unavailable!" % single_page_id)
            return None # None items are dropped in final feed

        single_page_soup = bs(single_page_response.content,"lxml")
        logging.info("- Scraping %s" % single_page_url)

        ### MAIN SCRAPING LOGIC ###
        contents = []
        for cell in single_page_soup.select("td"):
            if cell.findAll('a'):
                contents.append([])
                for a in cell.findAll('a'):
                    contents[-1].append({
                        "content": a.text.strip(),
                        "href": self.options["base_url"] + a['onclick'].replace("window.open('","").replace("');","").strip()
                    })
            else:
                contents.append(cell.text.strip().strip(':'))

        document = dict([tuple(contents[i:i+2]) for i in range(0,len(contents),2)])

        document["Documento"] = document["Documento"] if "Documento" in document and isinstance(document["Documento"],list) else []
        document["Allegati"] = document["Allegati"] if "Allegati" in document and isinstance(document["Allegati"],list) else []
        ### END SCRAPING LOGIC ###

        # Return scraping data as an Item() instance
        return Item(
            title = document["Oggetto Atto"],
            link = single_page_url,
            description = document["Oggetto Atto"],
            pubDate = self.dt(document["Data Atto"] or document["Data Inizio Pubblicazione"]),
            guid = Guid(single_page_url),
            categories = [
                c
                for c in [
                    Category(
                        domain = self.specs_base_url + "#" + "item-category-uid",
                        category = "%s/%s" % (document["Anno di Pubblicazione"], document["Numero Pubblicazione"])
                    ),
                    Category(
                        domain = self.specs_base_url + "#" + "item-category-type",
                        category = document["Tipo Atto"]
                    ) if document["Tipo Atto"] else None,
                    Category(
                        domain = self.specs_base_url + "#" + "item-category-pubStart",
                        category = self.dt(document["Data Inizio Pubblicazione"] or document["Data Atto"])
                    ),
                    Category(
                        domain = self.specs_base_url + "#" + "item-category-pubEnd",
                        category = self.dt(document["Data Fine Pubblicazione"])
                    ) if document["Data Fine Pubblicazione"] else None,
                    Category(
                        domain = self.specs_base_url + "#" + "item-category-unit",
                        category = document["Mittente"]
                    ) if document["Mittente"] else None
                ]
                if c is not None
            ],
            enclosure = [
                Enclosure(
                    url = enclosure["href"],
                    length = 3000,
                    type = mimetypes.guess_type(enclosure["content"])[0] or "application/octet-stream"
                )
                for enclosure in document["Documento"] + document["Allegati"]
            ]
        )

    # Simple and generic wrapper around item() method if a list of urls is passed
    # Unavailable items are filtered out
    def items(self, single_page_urls):
        for single_page_url in single_page_urls:
            item = self.item(single_page_url)
            if item:
                yield item

