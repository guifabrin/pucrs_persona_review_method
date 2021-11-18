import json
import requests as requests
from concurrent.futures import ThreadPoolExecutor
from os import listdir
from os.path import isfile, join
import unicodedata
import re
from os.path import exists


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

scrapper_path = "scrappers\\"
onlyfiles = [f for f in listdir(scrapper_path) if isfile(join(scrapper_path, f)) and f.endswith(".json")]

pdfs = []
for file in onlyfiles:
    f = open(scrapper_path + file, encoding="utf-8")
    data = json.load(f)
    for item in data:
        pdfs.append(item)
    f.close()


def download(url, filename):
    print("Downloading ", filename)
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)


with ThreadPoolExecutor() as executor:
    futures = []
    for pdf in pdfs:
        try:
            filename = "downloads\\" + slugify(pdf['name'].replace('.pdf', '')) + '.pdf'
            if not exists(filename):
                futures.append(executor.submit(download, url=pdf['href'], filename=filename))
        except:
            print("Error ", pdf['name'])
