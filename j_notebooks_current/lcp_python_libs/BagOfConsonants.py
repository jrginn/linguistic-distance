from lcp_python_libs.Parser import Parser
# methods for cleaning samples

# This class contains the methods required in the 'Bag Of Consonants' approach.

class BagOfConsonants():
	def __init__(self):
		self._parser = Parser()

	def alpha_sort_dict(self,aDict):
		"""Returns a alphanumerically sorted dictionary.
			Arguments: a dictionary. Output: a sorted dictionary."""
		sorted_d = {}
		for i in sorted(aDict):
			sorted_d[i] = aDict[i]

		return sorted_d


	def get_c_dict(self,aString,sorted=False):
		"""Returns a dictionary of all of the consonants found in a string.
			Arguments: a string sample, a boolean to sort or not (default: unsorted).
			Output: a dictionary of consonants."""
		    # initialize an empty dictionary
		c_dict = {}
		# strip the string input to only consonants
		# first clean sample (returns a list), use join to turn to string
		stripped_c = ("").join(self._parser.only_consonants(aString))
		
		# populate the dictionary
		for c in stripped_c:
			if c in c_dict.keys():
				# increment count
				c_dict[c] +=1
			else:
				# add to consonant dict
				c_dict[c] = 1
		if(sorted == True):
			return self.alpha_sort_dict(c_dict)	
		return c_dict
	
	def get_diff_dict(self,strA,strB,sorted=False):
		"""Returns a dictionary of the differences in consonants found between
			strA and strB.
			Arguments: two string samples, a boolean for sorting (default: unsorted). 
			Output: A dictionary of consonant differences."""

		    # initialize empty dictionary
		diff_dict = {}
		
		# strip both strings
		c_dictA = self.get_c_dict(strA)
		c_dictB = self.get_c_dict(strB)
		
		# get all unique consonants found between both strings
		# add both keys, then take the set of them
		# set returns all individual elements, so we only get uniques
		found_consonants = list(c_dictA.keys()) + list(c_dictB.keys())
		uniq_consonants = set(found_consonants)
		
		for c in uniq_consonants:
			if(c in c_dictA and c in c_dictB):
				# a consonant appears in both strings
				# thus can properly subtract them
				# take absolute value so we can normalize later based on some factor
				difference = abs(c_dictA[c] - c_dictB[c])
				diff_dict[c] = difference
				
			elif(c in c_dictA):
				# unique consonant only in one string, cannot subtract
				# thus the difference is the number of appearances of unique consonant in the one string
				diff_dict[c] = c_dictA[c]
			else:
				diff_dict[c] = c_dictB[c]
		if(sorted == True):
			return self.alpha_sort_dict(diff_dict)	
		return diff_dict
	
	def get_c_diff_count(self,aDiffDict):
		"""Returns an integer value of the total differences of consonants found in
			a diffDict (see "get_diff_dict").
			Arguments: a difference dictionary. Output: an integer."""
		diff_sum = 0
		for k in aDiffDict.keys():
			diff_sum += aDiffDict[k]
		return diff_sum
	
	def get_normalized_diff(self,strA,strB,printProgress=False):
		# TO DO:
		# Check registers, read a JSON file for registers (for the percentages
		# of consonants to remove)
		"""Returns the normalized percentage difference between two strings
			using the BagOfConsonants method.
			Normalization by subtracting the total differences found from the total amount
			of consonants found then dividing by total amount of consonants found.
			Arguments: two strings. Output: a percentage between 0-1."""
		
		cDictA = self.get_c_dict(strA)
		cDictB = self.get_c_dict(strB)
		diffDict = self.get_diff_dict(strA,strB)

		
		
		total_cs = self.get_c_diff_count(cDictA) + self.get_c_diff_count(cDictB)
		total_diff = self.get_c_diff_count(diffDict)

		if(printProgress):
			print("String 1 Dictionary:")
			print(self.alpha_sort_dict(cDictA))
			print("String 2 Dictionary:")
			print(self.alpha_sort_dict(cDictB))
			print("Difference Dictionary:")
			print(self.alpha_sort_dict(diffDict))
			print("Total Differences:")
			print(total_diff)
			print("Total Consonants:")
			print(total_cs)

		perc = (total_cs - total_diff) / total_cs

		return perc
	
#### BASIC USE ####
# boc = BagOfConsonants()
# strA = "Hello World!"
# strB = "Goodbye World!"
# d1 = boc.get_c_dict(strA,True)
# print(d1)
# d2 = boc.get_c_dict(strB,True)
# print(d2)
# d3 = boc.get_diff_dict(strA,strB)
# print(d3) 

#### PERCENTAGES EXAMPLE ####
# boc = BagOfConsonants()
# strA = "Guided by the purposes and principles of the Charter of the United Nations, and expressing in particular the need to achieve international cooperation in promoting and encouraging respect for human rights and fundamental freedoms for all without distinction"
# strB = "Guiado por los propósitos y principios de la Carta de las Naciones Unidas, y expresando en particular la necesidad de lograr la cooperación internacional para promover y alentar el respeto de los derechos humanos y las libertades fundamentales para todos sin distinción"
# print(boc.get_normalized_diff(strA,strB))
