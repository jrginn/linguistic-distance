def csvFreqListLDistances(strSrcLangFile, strSrcLang, strTarLang, strSrcLangCode, strTarLangCode):
    #if __name__ == '__main__':
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