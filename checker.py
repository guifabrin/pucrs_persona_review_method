import re

import PyPDF2
import os
import pdfplumber
import gc

numbers_dictionary = [
    ["developed", "personas "],
    ["developed", "persona "],

    ["created", "personas "],
    ["created", "persona "],

    ["criado", "persona "],
    ["criado", "personas "],

    ["creado", "persona"],
    ["creado", "personas"],

    ["entwickelt", "personen"],
    ["entwickelt", "persona"],

    ["erstellt", "personen"],
    ["erstellt", "persona"],
]


def check(filename):
    with open(filename, 'rb') as f:
        try:
            pdf = PyPDF2.PdfFileReader(f)
            info = pdf.getDocumentInfo()
            return True if info else False
        except:
            return False


def get_between(string, init, end):
    matches = re.findall(r'{}.+?{}'.format(init, end), string)
    result = []
    for match in matches:
        result.append(match.replace(init, '').replace(end, ''))
    return result


def tests(text):
    for item in numbers_dictionary:
        matches = get_between(text, item[0], item[1])
        for match in matches:
            words = match.split(' ')
            if len(words) < 10:
                return True
        matches = get_between(text, item[1], item[0])
        for match in matches:
            words = match.split(' ')
            if len(words) < 10:
                return True
    return False


def process(filename, text_filename):
    pdf = pdfplumber.open(filename)
    if len(pdf.pages) > 50:
        pdf.close()
        return False
    text = ''
    if os.path.exists(text_filename):
        f = open(text_filename, "r", encoding="utf-8")
        text = f.read()
        f.close()
    else:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('- ', '') + " "
        text = re.sub(' +', ' ', text)
        f = open(text_filename, "a+", encoding="utf-8")
        f.write(text)
        f.close()
    pdf.close()
    return tests(text)


def search(path="downloads\\", move=False, skip_processed=False):
    contains = 0
    not_contains = 0
    with_error = 0
    files = os.listdir(path)
    for f in files:
        gc.collect()
        if not f.endswith('.pdf'):
            continue
        filename = os.path.join(path, f)
        try:
            text_filename = os.path.join("processing\\", f)+".txt"
            if skip_processed:
                if os.path.exists(text_filename):
                    continue
            if check(filename):
                print("[" + filename + "] is valid.")
                print("[" + filename + "] processing.")
                if process(filename, text_filename):
                    contains += 1
                    print("[" + filename + "] contain regex.")
                    if move:
                        os.rename(filename, path+"maybe\\" + f)
                else:
                    not_contains += 1
                    print("[" + filename + "] does not contain requirements.")
                    if move:
                        os.rename(filename, path+"not_contains\\" + f)
            else:
                os.rename(filename, path+"error\\" + f)
        except Exception as e:
            print('Error', e)
            os.rename(filename, path+"error\\" + f)
            with_error+=1
        print("Results: {} contains, {} not contains, {} with error".format(contains, not_contains, with_error))


if __name__ == "__main__":
    search(move=True)
    #search("downloads\\maybe\\")
