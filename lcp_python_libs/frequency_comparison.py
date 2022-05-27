from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
import re
import pandas as pd
from LDistance import LDistance as ld

#takes a string argument and returns the string without the vowels
def stringDevowelize(strArg):
    strRet = ""
    listVowels = ['a', 'e', 'i', 'o', 'u']
    for n in strArg:
        if n not in listVowels:
            strRet += n
    return strRet

if __name__ == '__main__':
    # Creates file from frequency list
    fileFreqList = open("fr_50k.txt", encoding='utf-8')
    listStops = stopwords.words("french")
    listAllLines = fileFreqList.readlines()
    # listFirstThousand is the first thousand non-stopword entries in the file
    listFirstThousand = []
    # scrapes frequency list for first 1000 entries (word and frequency) not in stopwords
    intFreqIndex = 0
    while len(listFirstThousand) < 1000:
        # checks if word is a stop word and adds if it is not
        if re.split(" ", listAllLines[intFreqIndex])[0].lower() not in listStops:
            listFirstThousand.append(listAllLines[intFreqIndex].lower())
        intFreqIndex += 1
    listThousandWords = []
    # removes frequency from entries and adds just the word to listThousandWords
    for stringText in listFirstThousand:
        listLine = re.split(" ", stringText)
        listThousandWords.append(listLine[0])
    # list of length 2 lists with the words from language A and their translations into language B
    listFraSpaWordLists = []
    for wordA in listThousandWords:
        listFraSpaWordLists.append([wordA, GoogleTranslator(source='fr', target='es').translate(text=wordA).lower()])
    listLDists = []
    for i in range(len(listFraSpaWordLists)):
        strFraWord = listFraSpaWordLists[i][0].lower()
        strSpaWord = listFraSpaWordLists[i][1].lower()
        listLDists.append(ld.floatLDistance(ld, stringDevowelize(strFraWord), stringDevowelize(strSpaWord)))
    # creates dataframe with columns: original word, translation, and l-distance
    df = pd.DataFrame(listFraSpaWordLists, columns=["French", "Spanish"])
    df["Distances"] = listLDists
    print(df)
    df.to_csv("fraSpa1.csv", encoding='utf-8-sig')