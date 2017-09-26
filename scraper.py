import sys, csv, arrow
from providers import *
from rfeed import *

if len(sys.argv) > 2:
    csv_filename = sys.argv[1].strip()
    download_dir = sys.argv[2].strip()
else:
    print("Usage: python %s %s %s" % (
        sys.argv[0],
        "[CSV filename]",
        "[download directory]"
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
now = arrow.now()

with open(sys.argv[1]) as f:

    reader = csv.DictReader(f)
    for line in reader:

        p = providers.get(line["provider"], line["options"])

        items = p.scrape()

        feed = Feed(
            title = "AlboPOP - %s - %s" % ( line["channel-category-type"] , line["channel-category-name"] ),
            link = p.feed_base_url + line["feed_name"],
            description = "*non ufficiale* RSS feed dell'Albo Pretorio del %s" % line["channel-category-name"],
            language = p.language,
            pubDate = p.format_datetime(now),
            webMaster = line["webmaster"],
            docs = p.docs_base_url + line["docs"].lower(),
            copyright = "Copyright %d %s" % ( now.year , line["channel-category-name"] ),
            categories = [
                Category( domain = p.specs_base_url + "#" + l[0], category = l[1] )
                for l in line.items() if l[0].startswith("channel-category-") and l[1]
            ],
            items = [item for item in items]
        )

        with open(download_dir + "/%s.xml" % line["feed_name"].split(".")[0],"w") as f:
            f.write(feed.rss())

