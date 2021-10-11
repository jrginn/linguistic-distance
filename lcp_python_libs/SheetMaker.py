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

	def listCreateWordWrapperList(self,lang_list):
		"""
		Inputs:
		list "lang_list"
		Outputs:
		list
		Utility:

		This function wraps words found in a list "lang_list" with the WordWrapper class.
		This is used for "dfGenerateAlignments". 
		Arguments: a list of words in a language. Output: a list of WordWrapper classes.
		Note that this also checks if a word is np.nan. If so, it will not append it.
		"""
		ret = []
		for i, word in enumerate(lang_list):
			if type(word) != float:
				ret.append(WordWrapper(word,i))
				
		return ret

	def boolCheckBounds(self,index_int,step_int,check_list):
		"""
		Inputs:
		int "index_int", int "step_int", list "check_list"
		Outputs:
		str
		Utility:
		This function checks if an selected index "index_int" is within "step_int" of a list "check_list".

		For instance, if the function returns "both", then i-step, i+step are within 0 to 
		the length of the list, thus within "both" upper and lower bounds.
		Similarly, "lower" is for within a lower bound, or i-step,i is between 0 and the length,
		"upper" is for within upper bound, or i,i+step is between 0 and the length.
		"""
		# first check both
		if (index_int-step_int) > 0 and (index_int+step_int) < len(check_list):
			return "both"
		# check lower
		elif (index_int-step_int) > 0 and index_int < len(check_list):
			return "lower"
		# check upper
		elif index_int > 0 and index_int + step_int < len(check_list):
			return "upper"
	def boolCheckEqualWordWrappers(self,i_int,j_int,listLangAWrappers_list,listLangBWrappers_list):
		"""
		Inputs:
		int "i_int", int "j_int", list "listLangAWrappers_list", list "listLangBWrappers_list"
		Outputs:
		str
		Utility:
		This function takes in two lists of word wrappers, and checks equality between them.
		If l1_word_wrappers[i]._word == l2_word_wrappers[j]._word, the function returns "equal".
		Else, return "unequal".
		If the word is within the other word, it returns "in". Else, it again returns "unequal".
		"""
		word1_str = listLangAWrappers_list[i_int]._word
		word2_str = listLangBWrappers_list[j_int]._word
		if word1_str == word2_str:
			return "equal"
		elif word1_str in word2_str or word2_str in word1_str:
			return "in"
		else:
			return "unequal"
	def strCreateAlignmentStr(self,i_int,j_int,counter_int,strMarker):
		"""
		Inputs:
		int "i_int", int "j_int", int "counter_int", str "strMarker"
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
			return "{} {}|{}".format("*"*counter_int,i_int,j_int)
		elif strMarker == "#":
		# "#" means "within word". This is more often risky, so always mark.
		# Even if within the original step count, mark it (why count + 1).
			return "{} {}|{}".format("#"*(counter_int+1),i_int,j_int)

	def dfGenerateAlignments(self,lang1,lang2,step,df):
		"""
		Inputs:
		Outputs:
		Utility:
		"""
		"""
		This function takes in two languages to be aligned, a step, and the dataframe of the 
		two languages. The "step" is the number of words near a word, up and down. For instance,
		if aligning a word at index 6, a step of 5 would mean to check either 5 above and below,
		just 5 above, or just 5 below. The step gets incremented by itself through every run.
		The alignments terminate when the step is greater than the length of either language's list of
		words. The "df" is the dataframe of the alignments, created by "create_align_df".
		"""
		dfReg = df.copy()
		# store words as WordWrappers
		listLangAWrappers = self.listCreateWordWrapperList(df[lang1 + "_eng"])
		listLangBWrappers = self.listCreateWordWrapperList(df[lang2 + "_eng"])
		
		# sentinel value
		boolWithinBounds = True
		
		# keep track of current step
		intCurrStep = step
		# keep track of runs
		counter = 0
		
		while(boolWithinBounds):
			# halt condition: if current step greater than length of lists
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
				intCurrStep += step
				
			except GetOutOfLoop:
                            # GetOutOfLoop is designed to be a quick means of leaving the loop and going back to the
                            # original while loop
				pass

		return dfReg

	def listGetLangTransToEng(self, listForeignWordList,strLangName):
		"""
		This function takes in a list of foreign words and translates them into english
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
			
		return listRetList
	
	def dictLangTransToEngText(self,lang_text_dict):
		"""
		Inputs:
		Outputs:
		Utility:
		"""
		"""
		This function takes in a dictionary of form {language: language words]}
		and returns a dictionary of form {language: list of english translations}

		If there is an error in the translation, the translation is "NOTFOUND", or "Not a number.
		"""
		ret_dict = {}


		for key in lang_text_dict:
			# no need to process eng
			if(key != "english"):
				print("Now processing \"{}\"...".format(key))
				translated_list = []
				for word in lang_text_dict[key]:
					try:
                                            # get a translation of the words
						translated_list.append(GoogleTranslator(source=key,target="english").translate(text=word))
					except Exception as e:
						print("*****************")
						print("While processing \"{}\" in language \"{}\" the following error occurred:".format(word,key))
						print(e)
						print("The value of np.nan will replace this word.")
						print("*****************")
						
						translated_list.append(np.nan)
				
				ret_dict[key] = translated_list


				print("Completed language " + "\"" + key + "\".")
				# sleep for google, cannot spam
				time.sleep(1.5)
		print("All languages processed.")
		return ret_dict

	def dictStrToDictList(self, d):
		"""
		Inputs:
		Outputs:
		Utility:
		"""
		"""
		This function returns a dictionary of split elements from a str, 
		given a dictionary of a big str.
		"""
		new_d = {}
		for key in d.keys():
			new_l = d[key].split()
			new_d[key] = new_l

		return new_d
	
	def dfMakeAlignDf(self, strLangA,strLangB,listLangAWords,listLangBWords,listLangAEngTrans,listLangBEngTrans):
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

	def create_align_df(self,lang1,lang2,lang_text_dict, lang_trans_dict):
		"""
		Inputs:
		Outputs:
		Utility:
		"""
		"""
		This function takes in 2 languages, a dictionary of the language texts in their raw form (lang_text_dict), and a dictionary of the english translations
		of the languages

		Returns an aligned dataframe of form:

		LANG1
		LANG2
		INDEX
		ALIGNMENT
		LANG1_eng
		LANG2_eng
		"""
		df_dict = {}
		df_dict[lang1] = lang_text_dict[lang1]
		df_dict[lang2] = lang_text_dict[lang2]
	
		len1 = len(lang_text_dict[lang1])
		len2 = len(lang_text_dict[lang2])
	
			# the df needs to have columns of equal length
			# so we pad the smaller dictionary
		max_len = 0
		if len1 > len2:
			max_len = len1
		else:
			max_len = len2
	
			# create index column
		df_dict["index"] = [i for i in range(max_len)]
				# create column for the alignment
		df_dict["alignment"] = [""] * max_len
	
		if(lang1 != "english"):
			df_dict["{}_eng".format(lang1)] = lang_trans_dict[lang1]
		else:
			df_dict["{}_eng".format(lang1)] = lang_text_dict[lang1]
		# other lang
		df_dict["{}_eng".format(lang2)] = lang_trans_dict[lang2]
	
		# pad the df
		for k in df_dict:
			length = len(df_dict[k])
			if length < max_len:
				diff = max_len - length
				df_dict[k] += [np.nan] * diff
	
		return pd.DataFrame.from_dict(df_dict)

	def voidMakeTemplateAlignDf(self,strLangAName,strLangARawSample,strLangBName, strLangBRawSample,dirDirName):
		"""
		Creates a template csv in dir dirDirName.
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
		# creates a csv file from pandas df
		dfData.to_csv(strFilePath,index=False,encoding="utf-8-sig")	

	def voidPopulateAlignmentCSV(self,strLangA,strLangB,strFilePath):
		# read the file
		dfCSV = pd.read_csv(strFilePath)

		dfAligned = self.dfGenerateAlignments(strLangA,strLangB,5,dfCSV)

		self.voidDfToCSV(dfAligned,strFilePath)

	def make_auto_matched_csv(self,lang_str_dict,step,dir_name):
		"""
		Inputs:
		Outputs:
		Utility:
		"""
		"""
		This function takes in a dictionary of raw language strs of form
		{LANG1:STR1, LANG2:STR2}

		and returns a csv of the matched alignments

		"""

		lang_parsed_dict = {}
		# create a dict of parsed strs
                # parsed = no common words
		for key in lang_str_dict:
			sample_str = lang_str_dict[key]
			lang_parsed_dict[key] =  self._parser.listRemoveCommonWordsFromString(sample_str,key)
		
                # get a dictionary of all of the english translations of the languages, AFTER removing common words
		translated_dict = self.dictLangTransToEngText(lang_parsed_dict)

		aligned_df_list = []

		all_langs = list(lang_str_dict.keys())

                # appending each combination of LANG_A LANG_B alignment dataframs to aligned_df_list
		for i in range(len(all_langs)):
			for j in range(i+1,len(all_langs)):
				temp = self.create_align_df(all_langs[i],all_langs[j],lang_parsed_dict,translated_dict)

				aligned_df = self.dfGenerateAlignments(all_langs[i],all_langs[j],step,temp)
				aligned_df_list.append(aligned_df)
		
                # making a directory to store the alignments, if dir already exists end the routine so as to not over-write things
		try:
			os.mkdir(dir_name)
		except:
			print("*************")
			print("WARNING: DIR ALREADY EXISTS. Ending function without creating dir")
			print("*************")

			return

                # create csv for each aligned_df, put into the dir that we just tried to make
		for i in range(len(aligned_df_list)):
			file_path = os.path.join(dir_name,"{}.csv".format(i))
			aligned_df_list[i].to_csv(file_path,index=False,encoding="utf-8-sig")
		
		lines = []
		# merge the csv
		csvs = [dir_name + "/{}.csv".format(i) for i in range(len(aligned_df_list))]

		for file_name in csvs:
			with open(file_name, "r",encoding="utf-8-sig") as csv_file:
				for line in csv_file:
					lines.append(line)