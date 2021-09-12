import numpy as np
import pandas as pd
import time
import os
from deep_translator import GoogleTranslator

from lcp_python_libs.Parser import Parser

class WordWrapper():

    def __init__(self,word,index):
        self._word = str(word).lower()
        self._index = index
    
class GetOutOfLoop(Exception):
    pass

class SheetMaker():

	def __init__(self):
		self._parser = Parser()

	def create_word_wrapper_list(self,lang_list):
		"""
		This function wraps words found in a language with the WordWrapper class.
		This is used for "generate_alignments". 
		Arguments: a list of words in a language. OUtput: a list of WordWrapper classes.
		Note that this also checks if a word is np.nan. If so, it will not append it.
		"""
		ret = []
		for i, word in enumerate(lang_list):
			if type(word) != float:
				ret.append(WordWrapper(word,i))
				
		return ret
	def check_bounds(self,i,step,alist):
		"""
		This function checks if an selected index is within "step" of a list.
		For instance, if the function returns "both", then i-step, i+step are within 0 to 
		the length of the list, thus within "both" upper and lower bounds.
		Similarly, "lower" is for within a lower bound, or i-step,i is between 0 and the length,
		"upper" is for within upper bound, or i,i+step is between 0 and the length.
		"""
		# first check both
		if (i-step) > 0 and (i+step) < len(alist):
			return "both"
		# check lower
		elif (i-step) > 0 and i < len(alist):
			return "lower"
		# check upper
		elif i > 0 and i + step < len(alist):
			return "upper"
	def check_equal_word_wrappers(self,i,j,l1_wrappers,l2_wrappers):
		"""
		This function takes in two lists of word wrappers, and checks equality between them.
		If l1_word_wrappers[i]._word == l2_word_wrappers[j]._word, the function returns "equal".
		Else, return "unequal".
		If the word is within the other word, it returns "in". Else, it again returns "unequal".
		"""
		word1 = l1_wrappers[i]._word
		word2 = l2_wrappers[j]._word
		if word1 == word2:
			return "equal"
		elif word1 in word2 or word2 in word1:
			return "in"
		else:
			return "unequal"
	def create_alignment_string(self,i,j,counter,marker):
		"""
		This function returns an alignment string that is inputted into the alignment df.
		i,j are the indices that will be shown in the alignment. 
		The counter is to determine the number of "marker" displayed.
		Ie: create_align_string(1,2,4,"*") returns:

		NOTE: BARS DELIM BETWEEN 2 LANGS, COMMAS BETWEEN WORDS OF SAME LANG!

		**** 1 2
		"""
		if marker == "*":
			# "*" denotes additional steps, ie
			# 2 stars means 2 additional steps.
			# If step = 5, 2 stars means 5 + 2(5) = 15 steps.
			return "{} {}|{}".format("*"*counter,i,j)
		elif marker == "#":
		# "#" means "within word". This is more often risky, so always mark.
		# Even if within the original step count, mark it (why count + 1).
			return "{} {}|{}".format("#"*(counter),i,j)
	def generate_alignments(self,lang1,lang2,step,df):
		"""
		This function takes in two languages to be aligned, a step, and the dataframe of the 
		two languages. The "step" is the number of words near a word, up and down. For instance,
		if aligning a word at index 6, a step of 5 would mean to check either 5 above and below,
		just 5 above, or just 5 below. The step gets incremented by itself through every run.
		The alignments terminate when the step is greater than the length of either language's list of
		words. The "df" is the dataframe of the alignments, created by "create_align_df".
		"""
		ret_df = df.copy()
		# store words as WordWrappers
		l1_wrappers = self.create_word_wrapper_list(df[lang1 + "_eng"])
		l2_wrappers = self.create_word_wrapper_list(df[lang2 + "_eng"])
		
		# sentinel value
		within_bounds = True
		
		# keep track of current step
		curr_step = step
		# keep track of runs
		counter = 0
		
		while(within_bounds):
			# halt condition: if current step greater than length of lists
			if curr_step > len(l1_wrappers) or curr_step > len(l2_wrappers):
				within_bounds = False
				break
			try:
				for i in range(len(l1_wrappers)):
					if self.check_bounds(i,curr_step,l1_wrappers) == "both" and self.check_bounds(i,curr_step,l2_wrappers) == "both":
						# can safely go both lower and uppper
						for j in range((i-curr_step),(i+curr_step)):
							if self.check_equal_word_wrappers(i,j,l1_wrappers,l2_wrappers) == "equal":
                                                            # words are a direct match
								alignment = self.create_alignment_string(l1_wrappers[i]._index,l2_wrappers[j]._index,counter,"*")
								ret_df.at[l1_wrappers[i]._index,"alignment"] = alignment
								# remove
								l2_wrappers.pop(j)
								l1_wrappers.pop(i)
								raise GetOutOfLoop
							# method 2: in -- change to "#"'
							elif self.check_equal_word_wrappers(i,j,l1_wrappers,l2_wrappers) == "in":
                                                            # word1 is within word2
								alignment = self.create_alignment_string(l1_wrappers[i]._index,l2_wrappers[j]._index,counter,"#")
								ret_df.at[l1_wrappers[i]._index,"alignment"] = alignment
								# remove
								l2_wrappers.pop(j)
								l1_wrappers.pop(i)
								raise GetOutOfLoop
					elif self.check_bounds(i,curr_step,l1_wrappers) == "lower" and self.check_bounds(i,curr_step,l2_wrappers) == "lower":
						# can safely check lower bounds
						for j in range((i-curr_step),i):
							if self.check_equal_word_wrappers(i,j,l1_wrappers,l2_wrappers) == "equal":
                                                            # direct match
								alignment = self.create_alignment_string(l1_wrappers[i]._index,l2_wrappers[j]._index,counter,"*")
								ret_df.at[l1_wrappers[i]._index,"alignment"] = alignment
								# remove
								l2_wrappers.pop(j)
								l1_wrappers.pop(i)
								raise GetOutOfLoop
							# method 2: in
							elif self.check_equal_word_wrappers(i,j,l1_wrappers,l2_wrappers) == "in":
                                                            # word1 in word2
								alignment = self.create_alignment_string(l1_wrappers[i]._index,l2_wrappers[j]._index,counter,"#")
								ret_df.at[l1_wrappers[i]._index,"alignment"] = alignment
								# remove
								l2_wrappers.pop(j)
								l1_wrappers.pop(i)
								raise GetOutOfLoop

					elif self.check_bounds(i,curr_step,l1_wrappers) == "upper" and self.check_bounds(i,curr_step,l2_wrappers) == "upper":
						# can safely check upper bounds
						for j in range(i,(i+curr_step)):
							if self.check_equal_word_wrappers(i,j,l1_wrappers,l2_wrappers) == "equal":
								alignment = self.create_alignment_string(l1_wrappers[i]._index,l2_wrappers[j]._index,counter,"*")
								ret_df.at[l1_wrappers[i]._index,"alignment"] = alignment
								# remove
								l2_wrappers.pop(j)
								l1_wrappers.pop(i)
								raise GetOutOfLoop
							# method 2: in
							elif self.check_equal_word_wrappers(i,j,l1_wrappers,l2_wrappers) == "in":
								alignment = self.create_alignment_string(l1_wrappers[i]._index,l2_wrappers[j]._index,counter,"#")
								ret_df.at[l1_wrappers[i]._index,"alignment"] = alignment
								# remove
								l2_wrappers.pop(j)
								l1_wrappers.pop(i)
								raise GetOutOfLoop
				counter += 1
				curr_step += step
				
			except GetOutOfLoop:
                            # GetOutOfLoop is designed to be a quick means of leaving the loop and going back to the
                            # original while loop
				pass

		return ret_df

	
	def get_lang_trans_to_eng_texts_dict(self,lang_text_dict):
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


	def dict_str_to_dict_list(self, d):
		"""
		This function returns a dictionary of split elements from a string, 
		given a dictionary of a big string.
		"""
		new_d = {}
		for key in d.keys():
			new_l = d[key].split()
			new_d[key] = new_l

		return new_d

	def create_align_df(self,lang1,lang2,lang_text_dict, lang_trans_dict):
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


	def make_auto_matched_csv(self,lang_str_dict,step,dir_name):
		"""
		This function takes in a dictionary of raw language strings of form
		{LANG1:STR1, LANG2:STR2}

		and returns a csv of the matched alignments

		"""

		lang_parsed_dict = {}
		# create a dict of parsed strings
                # parsed = no common words
		for key in lang_str_dict:
			sample_str = lang_str_dict[key]
			lang_parsed_dict[key] =  self._parser.remove_common_words_from_string(sample_str,key)
		
                # get a dictionary of all of the english translations of the languages, AFTER removing common words
		translated_dict = self.get_lang_trans_to_eng_texts_dict(lang_parsed_dict)

		aligned_df_list = []

		all_langs = list(lang_str_dict.keys())

                # appending each combination of LANG_A LANG_B alignment dataframs to aligned_df_list
		for i in range(len(all_langs)):
			for j in range(i+1,len(all_langs)):
				temp = self.create_align_df(all_langs[i],all_langs[j],lang_parsed_dict,translated_dict)

				aligned_df = self.generate_alignments(all_langs[i],all_langs[j],step,temp)
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











