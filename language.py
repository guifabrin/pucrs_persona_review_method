import concurrent
import os
import random
from concurrent.futures import ThreadPoolExecutor
from os import listdir
from os.path import isfile, join, exists
from langdetect import detect

path = "downloads\\maybe\\"
processing_path = "processing\\"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith(".pdf")]
partial_size = 50

random.shuffle(onlyfiles)

for file in onlyfiles:
    f = open(processing_path + file + ".txt", "r", encoding="utf-8")
    words = f.read().split(' ')
    len_words = len(words)
    index = 0
    checked_languages = []
    while index < len_words:
        print(file, index, len_words)
        partial = ''
        while len(partial) < partial_size:
            try:
                partial += words[index].replace(".", "") + " "
                index += 1
            except:
                break
        try:
            checked_languages.append(detect(partial))
            if len_words == index + 1:
                break
        except:
            pass
    language = max(set(checked_languages), key=checked_languages.count)
    f.close()
    os.makedirs(path+"\\"+language+"\\", exist_ok=True)
    os.rename(path+file, path+"\\"+language+"\\"+file)
    print([file, language])
