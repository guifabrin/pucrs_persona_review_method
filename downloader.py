import json
import requests as requests
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


def download(url, filename):
    print("Downloading ", filename)
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)


scrapper_path = "scrappers\\"
onlyfiles = [f for f in listdir(scrapper_path) if isfile(join(scrapper_path, f)) and f.endswith(".json")]

pdfs = []
for file in onlyfiles:
    f = open(scrapper_path + file, encoding="utf-8")
    data = json.load(f)
    for item in data:
        pdfs.append(item)
    f.close()

unique_pdfs = []
unique_names = []

for pdf in pdfs:
    if pdf['title'] in unique_names:
        continue
    unique_pdfs.append(pdf)
    unique_names.append(pdf['title'])

error = 0
skipped = 0
downloaded = 0
for pdf in unique_pdfs:
    try:
        filename = "downloads\\" + slugify(pdf['title'].replace('[PDF]', '')) + '.pdf'
        if exists(filename):
            downloaded += 1
            continue
        if pdf['year'] is not None and pdf['year'] >= 2019:
            download(url=pdf['url'], filename=filename)
            downloaded += 1
        else:
            skipped += 1
    except:
        error += 1
        print("Error ", pdf['title'])
print(downloaded, skipped, error, downloaded + skipped + error)
