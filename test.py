import sys, csv
from providers import providers

if len(sys.argv) > 1:
    csv_filename = sys.argv[1].strip()
else:
    print("Usage: python %s %s" % (
        sys.argv[0],
        "[CSV filename]"
    ))
    exit()

with open(sys.argv[1]) as f:

    reader = csv.DictReader(f)
    for line in reader:

        try:
            p = getattr(providers, line["provider"])()
            p.opts(line["options"])
        except AttributeError as e:
            logging.warning("Requested provider not found: %s" % line["provider"])
            q.task_done()
            continue

        urls = [url for url in p.urls()]
        print(urls)
        items = [item for item in p.items(urls)]
        print(items)

