from zoneinfo import InvalidTZPathWarning
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd
import pathlib
import codecs
from VSLDistance import LDistance as ld


if __name__ == '__main__':
    # Creates file from frequency list
    filePath = 'es_50k.txt'
    fileFreqList = open(filePath, encoding="utf-8")
    language = "Spanish"
    nltk.download('stopwords')
    listStops = set(stopwords.words(language.lower()))
    listAllLines = fileFreqList.readlines()
    # listFirstThousand is the first thousand non-stopword entries in the file
    listFirstThousand = []
    # scrapes frequency list for first 1000 entries (word and frequency)
    intFreqIndex = 0
    count = 0
    intWordCount = 2000 

    # checks if word is a stop word and adds to new file if not
    newTitle = language+str(intWordCount)+'_rm_Stops.txt'
    with codecs.open (newTitle, 'w', "utf-8") as f:
        while count < intWordCount:
            word = re.split(" ", listAllLines[intFreqIndex])[0].lower()
            if word not in listStops:
                listFirstThousand.append(listAllLines[intFreqIndex].lower())
                f.write(listAllLines[intFreqIndex])
                count += 1
            intFreqIndex += 1