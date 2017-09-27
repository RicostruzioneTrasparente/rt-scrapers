import sys, csv, logging, arrow
from providers import providers
from rfeed import *
from threading import Thread
from queue import Queue, Empty

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

now = arrow.now()
q = Queue()

def spider(q):

    while not q.empty():

        try:
            line = q.get(timeout = 1)
        except Empty:
            break

        try:
            p = getattr(providers, line["provider"])()
            p.opts(line["options"])
        except AttributeError as e:
            logging.warning("Requested provider not found: %s" % line["provider"])
            q.task_done()
            continue

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

        q.task_done()

with open(sys.argv[1]) as f:
    reader = csv.DictReader(f)
    for line in reader:
        q.put(line)

num_spiders = 10
spiders = []

logging.info("Starting scraper with %d spiders on %d sources..." % ( num_spiders , q.qsize() ))

for n in range(num_spiders):
    t = Thread(
        name = "Spider #%d" % n,
        target = spider,
        args = (q,)
    )
    spiders.append(t)
    t.start()

for t in spiders:
    t.join()

logging.info("... done!")

