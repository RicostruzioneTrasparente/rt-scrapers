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
    input_format = "D/M/YYYY"

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

        index_table = index_page_soup.find("div", class_="single_post").find("table")

        if not index_table:
            logging.warning("Table in index page %s not found!" % index_page_url)
            return []

        headers = [
            header.text.strip().strip(":")
            for header in index_table.find("tr").find_all("th")
        ]

        results = [
            {
                headers[i]: cell.text.strip()
                for i, cell in enumerate(row.find_all("td"))
            }
            for row in index_table.find_all("tr")[1:]
        ]

        self.options["index_items"] = {
            el["N.Registro"].replace("N.","").strip(): el
            for el in results
        }

        for a in index_table.find_all("a"):
            if a.get("href"):
                yield a.get("href").strip()

    # Scrape a single item page from its url and return structured data as Item() instance (from rfeed)
    def item(self,single_page_url):
        pass

    # Simple and generic wrapper around item() method if a list of urls is passed
    # Unavailable items are filtered out
    def items(self, single_page_urls):
        # Return value of urls() method is passed to items() method,
        # so you can manage here the scraping logic if all items are in the index page
        # and there are no single item pages to fetch
        for single_page_url in single_page_urls:
            try:
                item = self.item(single_page_url)
                if item:
                    yield item
            except Exception as e:
                logging.warning("Error scraping page %s: %s" % ( single_page_url , e ))
                continue

