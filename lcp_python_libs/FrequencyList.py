from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from lcp_python_libs.LDistance import LDistance

"""
***************************
Class notes:
***************************
This class contains all of the methods used to calculate the Levenshtein distance for frequency lists
"""
class FrequencyList():
    
    '''
    Inputs: A string "strSrcLangFile" which is the file path of the frequency list in the source language,
            a string "strSrcLang" which is the source language, a string "strTarLang" which is the target language,
            a string "strSrcLangCode" which is the two letter code for the source language, and
            a string "strTarLangCode" which is the two letter code for the target langauge
    Outputs: Nothing returned but saves a csv of original word, translation, and Ldistance columns
    Utility: Calculates Ldistances for a frequency list
    '''
    def freqListLDistances(strSrcLangFile, strSrcLang, strTarLang, strSrcLangCode, strTarLangCode):
        # Creates file from frequency list
        fileFreqList = open(strSrcLangFile, encoding="utf-8")
        listStops = stopwords.words(strSrcLang)
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
        listSrcTarWordLists = []
        for wordA in listThousandWords:
            listSrcTarWordLists.append([wordA, GoogleTranslator(source=strSrcLangCode, target=strTarLangCode).translate(text=wordA).lower()])
        listLDists = []
        for i in range(len(listSrcTarWordLists)):
            strSpaWord = listSrcTarWordLists[i][0].lower()
            strEngWord = listSrcTarWordLists[i][1].lower()
            listLDists.append(LDistance.floatLDistance(LDistance, stringDevowelize(strSpaWord), stringDevowelize(strEngWord)))
        
        # creates dataframe with columns: original word, translation, and l-distance
        df = pd.DataFrame(listSrcTarWordLists, columns=[strSrcLang, strTarLang])
        df["Distances"] = listLDists
        print(df)
        csvFileName = ""
        csvFileName += strSrcLang[0:3]
        csvFileName += strTarLang[0:3]
        csvFileName += "1.csv"

        df.to_csv(csvFileName, encoding='utf-8-sig')

    '''
    Inputs: A list of Ldistance averages "listRatioValues", a list of language names "listLangNames", and
            a filepath for the saved figure "strFileSaveName"
    Outputs: Returns a string if there is a mismatch in data size, otherwise saves a heatmap
    Utility: Creates a heatmap showing average Ldistance across provided languages
    '''
    def snsCreateHeatMap(listRatioValues, listLangNames, strFileSaveName):
        intTableLen = pow(len(listLangNames), 2)

        if ((len(listRatioValues[0]) * len(listRatioValues)) != intTableLen):
            return "Incorrect number of data values, please edit listRatioValues."

        listData = listRatioValues
        listRows = listLangNames
        listCols = listLangNames

        df = pd.DataFrame(listData, index=listRows, columns=listCols)
        s = sns.heatmap(df.head(), annot=True, cmap='YlOrRd', cbar=True,fmt='.4f')
        plt.savefig(strFileSaveName)
        s.set(xlabel='Source Language', ylabel='Target Language')

