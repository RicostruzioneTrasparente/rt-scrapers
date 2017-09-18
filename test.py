import sys, csv
from providers import *

if len(sys.argv) > 1:
    csv_filename = sys.argv[1].strip()
else:
    print("Usage: python %s %s" % (
        sys.argv[0],
        "[CSV filename]"
    ))
    exit()

class Providers():

    def __init__(self):
        self.providers = {}

    def load(self, name):
        if name in globals():
            self.providers[name] = getattr(globals()[name],name)()

    def get(self, name, opt):
        if name not in self.providers:
            self.load(name)
        return self.providers[name].opts(opt)

providers = Providers()

with open(sys.argv[1]) as f:

    reader = csv.DictReader(f)
    for line in reader:

        p = providers.get(line["provider"], line["options"])
        urls = p.urls()
        print([url for url in urls])
        items = p.items(urls)
        print([item for item in items])

