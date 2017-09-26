# An example of provider definition

# Mandatory imports
from .Provider import Provider
from rfeed import *

# Optional imports
import requests, mimetypes, logging
logging.basicConfig(level=logging.INFO)
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
class Sample(Provider):

    # Mandatory attributes
    # Datetime format of scraped data
    input_format = "DD/MM/YYYY"

    # Optional attributes
    # ...

    # Transform and prepare options from CSV row (options column)
    def opts(self, opt):
        # From elenco_albi.csv -> options can be read custom options
        # Here you can manage them and store in the self.options dict
        return self # Mandatory for chaining

    # Scrape index page and return single item urls
    def urls(self):
        # From the index page you have to write here the scraping rules to fetch single page urls
        # You can return a list of urls (strings) or a generator with the yield operator
        pass

    # Scrape a single item page from its url and return structured data as Item() instance (from rfeed)
    def item(self,single_page_url):
        # From the url you can fetch the single item page and scrape data from it
        # You must return an Item() with structured data in it
        # Refer to Halley.py definition for more details
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

    # Public method called by scraper.py
    def scrape(self):
        return self.items(self.urls())

