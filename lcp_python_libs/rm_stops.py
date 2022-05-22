from zoneinfo import InvalidTZPathWarning
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd
import pathlib
from LDistance import LDistance as ld


if __name__ == '__main__':
    # Creates file from frequency list
    fileTitle = 'en_50k.txt'
    filePath = pathlib.Path(__file__).parent / ogFileTitle
    fileFreqList = open(filePath)
    language = "English"
    nltk.download('stopwords')
    listStops = set(stopwords.words(language.lower()))
    listAllLines = fileFreqList.readlines()
    # listFirstThousand is the first thousand non-stopword entries in the file
    listFirstThousand = []
    # scrapes frequency list for first 1000 entries (word and frequency)
    intFreqIndex = 0
    count = 0
    intWordCount = 1000

    # checks if word is a stop word and adds to new file if not
    newTitle = language+'_rm_Stops.txt'
    with open (newTitle, 'w') as f:
        while count < intWordCount:
            word = re.split(" ", listAllLines[intFreqIndex])[0].lower()
            if word not in listStops:
                listFirstThousand.append(listAllLines[intFreqIndex].lower())
                f.write(listAllLines[intFreqIndex])
                count += 1
            intFreqIndex += 1