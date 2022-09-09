import re # to use in regular expressions
import numpy as np
import nltk 
from nltk.stem.snowball import SnowballStemmer # to stem words, doesn't work well
from nltk.corpus import stopwords # to remove common words


"""
***************************
Class notes:
***************************
This class contains all of the code to calculate L distances.
"""
class LDistance():

	def floatLDistance(self,strA, strB):
		"""
		Inputs:
		a string "strA", a string "strB"
		Outputs:
		float
		Utility:	
		This function calculates the distances between string A and B and returns their Levenshtein Distance.
		"""
		
		#setting up nparrMatrix
		intSizeX = len(strA) + 1
		intSizeY = len(strB) + 1
		nparrMatrix = np.zeros((intSizeX, intSizeY))
		for intX in range(intSizeX):
			nparrMatrix [intX, 0] = intX
		for intY in range(intSizeY):
			nparrMatrix [0, intY] = intY
		
		#populating nparrMatrix
		for intX in range(1, intSizeX):
			for intY in range(1, intSizeY):
				if strA[intX-1] == strB[intY-1]: #elements are equal
					nparrMatrix[intX][intY] = nparrMatrix[intX-1][intY-1]
				else: 
					a = nparrMatrix[intX][intY-1]
					b = nparrMatrix[intX-1][intY]
					c = nparrMatrix[intX-1][intY-1]
					if (a <= b and a <= c):
						nparrMatrix[intX][intY] = a + 1
					elif (b <= a and b <= c):
						nparrMatrix[intX][intY] = b + 1
					else:
						nparrMatrix[intX][intY] = c + 1
		# bottom-right element is l-distance
		distance = nparrMatrix[-1][-1]
			
		#taking into consideration the length of the words
		intLength = 0
		if ((len(strA) > len(strB)) or (len(strA) == len(strB))):
			intLength = len(strA)
		else:
			intLength = len(strB)
			
		lscore = ((intLength - distance) / intLength) 
		
		return lscore

	def listMeasureSamples(self,listLangA, listLangB, listAlignment):
		"""
		Inputs:
		list "listLangA", list "listLangB", list "listAlignment"
		Outputs:
		list
		Utility:	
		This function takes in a list of words from language 1 "listLangA", a list of words from language 2 "listLangB",
		and a list of alignments from language 1 to language 2 "listAlignment"

		It then returns alist of the alignments between lang1 to lang2.
		"""
		distances=[]
		
		# aligning pairs

		# Check if not dictionary, if so then 1-1
		if type(listAlignment) != dict:
			for i in range(len(listAlignment)):
				idx1 = listAlignment[i][0]
				idx2 = listAlignment[i][1]
				str1 = listLangA[idx1]
				str2 = listLangB[idx2]
				print(str1 + "-" + str2)
				floatL = self.floatLDistance(str(str1), str(str2))
				distances.append(floatL)
			return distances
		else:
			# check if many-many or 1-many listAlignments
			if(type(listAlignment[list(listAlignment.keys())[0]] == tuple)):
				return self.listMeasureSamplesManyMany(listLangA,listLangB,listAlignment)
			else:
				return self.listMeasureSamplesOneMany(listLangA,listLangB,listAlignment)
	
	def listMeasureSamplesManyMany(self, listLangA,listLangB,dictAlignment):
		"""
		Inputs:
		list "listLangA", list "listLangB", dictionary "dictAlignment"
		Outputs:
		list
		Utility:

		This function takes in a list of words from language A "listLangA", a list of words from language B
		"listLangB", and a dictionary of the alignments from language A to language B.

		It returns a list of the Levenshtein distances for each key-value pairing (not necessarily one word to one word).
		"""

		listDistances = []

		# align lists of lists in alignments
		# each element in alignment is a 
		for tuple_key in dictAlignment.keys():
			str1 = ""
			str2 = ""

			# populate string1
			for i in range(len(tuple_key)):
				# find the corresponding index in listLangA, add it to str
				index = tuple_key[i]
				str1 += listLangA[index]
			
			# populate string2
			for i in range(len(dictAlignment[tuple_key])):
				# find the corresponding index in listLangA, add it to str
				index = dictAlignment[tuple_key][i]
				str2 += listLangB[index]
			
			print(str1 + "-" + str2)
			floatLDistance = self.floatLDistance(str1,str2)

			listDistances.append(floatLDistance)
			
		return listDistances

	def listMeasureSamplesOneMany(self,listLangA, listLangB, dictAlignment):
		"""
		Inputs:
		list "listLangA", list "listLangB", dictionary "dictAlignment"
		Outputs:
		list
		Utility:	
		This function takes in a list of words from language A "listLangA, a list of words from language B "listLangB", and
		a dictionary of alignments.

		It then returns a list of the Levenshtein distances for each key-value pairing.
		"""
		distances=[]
		
		# aligning pairs
		for i in dictAlignment:
			str2 = ""
			str1 = listLangA[i]
			for x in range(len(dictAlignment[i])):
				str2 += listLangB[dictAlignment[i][x]]
			print(str1 + "-" + str2)
			l = self.floatLDistance(str(str1), str(str2))
			distances.append(l)
			
		return distances