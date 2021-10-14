import unidecode
import re
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

"""
***************************
Class notes:
***************************
This class deals with the parsing of strs.
It is used heavily for calculating Levenshtein distances.
"""
class Parser():

	def strRemoveNumbers(self,strA):
		"""
		Inputs:
		str "strA"
		Outputs:
		str
		Utility:
		This function takes in a str and outputs the str without numbers in it.
		"""
		# regex to remove numbers
		strRemoveNumbers = re.compile(r"[0-9]")

		strA = re.sub(strRemoveNumbers,"",strA.lower())

		return strA

	def strRemovePunct(self, strA):
		"""
		Inputs:
		str "strA"
		Outputs:
		str
		Utility:
		This function takes in a str and outputs the str without punctuation.
		"""
		# regex to remove puncutation
		strRemovePunct = re.compile(r"[,@\#?\.$%_/:()']")

		strA = re.sub(strRemovePunct, "", strA.lower())

		return strA
	
	def listRemoveNumbersAndPunct(self, listStrList):
		listRetList = []

		for strWord in listStrList:
			strWordParse = self.strRemoveNumbersAndPunct(strWord)
			listRetList.append(strWordParse)
		
		return listRetList

	
	def strRemoveNumbersAndPunct(self,strA):
		"""
		Inputs:
		str "strA"
		Outputs:
		str
		Utility:
		This function takes in a str and outputs the str without punctuation and without numbers.
		"""
		# regex to remove puncutation and numbers
		strRemovePunct = re.compile(r"[0-9,@\?\.\$%_/:()']")

		strA = re.sub(strRemovePunct, "", strA.lower())

		return strA

	def strOnlyConsonants(self,strA):
		"""
		Inputs:
		str "strA"
		Outputs:
		str
		Utility:
		This function returns only the consonants in a str.
		"""

		REGEX = "[bcdfghjklmnpqrstvwxyz]"

		# turn into all lower case
		temp_str = strA.lower()
		# convert accents / other to alphabetical
		temp_str = unidecode.unidecode(temp_str)
		# # remove characters
		# ret = re.sub(toRemove,"",ret)
		merged_str = "".join(re.findall(REGEX,temp_str))
		return merged_str

	def listStemList(self, listWordList,strLangName):
		stemmer = SnowballStemmer(strLangName)
		listRetList = []

		for strWord in listWordList:
			strWordStem = stemmer.stem(strWord)
			listRetList.append(strWordStem)
		return listRetList


	def strStemWord(self, aWord, languageStr):
		"""
		Inputs:
		str "aWord", str "languageStr"
		Outputs:
		str
		Utility:
		This function takes in a word "aWord" from a language "languageStr" and returns the word in its stemmed form as a str.
		"""
		stemmer = SnowballStemmer(languageStr)

		stemmed_word = stemmer.stem(aWord)

		return stemmed_word
	
	def listStemList(self, aWordList, languageStr):
		"""
		Inputs:
		list "aWordList", str "languageStr"	
		Outputs:
		list
		Utility:
		This function takes in a list of words "aWordList" from a language "languageStr" and
		returns a list of the stemmed words.
		"""
		stems = []
		for word in aWordList:
			# need to remove everything except apostrophe since stop words includes those
			word = re.sub(re.compile("@\?\.\$%_/: \(\) ,'\-"),"",word)
			stemmed_word = self.strStemWord(word,languageStr)
			# temporary fix
			if stemmed_word != ",":
				stems.append(stemmed_word)
		
		return stems
	
	def listRemoveCommonWordsFromString(self,strA,strLanguageA):
		"""
		Inputs:
		str "strA", str "languageStr"
		Outputs:
		list
		Utility:
		This function returns a list of the noncommon words within a str of text "strA" in given language "languageStr".
		"""
		common_words = stopwords.words(strLanguageA)

		# if french, get rid of "l'"
		common_words.append(["l'","",","])

		# lower case the str
		strA = strA.lower()

		# split str into word elements
		word_list = strA.split()
		# if french, remove " l' " from beginning of words
		if strLanguageA == "french":
			new_sample = []
			for word in word_list:
				if len(word) > 2 and word[0:2] == "l'":
					word = word[2:]
				# append word to new sample
				new_sample.append(word)
			# update sample
			word_list = new_sample

		word_list_no_common = []
		for word in word_list:
			if word not in common_words:
				word = self.strRemoveNumbersAndPunct(word)
				if word != "":
					if strLanguageA != "french":
						word_list_no_common.append(word)
					else:
						if word != "l" and word != "d":
							word_list_no_common.append(word)
		
		return word_list_no_common

	def listCleanSample(self,sampleStr, languageStr):
		"""
		Inputs:
		str "sampleStr", str "languageStr"		
		Outputs:
		list
		Utility:
		This function cleans the text found in "sampleStr" in given language "languageStr".
		"""

		# list of common words in the languageStr
		common_words = stopwords.words(languageStr)

		# convert to lowercase, remove punctuation / numbers
		sampleStr = sampleStr.lower()

		# separate based on spaces

		# if french, remove " l' " from beginning of words
		if languageStr == "french":
			new_sampleStr = []
			for word in sampleStr.split():
				if len(word) > 2 and word[0:2] == "l'":
					word = word[2:]
				# append word to new sampleStr
				new_sampleStr.append(word)
			# update sampleStr
			sampleStr = (" ").join(new_sampleStr)
		

		sampleStr = self.strRemoveNumbersAndPunct(sampleStr)

		word_list = sampleStr.split() 
		# stem the words
		stems = []
		for word in word_list:
			if word not in common_words:
				stemmed_word = self.strStemWord(word,languageStr)
				stems.append(stemmed_word)
		
		# remove punc, numbers, vowls and storing in word_list
		parsed_stems = []
		for stem in stems:
			stripped_str = self.strOnlyConsonants(stem)

			if(stripped_str != ""):
				parsed_stems.append(stripped_str)
				
		
		return parsed_stems


# TESTING

# _p = Parser()

# TESTING REMOVAL OF STOP WORDS

# print(_p.removeStopWordsFromString("Hello how are you","english"))
# print(stopwords.words("english"))

# TESTING STEMMING

# print(_p.strStemWord("having","english"))
# print(_p.listStemList(["having", "had", "went" , "gone"],"english"))

# TESTING FRENCH REMOVAL OF " l' " IN START OF WORD
# fr_str = "Réaffirmant l'engagement de l'tous les l'États à s'acquitter de leurs obligations en vertu d' autres instruments importants du droit international , en particulier ceux du droit international des droits de l'homme et du droit international humanitaire"
# print(_p.listCleanSample(fr_str, "french"))
