import re # to use in regular expressions
import numpy as np
import nltk 
# from nltk.translate import Alignment
from nltk.stem.snowball import SnowballStemmer # to stem words, doesn't work well
from nltk.corpus import stopwords # to remove common words
# from transliterate import translit, get_available_language_codes

# This class contains all of the code to calculate L distances.

class LDistance():

	def l_distance(self,strA, strB):
		
		#setting up matrix
		size_x = len(strA) + 1
		size_y = len(strB) + 1
		matrix = np.zeros((size_x, size_y))
		for x in range(size_x):
			matrix [x, 0] = x
		for y in range(size_y):
			matrix [0, y] = y
		
		#populating matrix
		for x in range(1, size_x):
			for y in range(1, size_y):
				if strA[x-1] == strB[y-1]: #elements are equal
					matrix[x][y] = matrix[x-1][y-1]
				else: 
					a = matrix[x][y-1]
					b = matrix[x-1][y]
					c = matrix[x-1][y-1]
					if (a <= b and a <= c):
						matrix[x][y] = a + 1
					elif (b <= a and b <= c):
						matrix[x][y] = b + 1
					else:
						matrix[x][y] = c + 1
		# bottom-right element is l-distance
		distance = matrix[-1][-1]
			
		#taking into consideration the length of the words
		length = 0
		if ((len(strA) > len(strB)) or (len(strA) == len(strB))):
			length = len(strA)
		else:
			length = len(strB)
			
		lscore = ((length - distance) / length) 
		
		return lscore


	def measure_samples(self,list1, list2, alignment):
		"""Function that lines up pairs of words between the two samples, and calculates their l-distance
	   		parameters: 2 lists of words from each sample, 1 list of manually-created alignment between the two lists"""
		distances=[]
		
		# aligning pairs

		# Check if not dictionary, if so then 1-1
		if type(alignment) != dict:
			for i in range(len(alignment)):
				idx1 = alignment[i][0]
				idx2 = alignment[i][1]
				str1 = list1[idx1]
				str2 = list2[idx2]
				print(str1 + "-" + str2)
				l = self.l_distance(str(str1), str(str2))
				distances.append(l)
			return distances
		else:
			# check if many-many or 1-many alignments
			if(type(alignment[list(alignment.keys())[0]] == tuple)):
				return self.measure_samples_many_many(list1,list2,alignment)
			else:
				return self.measure_samples_one_many(list1,list2,alignment)
	
	def measure_samples_many_many(self, list1,list2,alignment_dict):
		"""
		function that lines up pairs of words between two samples.
		Parameters: 2 lists of words from each sample, 1 dictionary of tuples manually-created alignment between the two lists
		Output: a list of the l-d scores.
		"""

		distances = []

		# align lists of lists in alignments
		# each element in alignment is a 
		for tuple_key in alignment_dict.keys():
			str1 = ""
			str2 = ""

			# populate string1
			for i in range(len(tuple_key)):
				# find the corresponding index in list1, add it to str
				index = tuple_key[i]
				str1 += list1[index]
			
			# populate string2
			for i in range(len(alignment_dict[tuple_key])):
				# find the corresponding index in list1, add it to str
				index = alignment_dict[tuple_key][i]
				str2 += list2[index]
			
			print(str1 + "-" + str2)
			l_distance = self.l_distance(str1,str2)

			distances.append(l_distance)
			
		return distances

	def measure_samples_one_many(self,list1, list2, alignment):
		"""function that lines up pairs of words between the two samples, and calculates their l-distance
		parameters: 2 lists of words from each sample, 1 list of manually-created alignment between the two lists"""
		distances=[]
		
		# aligning pairs
		for i in alignment:
			str2 = ""
			str1 = list1[i]
			for x in range(len(alignment[i])):
				str2 += list2[alignment[i][x]]
			print(str1 + "-" + str2)
			l = self.l_distance(str(str1), str(str2))
			distances.append(l)
			
		return distances

# ### TESTING ###
# from Parser import Parser
# _ld = LDistance()
# _p = Parser()

# engSample = "Reaffirming that the enhancement of international cooperation in the field of human rights is essential for the full achievement of the purposes of the United Nations and that human rights and fundamental freedoms are the birthright of all human beings"
# gerSample = "Bekräftigend, dass die Verbesserung der internationalen Zusammenarbeit im Bereich der Menschenrechte für die volle Verwirklichung der Ziele der Vereinten Nationen von wesentlicher Bedeutung ist und dass die Menschenrechte und Grundfreiheiten das Geburtsrecht aller Menschen sind, den Schutz und die Förderung dieser Rechte und Freiheiten"

# engWords = _p.clean_sample(engSample, "english")

# gerWords = _p.clean_sample(gerSample, "german")

 

# eng_ger_dict = {
#     (0,):(0,),
#     (1,):(1,),
#     (2,):(2,),
#     (3,):(3,),
#     (4,):(4,),
#     (5,6):(1,),
#     (5,7):(1,),
#     (5,8):(1,),
#     (5,):(1,),
# }
# measures = _ld.measure_samples_many_many(engWords, gerWords, eng_ger_dict)

 

# print("\n")
# print("L-distance measures")
# print(measures)
# print("\n")
# print("Average")
# avg = 0
# for i in range(len(measures)):
#     avg = avg + measures[i]
# print(avg/len(measures))

# Testing on 1 - 1
# _ld = LDistance()
# _p = Parser()

# engSample = "Guided by the purposes and principles of the Charter of the United Nations, and expressing in particular the need to achieve international cooperation in promoting and encouraging respect for human rights and fundamental freedoms for all without distinction"
# spaSample = "Inspirándose en los propósitos y principios de la Carta de las Naciones Unidas y expresando en particular la necesidad de lograr la cooperación internacional en la promoción y el fomento del respeto de los derechos humanos y las libertades fundamentales para todos sin distinción"

# engWords = _p.clean_sample(engSample,"english")
# spaWords = _p.clean_sample(spaSample,"spanish")

# print("Spa-Eng Pairs\n")
# eng_spa_align = [(0,0), (1,1), (2,2), (3,3), (4,5), (5,4), (6, 6), (7,7), (8,8), (9,9), (10, 11), (11, 10), (12, 12), (13, 13), (14, 14), (15, 16), (16, 15), (18, 17), (17, 18), (20, 19)]
# measures = _ld.measure_samples(engWords,spaWords,eng_spa_align)
# print("\n")
# print("English consonants\n")
# print(engWords)
# print("\n")
# print("Spanish consonants\n")
# print(spaWords)
# print("\n")
# print("L-Distance measures per pair of aligned words\n")
# print(measures)
# print("\n")

# print("Average")
# avg = 0
# for i in range(len(measures)):
#     avg = avg + measures[i]
# print(avg/len(measures))

# Testing on Many - Many
# engSample = "Guided by the purposes and principles of the Charter of the United Nations, and expressing in particular the need to achieve international cooperation in promoting and encouraging respect for human rights and fundamental freedoms for all without distinction"
# spaSample = "Inspirándose en los propósitos y principios de la Carta de las Naciones Unidas y expresando en particular la necesidad de lograr la cooperación internacional en la promoción y el fomento del respeto de los derechos humanos y las libertades fundamentales para todos sin distinción"

# engWords = _p.clean_sample(engSample,"english")
# spaWords = _p.clean_sample(spaSample,"spanish")

# # dummy align data, note use of tuple:tuple dictionary
# # IMPORTANT: SINGLE ITEM TUPLES NEED TRAILING COMMA 
# eng_spa_align = {
# 	(0,1):(1,0),
# 	(2,):(2,),
# 	(3,4):(4,),
# 	(5,):(2,3),
# 	(5,6,7,8):(2,),
# }
# print(type(eng_spa_align))
# measures = _ld.measure_samples(engWords,spaWords,eng_spa_align)
# print("\n")
# print("English consonants\n")
# print(engWords)
# print("\n")
# print("Spanish consonants\n")
# print(spaWords)
# print("\n")
# print("L-Distance measures per pair of aligned words\n")
# print(measures)
# print("\n")

# print("Average")
# avg = 0
# for i in range(len(measures)):
#     avg = avg + measures[i]
# print(avg/len(measures))
