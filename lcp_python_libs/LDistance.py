import re # to use in regular expressions
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import nltk 
from nltk.translate import Alignment
from nltk.stem.snowball import SnowballStemmer # to stem words, doesn't work well
from nltk.corpus import stopwords # to remove common words
from transliterate import translit, get_available_language_codes

# This class contains all of the code to calculate L distances.

class LDistance():

	def ldistance(self,strA, strB):
		
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
		
		# printing
		#for t1 in range(size_x):
			#for t2 in range(size_y ):
				#print(int(matrix[t1][t2]), end=" ")
			#print()
			
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
		for i in range(len(alignment)):
			idx1 = alignment[i][0]
			idx2 = alignment[i][1]
			str1 = list1[idx1]
			str2 = list2[idx2]
			print(str1 + "-" + str2)
			l = self.ldistance(str(str1), str(str2))
			distances.append(l)
			
		return distances

	def measure_samples_dict(self,list1, list2, alignment):
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
			l = self.ldistance(str(str1), str(str2))
			distances.append(l)
			
		return distances


#### TESTING SPA-ENG ####
# ld = LDistance()
# engSample = "Guided by the purposes and principles of the Charter of the United Nations, and expressing in particular the need to achieve international cooperation in promoting and encouraging respect for human rights and fundamental freedoms for all without distinction"
# spaSample = "Guiado por los propósitos y principios de la Carta de las Naciones Unidas, y expresando en particular la necesidad de lograr la cooperación internacional para promover y alentar el respeto de los derechos humanos y las libertades fundamentales para todos sin distinción"

# #Removing vowels, punctuation, stemming
# engWords = ld.clean_sample(engSample, "english")
# spaWords = ld.clean_sample(spaSample, "spanish")

# #Manually transcribing sentence alignment to compare word-to-word
# print("Spa-Eng Pairs\n")
# eng_spa_align = [(0,0), (1,1), (2,2), (3,3), (4,5), (5,4), (6, 6), (7,7), (8,8), (9,9), (10, 11), (11, 10), (12, 12), (13, 13), (14, 14), (15, 16), (16, 15), (18, 17), (17, 18), (20, 19)]


# #Passing lists of consonant-only words in both languages and their alignment to Ldistnance method
# measures = ld.measure_samples(engWords, spaWords, eng_spa_align)
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
	
#### TESTING RUS-ENG ####
# ld = LDistance()
# engSample = "Guided by the purposes and principles of the Charter of the United Nations, and expressing in particular the need to achieve international cooperation in promoting and encouraging respect for human rights and fundamental freedoms for all without distinction"
# rusSample = "Руководствуясь целями и принципами Устава Организации Объединенных Наций и выражая в частности необходимость достижения международного сотрудничества в поощрении и поощрении уважения прав человека и основных свобод для всех без различия"
#rusSample = translit(rusSample, 'ru', reversed=True)
# engWords = engSample.split()
# rusWords = rusSample.split()

#Removing vowels, punctuation, stemming
# engWords = ld.clean_sample(engSample, "english")
# rusWords = ld.clean_sample(rusSample, "russian")


# transliterating Cyrillic text
# print("Rus-Eng Pairs\n")
# translitRus=[]
# for i in range(len(rusWords)):
#     l = translit(rusWords[i], 'ru', reversed=True)
#     translitRus.append(l)

# # running through clean_sample once more - to remove vowels
# translitString=""
# for i in range(len(translitRus)):
#     translitString+=translitRus[i] + " "
# rusFinal = ld.clean_sample(translitString, "russian")
    
# # manual alignment
# eng_rus_align = [(0,0), (1,1), (2,2), (3,3), (4,6), (5,7), (6,8), (7,7), (8,8), (9,9), (10, 10), (11,11), (12,12), (13,13), (15,14), (14,15), (16,16), (17,17), (19,18)]

# #Passing lists of consonant-only words in both languages and their alignment to Ldistnance method
# measures = ld.measure_samples(engWords, rusFinal, eng_rus_align)
# print("\n")
# print("English consonants\n")
# print(engWords)
# print("\n")
# print("Russian consonants\n")
# print(rusFinal)
# print("\n")
# print("L-Distance measures per pair of aligned words\n")
# print(measures)
# print("\n")

# print("Average")
# avg = 0
# for i in range(len(measures)):
#     avg = avg + measures[i]
# print(avg/len(measures))