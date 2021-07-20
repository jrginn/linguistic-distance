import unidecode
import re
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


# This class contains all utils for parsing the samples.
# With reference from https://github.com/vivianofsouza/linguistic-distance

class Parser():

	def remove_numbers(self,aString):
		# regex to remove numbers
		remove_numbers = re.compile(r"[0-9]")

		aString = re.sub(remove_numbers,"",aString.lower())

		return aString

	def remove_punct(self, aString):
		# regex to remove puncutation
		remove_punct = re.compile(r"[,@\?\.$%_/:()']")

		aString = re.sub(remove_punct, "", aString.lower())

		return aString
	
	def remove_numbers_and_punct(self,aString):
		# regex to remove puncutation and numbers
		remove_punct = re.compile(r"[0-9,@\?\.\$%_/:()']")

		aString = re.sub(remove_punct, "", aString.lower())

		return aString

	def only_consonants(self,aString):
		"""Returns only the consonants from a given string.
			Argument: a string. Output: a string."""
		REGEX = "[bcdfghjklmnpqrstvwxyz]"

		# turn into all lower case
		temp_str = aString.lower()
		# convert accents / other to alphabetical
		temp_str = unidecode.unidecode(temp_str)
		# # remove characters
		# ret = re.sub(toRemove,"",ret)
		merged_str = "".join(re.findall(REGEX,temp_str))
		return merged_str

	def stem_word(self, aWord, language):
		"""
		Returns the word stemmed.

		Arguments: a word for the sample and the sample's language.
		Output: a stemmed word.
		"""
		stemmer = SnowballStemmer(str(language))

		stemmed_word = stemmer.stem(aWord)

		return stemmed_word
	
	def stem_list(self, aWordList, language):
		"""
		Returns the list of words stemmed.

		Arguments: a list of unstemmed words and the language of the words.
		Output: a list of stemmed words.
		"""
		stems = []
		for word in aWordList:
			# need to remove everything except apostrophe since stop words includes those
			word = re.sub(re.compile("@\?\.\$%_/: \(\) ,'"),"",word)
			stemmed_word = self.stem_word(word,language)
			# temporary fix
			if stemmed_word != ",":
				stems.append(stemmed_word)
		
		return stems
	
	def remove_common_words_from_string(self, aString, aLanguage):
		"""
		Returns a list without the common words in a language.

		Arguments: a string sample, the language of the sample
		Output: a list of the words that are not in stoppwords
		"""
		common_words = stopwords.words(aLanguage)

		# if french, get rid of "l'"
		if aLanguage == "french":
			common_words.append("l'")

		# lower case the string
		aString = aString.lower()


		# split string into word elements
		word_list = aString.split()

		word_list_no_common = []
		for word in word_list:
			if word not in common_words:
				word_list_no_common.append(word)
		
		return word_list_no_common

	
	def clean_sample(self,sample, language,**kwargs):

		# if want only unique words
		unique = False
		
		# optional kwargs
		if("unique" in kwargs):
			# only get unique words
			# if user enters unique: [True, False]
			unique = kwargs["unique"]

		# list of common words in the language
		common_words = stopwords.words(language)

		# convert to lowercase, remove punctuation / numbers
		sample = sample.lower()

		# separate based on spaces

		# if french, remove " l' " from beginning of words
		if language == "french":
			new_sample = []
			for word in sample.split():
				if len(word) > 2 and word[0:2] == "l'":
					word = word[2:]
				# append word to new sample
				new_sample.append(word)
			# update sample
			sample = (" ").join(new_sample)
		

		sample = self.remove_numbers_and_punct(sample)

		word_list = sample.split() 

		if unique:
			# then only return unique words
			word_list = list(dict.fromkeys(word_list))
		
		# stem the words
		stems = []
		for word in word_list:
			if word not in common_words:
				stemmed_word = self.stem_word(word,language)
				stems.append(stemmed_word)
		
		# remove punc, numbers, vowls and storing in word_list
		parsed_stems = []
		for stem in stems:
			stripped_str = self.only_consonants(stem)

			if(stripped_str != ""):
				parsed_stems.append(stripped_str)
				
		
		return parsed_stems


# TESTING

# _p = Parser()

# TESTING REMOVAL OF STOP WORDS

# print(_p.removeStopWordsFromString("Hello how are you","english"))
# print(stopwords.words("english"))

# TESTING STEMMING

# print(_p.stem_word("having","english"))
# print(_p.stem_list(["having", "had", "went" , "gone"],"english"))

# TESTING FRENCH REMOVAL OF " l' " IN START OF WORD
# fr_str = "Réaffirmant l'engagement de l'tous les l'États à s'acquitter de leurs obligations en vertu d' autres instruments importants du droit international , en particulier ceux du droit international des droits de l'homme et du droit international humanitaire"
# print(_p.clean_sample(fr_str, "french"))
