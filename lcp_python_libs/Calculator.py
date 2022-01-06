import re
import pandas as pd
import os

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
    
    def voidPrintAvg(self,val_list):
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
    
    def voidPrintLDScoresDir(self,strDirPath):
        """
        Inputs:
        Outputs:
        string "strDirPath"
        Void.
        Utility:
        This function reads each of the csvs in a directory of alignment files named "[langA]_[langB].csv"
        and prints the LDScores.
        """
        for strFileName in os.listdir(strDirPath):
            listFileParts = strFileName.split(".")
            if(listFileParts[-1] == "csv"):
                strFileBase = listFileParts[0]
                
                listLangNames = strFileBase.split("_")

                strLangAName = listLangNames[0]
                strLangBName = listLangNames[1]

                strFullFilePath = os.path.join(strDirPath,strFileName)
                dfTemp = pd.read_csv(strFullFilePath)

                self.voidPrintLDScoreFile(strLangAName,strLangBName,dfTemp)

    def voidPrintLDScoreFile(self,strLangA,strLangB,strFilePath):
        """
        Inputs:
        String "strLangA", string "strLangB", a pandas dataframe.
        Outputs:
        Void.
        Utility:
        This function takes in two strings, "strLangA" and "strLangB" to denote the 
        languages compared. It also takes in a dataframe of an align data frame 
        (see SheetMaker's create_align_df) for this.
        
        Returns: nothing. Prints the 20,50, 100 LDs.
        """

        df = pd.read_csv(strFilePath)

        distances = []
        print("-"*20)
        print("{} AND {}".format(strLangA,strLangB))
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

                    align_word = df[strLangA][int(align)]
                    print("entry #", len(distances))
                    print(align,align_word, end=" ")
                    # clean the word
                    # note clean sample returns a list, need just the first entry
                    # which is the word
                    #str1 += "".join(self._p.listCleanSample(align_word,strLangA))
                    str1 += "".join(self._p.strOnlyConsonants(align_word))
                print(" -- ",end = " ")
                
                for align in split_rhs:

                    align_word = df[strLangB][int(align)]
                    
                    print(align,align_word,end=" ")
            
                    #str2 += "".join(self._p.listCleanSample(align_word,strLangB))
                    str2 += "".join(self._p.strOnlyConsonants(align_word))

                print()
                print("devowelized:")
                print(str1, str2)
                if str1 != "" and str2 != "":
                
                    ld = self._ld.floatLDistance(str1, str2)
                    print("ld: ",ld)
                    print("_"*20)
                    distances.append(ld)
                    
                    if len(distances) == 20:
                        print("*"*20)
                        print("* 20 score:\n*",end=" ")
                        self.voidPrintAvg(distances)
                        print("*"*20)

                    elif len(distances) == 50:
                        print("*"*20)
                        print("* 50 score:\n*",end=" ")
                        self.voidPrintAvg(distances)
                        print("*"*20)
                    elif len(distances) == 100:
                        print("*"*20)
                        print("* 100 score:\n*",end=" ")
                        self.voidPrintAvg(distances)
                        print("*"*20)




