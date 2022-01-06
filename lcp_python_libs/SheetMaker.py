import numpy as np
import pandas as pd
import time
import os
from deep_translator import GoogleTranslator

from lcp_python_libs.Parser import Parser

"""
***************************
Class notes:
***************************
This class wraps words.
Utility: The class allows individual words to maintain their index within a list, even if the 
size of the list changes. This is important in alignments, as the size of the stored amount of words
changes, but the words need to maintain their indices for comparison using Levenshtein, since the indices map back
to alignments.
"""
class WordWrapper():

    def __init__(self,word,index):
        self._word = str(word).lower()
        self._index = index
    
"""
***************************
Class notes:
***************************
This class is an Exception that is used to quickly get out of loops. Think of it similar to an unconditional
jump in MIPS assembly.
"""
class GetOutOfLoop(Exception):
    pass

"""
***************************
Class notes:
***************************
This class creates the automatically generated alignment csvs.
"""
class SheetMaker():

	def __init__(self):
		self._parser = Parser()

	def listCreateWordWrapperList(self,listLangList):
		"""
		Inputs:
		list "listLangList"
		Outputs:
		list
		Utility:

		This function wraps words found in a list "listLangList" with the WordWrapper class.
		This is used for "dfGenerateAlignments". 
		Arguments: a list of words in a language. Output: a list of WordWrapper classes.
		Note that this also checks if a word is np.nan. If so, it will not append it.
		"""
		ret = []
		for i, word in enumerate(listLangList):
			if type(word) != float:
				ret.append(WordWrapper(word,i))
				
		return ret

	def boolCheckBounds(self,intIndex,intStep,listListToCheck):
		"""
		Inputs:
		int "intIndex", int "intStep", list "listListToCheck"
		Outputs:
		str
		Utility:
		This function checks if an selected index "intIndex" is within "intStep" of a list "listListToCheck".

		For instance, if the function returns "both", then i-step, i+step are within 0 to 
		the length of the list, thus within "both" upper and lower bounds.
		Similarly, "lower" is for within a lower bound, or i-step,i is between 0 and the length,
		"upper" is for within upper bound, or i,i+step is between 0 and the length.
		"""
		# first check both
		if (intIndex-intStep) > 0 and (intIndex+intStep) < len(listListToCheck):
			return "both"
		# check lower
		elif (intIndex-intStep) > 0 and intIndex < len(listListToCheck):
			return "lower"
		# check upper
		elif intIndex > 0 and intIndex + intStep < len(listListToCheck):
			return "upper"

	def boolCheckEqualWordWrappers(self,intI,intJ,listLangAWrappers,listLangBWrappers):
		"""
		Inputs:
		int "intI", int "intJ", list "listLangAWrappers", list "listLangBWrappers"
		Outputs:
		str
		Utility:
		This function takes in two lists of word wrappers, and checks equality between them.
		If l1_word_wrappers[i]._word == l2_word_wrappers[j]._word, the function returns "equal".
		Else, return "unequal".
		If the word is within the other word, it returns "in". Else, it again returns "unequal".
		"""
		word1_str = listLangAWrappers[intI]._word
		word2_str = listLangBWrappers[intJ]._word
		if word1_str == word2_str:
			return "equal"
		elif word1_str in word2_str or word2_str in word1_str:
			return "in"
		else:
			return "unequal"

	def strCreateAlignmentStr(self,intI,intJ,intCounter,strMarker):
		"""
		Inputs:
		int "intI", int "intJ", int "intCounter", str "strMarker"
		Outputs:
		str
		Utility:
		NOTE: BARS DELIM BETWEEN 2 LANGS, COMMAS BETWEEN WORDS OF SAME LANG!

		This function returns an alignment str that is inputted into the alignment df.
		i,j are the indices that will be shown in the alignment. 
		The counter is to determine the number of "marker" displayed.

		Ie: create_align_str(1,2,4,"*") returns:
		**** 1 2
		"""
		if strMarker == "*":
			# "*" denotes additional steps, ie
			# 2 stars means 2 additional steps.
			# If step = 5, 2 stars means 5 + 2(5) = 15 steps.
			return "{} {}|{}".format("*"*intCounter,intI,intJ)
		elif strMarker == "#":
		# "#" means "within word". This is more often risky, so always mark.
		# Even if within the original step count, mark it (why count + 1).
			return "{} {}|{}".format("#"*(intCounter+1),intI,intJ)
		
	def dfGenerateAlignments(self,strLangA,strLangB,intStep,df):
		"""
		Inputs:
		string "strLangA", string "strLangB", int "intStep", pandas dataframe "df"
		Outputs:
		pandas dataframe
		Utility:
		"""
		"""
		This function takes in two languages to be aligned, a intStep, and the dataframe of the 
		two languages. The "intStep" is the number of words near a word, up and down. For instance,
		if aligning a word at index 6, a intStep of 5 would mean to check either 5 above and below,
		just 5 above, or just 5 below. The intStep gets incremented by itself through every run.
		The alignments terminate when the intStep is greater than the length of either language's list of
		words. The "df" is the dataframe of the alignments, created by "create_align_df".
		"""
		dfReg = df.copy()
		# store words as WordWrappers
		listLangAWrappers = self.listCreateWordWrapperList(df[strLangA + "_eng"])
		listLangBWrappers = self.listCreateWordWrapperList(df[strLangB + "_eng"])
		
		# sentinel value
		boolWithinBounds = True
		
		# keep track of current intStep
		intCurrStep = intStep
		# keep track of runs
		counter = 0
		
		while(boolWithinBounds):
			# halt condition: if current intStep greater than length of lists
			if intCurrStep > len(listLangAWrappers) or intCurrStep > len(listLangBWrappers):
				boolWithinBounds = False
				break
			try:
				for i in range(len(listLangAWrappers)):
					if self.boolCheckBounds(i,intCurrStep,listLangAWrappers) == "both" and self.boolCheckBounds(i,intCurrStep,listLangBWrappers) == "both":
						# can safely go both lower and uppper
						for j in range((i-intCurrStep),(i+intCurrStep)):
							if self.boolCheckEqualWordWrappers(i,j,listLangAWrappers,listLangBWrappers) == "equal":
                                                            # words are a direct match
								alignment = self.strCreateAlignmentStr(listLangAWrappers[i]._index,listLangBWrappers[j]._index,counter,"*")
								dfReg.loc[listLangAWrappers[i]._index,"alignment"] = alignment
								# remove
								listLangBWrappers.pop(j)
								listLangAWrappers.pop(i)
								raise GetOutOfLoop
							# method 2: in -- change to "#"'
							elif self.boolCheckEqualWordWrappers(i,j,listLangAWrappers,listLangBWrappers) == "in":
                                                            # word1 is within word2
								alignment = self.strCreateAlignmentStr(listLangAWrappers[i]._index,listLangBWrappers[j]._index,counter,"#")
								dfReg.loc[listLangAWrappers[i]._index,"alignment"] = alignment
								# remove
								listLangBWrappers.pop(j)
								listLangAWrappers.pop(i)
								raise GetOutOfLoop
					elif self.boolCheckBounds(i,intCurrStep,listLangAWrappers) == "lower" and self.boolCheckBounds(i,intCurrStep,listLangBWrappers) == "lower":
						# can safely check lower bounds
						for j in range((i-intCurrStep),i):
							if self.boolCheckEqualWordWrappers(i,j,listLangAWrappers,listLangBWrappers) == "equal":
                                                            # direct match
								alignment = self.strCreateAlignmentStr(listLangAWrappers[i]._index,listLangBWrappers[j]._index,counter,"*")
								dfReg.loc[listLangAWrappers[i]._index,"alignment"] = alignment
								# remove
								listLangBWrappers.pop(j)
								listLangAWrappers.pop(i)
								raise GetOutOfLoop
							# method 2: in
							elif self.boolCheckEqualWordWrappers(i,j,listLangAWrappers,listLangBWrappers) == "in":
                                                            # word1 in word2
								alignment = self.strCreateAlignmentStr(listLangAWrappers[i]._index,listLangBWrappers[j]._index,counter,"#")
								dfReg.loc[listLangAWrappers[i]._index,"alignment"] = alignment
								# remove
								listLangBWrappers.pop(j)
								listLangAWrappers.pop(i)
								raise GetOutOfLoop

					elif self.boolCheckBounds(i,intCurrStep,listLangAWrappers) == "upper" and self.boolCheckBounds(i,intCurrStep,listLangBWrappers) == "upper":
						# can safely check upper bounds
						for j in range(i,(i+intCurrStep)):
							if self.boolCheckEqualWordWrappers(i,j,listLangAWrappers,listLangBWrappers) == "equal":
								alignment = self.strCreateAlignmentStr(listLangAWrappers[i]._index,listLangBWrappers[j]._index,counter,"*")
								dfReg.loc[listLangAWrappers[i]._index,"alignment"] = alignment
								# remove
								listLangBWrappers.pop(j)
								listLangAWrappers.pop(i)
								raise GetOutOfLoop
							# method 2: in
							elif self.boolCheckEqualWordWrappers(i,j,listLangAWrappers,listLangBWrappers) == "in":
								alignment = self.strCreateAlignmentStr(listLangAWrappers[i]._index,listLangBWrappers[j]._index,counter,"#")
								dfReg.loc[listLangAWrappers[i]._index,"alignment"] = alignment
								# remove
								listLangBWrappers.pop(j)
								listLangAWrappers.pop(i)
								raise GetOutOfLoop
				counter += 1
				intCurrStep += intStep
				
			except GetOutOfLoop:
                            # GetOutOfLoop is designed to be a quick means of leaving the loop and going back to the
                            # original while loop
				pass

		return dfReg

	def listGetLangTransToEng(self, listForeignWordList,strLangName):
		"""
		Inputs:
		list of strings "listForeignWordList", string "strLangName"
		Outputs:
		list
		Utility:
		This function takes in a list of foreign words and translates them into english, returns that list of translations.
		"""
		if strLangName == "english":
			# english translated to english is english
			return listForeignWordList

		listRetList = []

		intCounter = 0

		for strWord in listForeignWordList:
			if(intCounter == 100):
				# wait for google translate to cool down
				time.sleep(0.5)
			try:
				strLowerStrWord = strWord.lower()
				strLowerStrWordTranslation = GoogleTranslator(source = strLangName,target = "english").translate(text=strLowerStrWord)
				listRetList.append(strLowerStrWordTranslation)
			except Exception as e:
				print("************")
				print("While processing \"{}\" in language \"{}\", the following error occurred: ".format(strWord, strLangName))
				print(e)
				print("The value of np.nan will replace this word.")
				print("************")

				listRetList.append(np.nan)

			intCounter +=1
		
		print("Processing of language \"{}\" complete.".format(strLangName))
			
		return listRetList
	
	def dictGetLangTransToEng(listForeignWordList,strLangName):
		"""
		Inputs:
		list listForeignWordList, string "strLangName"
		
		Outputs:
		dictionary with translations as values
		
		Utility:
		This function processes translations and stores them in a dictionary for all languages other than English. Such a dictionary can then 
		be used to construct a pandas dataframe. This dictionary of translations can be accessed in the future for further
		reference. This function does NOT perform alignment. 
		"""
		
		# creating blank dictionary
		dictTranslatedWords = {}
		
		# english translated to english is english
		if strLangName == "english":
			for word in listForeignWordList:
				dictTranslatedWords[word] = word 
			return dictTranslatedWords
			
		# translating for any other language
		intCounter = 0
		dictTranslatedWords = {}
			
		for strWord in listForeignWordList:
			if(intCounter == 100):
				# wait for google translate to cool down
				time.sleep(0.5)
			try:
				strLowerStrWord = strWord.lower()
				# if word not found in dictionary, send to translator and place in dictionary
				if strLowerStrWord not in dictionary.keys():
					strLowerStrWordTranslation = GoogleTranslator(source = strLangName,target = "english").translate(text=strLowerStrWord)
					dictTranslatedWords[strLowerStrWord] = strLowerStrWordTranslation
				else: # else just copy over word
					#strLowerStrWordTranslation = dictionary[strLowerStrWord]
					continue
					
			except Exception as e:
				print("************")
				print("While processing \"{}\" in language \"{}\", the following error occurred: ".format(strWord, strLangName))
				print(e)
				print("The value of np.nan will replace this word.")
				print("************")

			intCounter +=1

		print("Processing of language \"{}\" complete.".format(strLangName))

		# returns dictionary
		return dictTranslatedWords

	def dfMakeAlignDf(self, strLangA,strLangB,listLangAWords,listLangBWords,listLangAEngTrans,listLangBEngTrans):
		"""
		Inputs:
		string "strLangA", string "strLangB", list "listLangAWords", list "listLangBWords", list "listLangAEngTrans",
		list "listLangBEngTrans"
		Outputs:
		pandas dataframe
		Utility:
		This function makes a pandas dataframe that is to be populated by "dfMakeTemplateAlignDf". Basically this is the skeleton of the dataframe.
		"dfMakeTemplateAlignDf" populates this dataframe with the words in both languages but does NOT align them. That is another function.
		"""
		dictDfDict = {}

		intLenA = len(listLangAWords)
		intLenB = len(listLangBWords)

		intMaxLen = 0
		if intLenA > intLenB:
			intMaxLen = intLenA
		else:
			intMaxLen = intLenB
		
		# create columns for languages
		dictDfDict[strLangA] = listLangAWords
		dictDfDict[strLangB] = listLangBWords
		
		# create index column
		dictDfDict["index"] = [i for i in range(intMaxLen)]
			# create column for the alignment
		dictDfDict["alignment"] = [""] * intMaxLen
	
		dictDfDict["{}_eng".format(strLangA)] = listLangAEngTrans
		dictDfDict["{}_eng".format(strLangB)] = listLangBEngTrans
	
		# pad the df
		for strKey in dictDfDict:
			intLength = len(dictDfDict[strKey])
			if intLength < intMaxLen:
				intDiff = intMaxLen - intLength
				dictDfDict[strKey] += [np.nan] * intDiff
	
		return pd.DataFrame.from_dict(dictDfDict)
	
	def dfMakeAlignDfFromDict(strLangA,strLangB,listLangAWords,listLangBWords, langADictionary, langBDictionary):
		"""
		Inputs:
		string "strLangA", string "strLangB", list listLangAWords, list listLangBWords, dict langADictionary, dict langBDictionary
		
		Outputs:
		filled pandas dataframe
		
		Utility:
		This function fills in a data pandas frame from a set of dictionaries. This dataframe can then be passed to dfGenerateAlignments()
		"""
		dictDfDict = {}

		intLenA = len(listLangAWords)
		intLenB = len(listLangBWords)

		listLangBEngTrans = []
		listLangAEngTrans = []
			
		intMaxLen = 0
		if intLenA > intLenB:
			intMaxLen = intLenA
		else:
			intMaxLen = intLenB

		# create columns for languages
		dictDfDict[strLangA] = listLangAWords
		dictDfDict[strLangB] = listLangBWords

		# create index column
		dictDfDict["index"] = [i for i in range(intMaxLen)]
			
		for word in listLangAWords:
			if word in langADictionary.keys():
				listLangAEngTrans.append(langADictionary[word])
					
		for word in listLangBWords:
			if word in langBDictionary.keys():
				listLangBEngTrans.append(langBDictionary[word])

		dictDfDict["{}_eng".format(strLangA)] = listLangAEngTrans
		dictDfDict["{}_eng".format(strLangB)] = listLangBEngTrans

		# pad the df
		for strKey in dictDfDict:
			intLength = len(dictDfDict[strKey])
			if intLength < intMaxLen:
				intDiff = intMaxLen - intLength
				dictDfDict[strKey] += [np.nan] * intDiff

		return pd.DataFrame.from_dict(dictDfDict)

	def voidMakeTemplateAlignDf(self,strLangAName,strLangARawSample,strLangBName, strLangBRawSample):
		"""
		Inputs:
		string "strLangAName", string "strLangARawSample", string "strLangBName", string "strLangBRawSample"
		Outputs:
		void
		Utility:
		Creates a template csv in dir dirDirName. Note that this CSV is not aligned, but contains all of the words and indices
		required for alignment.
		"""

		# remove common words
		listLangASampleNoCommon = self._parser.listRemoveCommonWordsFromString(strLangARawSample,strLangAName)
		listLangBSampleNoCommon = self._parser.listRemoveCommonWordsFromString(strLangBRawSample,strLangBName)

		# remove punctuation
		listLangASampleNoPunctNoNumbers = self._parser.listRemoveNumbersAndPunct(listLangASampleNoCommon)
		listLangBSampleNoPunctNoNumbers = self._parser.listRemoveNumbersAndPunct(listLangBSampleNoCommon)

		# stem words
		listLangASampleStem = self._parser.listStemList(listLangASampleNoPunctNoNumbers,strLangAName)
		listLangBSampleStem = self._parser.listStemList(listLangBSampleNoPunctNoNumbers,strLangAName)

		# get the translations
		listLangAEngTrans = self.listGetLangTransToEng(listLangASampleNoCommon,strLangAName)
		listLangBEngTrans = self.listGetLangTransToEng(listLangBSampleNoCommon,strLangBName)

		dfAlignDf = self.dfMakeAlignDf(strLangAName,strLangBName,
			listLangASampleNoCommon,listLangBSampleNoCommon,
			listLangAEngTrans,listLangBEngTrans)
		
		return dfAlignDf

	def voidDfToCSV(self,dfData,strFilePath):
		"""
		Inputs:
		pandas dataframe "dfData", string "strFilePath"
		Outputs:
		void
		Utility:
		This function creates a .csv file out of a pandas dataframe.
		"""
		dfData.to_csv(strFilePath,index=False,encoding="utf-8-sig")	

	def voidPopulateAlignmentCSV(self,strLangA,strLangB,strFilePath):
		"""
		Inputs:
		string "strLangA", string "strLangB", string "strFilePath"
		Outputs:
		void
		Utility:
		This function populates the alignment field of a csv file "strFilePath".
		"""
		# read the file
		dfCSV = pd.read_csv(strFilePath)

		dfAligned = self.dfGenerateAlignments(strLangA,strLangB,5,dfCSV)

		self.voidDfToCSV(dfAligned,strFilePath)
	
	def voidPopulateAlignmentCSVsFromDict(self, dictLangDict,strDirectory,intStep=5):
		"""
		Inputs:
		dict "dictLangDict", string "strDirectory", int "intStep"
		Outputs:
		void
		Utility:
		This function populates a directory "strDirectory" with the aligned .csv files of the languages in a dict "dictLangDict".
		The structure of "dictLangDict" should be:

		{[LANG_A_NAME_STRING]:[LANG_A_NAME_CONTENT_STRING],
			[LANG_B_NAME_STRING]:[LANG_B_NAME_CONTENT_STRING],
			...
		}
		"""
		# populates directory with csvs

		listAllLangs = list(dictLangDict.keys())

		for i in range(len(listAllLangs)):
			for j in range(i+1,len(listAllLangs)):
				strLangA = listAllLangs[i]
				strLangAContent = dictLangDict[strLangA]

				strLangB = listAllLangs[j]
				strLangBContent = dictLangDict[strLangB]

				# create the data frame
				dfTempAlignTemplateDF = self.voidMakeTemplateAlignDf(strLangA,strLangAContent,
					strLangB,strLangBContent)

				# align the df
				dfTempAlignedDf = self.dfGenerateAlignments(strLangA,strLangB,intStep=intStep,df=dfTempAlignTemplateDF)

				# create the file
				strFilePath = "{}/{}_{}.csv".format(strDirectory,strLangA,strLangB)

				self.voidDfToCSV(dfTempAlignedDf,strFilePath)