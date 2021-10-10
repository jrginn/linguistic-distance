import nltk
import re
import pandas as pd
from nltk.stem.snowball import SnowballStemmer 
from nltk.corpus import stopwords
from unidecode import unidecode
from transliterate import translit, get_available_language_codes
from lcp_python_libs.LDistance import LDistance
from lcp_python_libs.Parser import Parser

"""
***************************
Class notes:
***************************
This class calculates LDistances given an alignment dataframe.
"""
class Calculator():

    def __init__(self):
        self._ld = LDistance()
        self._p = Parser()
    
    def print_avg(self,val_list):
        """
        Inputs:
        a list "val_list"
        Outputs:
        void.
        Utility:
        This function prints the average of a list.
        """
        avg = 0
        for e in val_list:
            avg+= e
        avg = avg / len(val_list)

        print(avg)

    def generate_ldistance(self,lang1,lang2,df):
        """
        Inputs:
        String "lang1", string "lang2", a pandas dataframe.
        Outputs:
        Void.
        Utility:
        This function takes in two strings, "lang1" and "lang2" to denote the 
        languages compared. It also takes in a dataframe of an align data frame 
        (see SheetMaker's create_align_df) for this.
        
        Returns: nothing. Prints the 20,50, 100 LDs.
        """

        distances = []
        print("{} AND {}".format(lang1,lang2))
        print("-"*20)
        special_chars = re.compile(r"[#* ]")
        for align in df['alignment']:
            
            align_str = str(align)
            
            if align_str != "nan" and align_str != "":
                
                lhs,rhs = align_str.split("|")
                
                
                lhs = re.sub(special_chars,"",lhs)
                rhs = re.sub(special_chars,"",rhs)
                
                split_lhs = lhs.split(",")
                split_rhs = rhs.split(",")
                
                
                str1 = ""
                str2 = ""
                
                for align in split_lhs:

                    align_word = df[lang1][int(align)]
                    print("entry #", len(distances))
                    print(align,align_word, end=" ")
                    # clean the word
                    # note clean sample returns a list, need just the first entry
                    # which is the word
                    str1 += "".join(self._p.clean_sample(align_word,lang1))
                print(" -- ",end = " ")
                
                for align in split_rhs:

                    align_word = df[lang2][int(align)]
                    
                    print(align,align_word,end=" ")
            
                    str2 += "".join(self._p.clean_sample(align_word,lang2))
                print()
                print("devowelized:")
                print(str1, str2)
                if str1 != "" and str2 != "":
                
                    ld = self._ld.l_distance(str1, str2)
                    print("ld: ",ld)
                    print("_"*20)
                    distances.append(ld)
                    
                    if len(distances) == 20:
                        print("*"*20)
                        print("* 20 score:\n*",end=" ")
                        self.print_avg(distances)
                        print("*"*20)

                    elif len(distances) == 50:
                        print("*"*20)
                        print("* 50 score:\n*",end=" ")
                        self.print_avg(distances)
                        print("*"*20)
                    elif len(distances) == 100:
                        print("*"*20)
                        print("* 100 score:\n*",end=" ")
                        self.print_avg(distances)
                        print("*"*20)




