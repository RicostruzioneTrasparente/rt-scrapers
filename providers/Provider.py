import re, arrow

class Provider():

    input_format = ""
    output_format = "%a, %d %b %Y %H:%M:%S %z"
    tz = "Europe/Rome"
    language = "it"

    feed_base_url = "http://feeds.ricostruzionetrasparente.it/albi_pretori/"
    docs_base_url = "http://albopop.it/"
    specs_base_url = "http://albopop.it/specs/"

    def __init__(self):
        self.options = {}

    # Parse and format datetime strings
    def format_datetime(self, ar):
        if isinstance(ar,arrow.arrow.Arrow):
            return ar.strftime(self.output_format)
        elif isinstance(ar,str) and ar:
            return self.format_datetime(arrow.get(ar,self.input_format).replace(tzinfo=self.tz))
        else:
            return ""

    # Clean strings
    def clean_string(self, old_string):
        if not old_string:
            return ""
        new_string = old_string
        chars = ["\n","\t","\r"]
        for c in chars:
            new_string = new_string.replace(c," ")
        new_string = re.sub(r" {2,}", " ", new_string)
        return new_string.strip()

    # Public method called by scraper.py
    def scrape(self):
        return []
