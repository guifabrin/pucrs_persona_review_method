from os import listdir
from os.path import isfile, join
from langdetect import detect

path = "processing\\"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".txt")]
languages = []
partial_size = 50
for file in onlyfiles:
    f = open(path + file, "r", encoding="utf-8")
    print(file)
    words = f.read().split(' ')
    len_words = len(words)
    index = 0
    checked_languages = []
    while index < len_words:
        partial = ''
        while len(partial) < partial_size:
            if len_words == index + 1:
                break
            partial += words[index].replace(".", "") + " "
            index += 1
        try:
            checked_languages.append(detect(partial))
            if len_words == index + 1:
                break
        except:
            pass
    language = max(set(checked_languages), key=checked_languages.count)
    print(language)
    if not language in languages:
        languages.append(language)
    f.close()

print(languages)
