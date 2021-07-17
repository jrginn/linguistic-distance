import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from lang_trans.arabic import buckwalter
#### This class is to hold all utilities needed, such as graphing.

class Util:
	
	def create_basic_df(self,aPairingList):
		"""This function takes a list structed as
			[[lang1,lang2,percentage],[lang1,lang2,percentage]...]
			and creates a generic dataframe of it.

			Arguments: a pairing list. Output: a dataframe."""
		
		df = pd.DataFrame(aPairingList)

		return df
	
	def create_corr_df(self,aPairingList):
		"""This function takes a list structed as
			[[lang1,lang2,percentage],[lang1,lang2,percentage]...]
			and creates a correlation dataframe from it.
			For use in creating heatmaps.

			Arguments: a pairing list. Output: a correlation dataframe."""
		# get the pairs
		pairs = [i[0:2] for i in aPairingList]
		cols = []
		# get the unique languages
		for i in aPairingList:
			for j in i[0:2]:
				if j not in cols:
					cols.append(j)
					
		# set up an identity matrix df to populate
		identity_data = np.identity(len(cols))
		df = pd.DataFrame(identity_data,columns=cols,index=cols)
		
		# fill the zeros with NaNs -> Not a Number
		# fill bottom left, then transpose
		for i in range(len(cols)-1):
			for j in range(i+1,len(cols)):
				df[df.columns[i]][df.index[j]] = df[df.columns[j]][df.index[i]] = np.NaN
		
		# set the data on the bottom left, then transpose it to top right
		for i in range(len(cols)-1):
			for j in range(i+1,len(cols)):
				#print(cols[i],"-",df.index[j])
				ind = 0
				found = False
				if [cols[i],df.index[j]] in pairs:
					ind = pairs.index([cols[i],df.index[j]])
					found = True
				elif [cols[j],df.index[i]] in pairs:
					ind = pairs.index([cols[j],df.index[i]])
					found = True
				if(found):
					val = aPairingList[ind][-1]
					df[df.columns[i]][df.index[j]] = val
					df[df.columns[j]][df.index[i]] = val
			
		return df

	def create_heatmap(self,aPairingList):
		"""This function takes a list structed as
			[[lang1,lang2,percentage],[lang1,lang2,percentage]...]
			It then creates a heatmap out of the data.

			Arguments: a pairing list. Output: a heatmap."""
		df = self.create_corr_df(aPairingList)
		# TO DO: ADD OPTION TO SAVE AS PNG
		sns.heatmap(df)
	
	def transliterate_ar(self,aStr):
		"""This function transliterates Arabic into English using
		Buckwalter method."""
		# transliterates Arabic into English
		
		return buckwalter.transliterate(aStr)


#### TESTING ON DUMMY DATA ####
# util = Util()
# pairing_list = [["English","Spanish",0.7],["Spanish","German",0.3],
#                 ["Italian","Russian",0.2],["Italian","German",0.5],
#                 ["Spanish","Italian",0.9],["English","Italian",0.6],
#                 ["Russian","English",0.1],["English","German",0.4]]
# util.create_corr_df(pairing_list)




