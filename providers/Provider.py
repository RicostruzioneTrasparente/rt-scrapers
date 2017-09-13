import arrow

class Provider():

    input_format = ""
    output_format = "%a, %d %b %Y %H:%M:%S %z"
    tz = "Europe/Rome"
    language = "it"

    feed_base_url = "http://feeds.ricostruzionetrasparente.it/albi_pretori/"
    docs_base_url = "http://albopop.it/"
    specs_base_url = "http://albopop.it/specs/"

    options = {}

    def dt(self, ar):
        if isinstance(ar,arrow.arrow.Arrow):
            return ar.strftime(self.output_format)
        elif isinstance(ar,str) and ar:
            return self.dt(arrow.get(ar,self.input_format).replace(tzinfo=self.tz))
        else:
            return ""

