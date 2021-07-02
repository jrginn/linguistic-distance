import unidecode
import re
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


# This class contains all utils for parsing the samples.
# With reference from https://github.com/vivianofsouza/linguistic-distance

class Parser():
	def only_consonants(self,aString):
		"""Returns only the consonants from a given string.
			Argument: a string. Output: a string."""
		# # the characters to be removed from aString
		# toRemove = re.compile(r"[aeiou0-9,@\?\.$%_/\!:()\n-;\"'&=\* ]")
		REGEX = "[bcdfghjklmnpqrstvwxyz]"

		# turn into all lower case
		temp_str = aString.lower()
		# convert accents / other to alphabetical
		temp_str = unidecode.unidecode(temp_str)
		# # remove characters
		# ret = re.sub(toRemove,"",ret)
		merged_str = "".join(re.findall(REGEX,temp_str))
		return merged_str

	def clean_sample(self,aString,language):
		"""Returns consonants after stemming words.
			Arguments: a string for the sample and the sample's language."""
		    # creating objects for stemmer, common words and key for punctuation/numbers to be removed
		stemmer = SnowballStemmer(str(language))
		common_words = stopwords.words(language)

		# separates sentence into elements and stores in elemList
		wordList=aString.split()
		
		# stemming first
		stems=[]
		for word in wordList:
			if word not in common_words:
				w = stemmer.stem(word)
				stems.append(w)

		# now removing punctuation, numbers, vowels and storing in wordList
		# need a string to call only_consonants
		parsed_stems = []
		for stem in stems:
			stripped_str  = self.only_consonants(stem)
			if(stripped_str != ""):
				parsed_stems.append(stripped_str)

		return parsed_stems 


# parser = Parser()
# ret = parser.clean_sample("подтверждая","russian")
# print(ret)
# print(unidecode.unidecode("подтверждая"))