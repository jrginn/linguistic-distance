import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
#### This class is to hold all utilities needed, such as graphing.

"""
***************************
Class notes:
***************************
This class contains many utility functions that can be used in other functions.
These typically include graphical representations of data.
"""
class Util:
	
	def dfCreateBasicDf(self,aPairingList):
		"""
		Inputs:
		list "aPairingList"
		Outputs:
		pandas dataframe
		Utility:
		This function takes a list structed as
		[[lang1,lang2,percentage],[lang1,lang2,percentage]...]
		and creates a generic dataframe of it.
		Arguments: a pairing list. Output: a dataframe.
		"""
		
		df = pd.DataFrame(aPairingList)

		return df
	
	def dfCreateCorrDf(self,aPairingList):
		"""
		Inputs:
		list "aPairingList"
		Outputs:
		pandas dataframe
		Utility:
		This function takes a list structured as
		[[lang1,lang2,percentage],[lang1,lang2,percentage]...]
		and creates a correlation dataframe from it.
		For use in creating heatmaps.

		Arguments: a pairing list. Output: a correlation dataframe.
		"""
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

	def snsCreateHeatMap(listLangNames, listRatioValues, strFileSaveName, strColorScheme):
		"""
		Inputs:
		list "listLangNames"
		list "listRatioValues"
		str "strFileSaveName"
		str "strColorScheme"

		Outputs:
		heatmap

		Utility:
		This function takes a list of languages from which comparison ratios will be used to construct a heatmap. The next required parameter, the list of data, must 
		be equivalent to the square of the number of languages in the first list. For example, if four languages are given in the first list, sixteen data points are
		exepected in the second. The following two string arguments set the title of the saved graphic and the color scheme of the map. 

		"""
		intTableLen = pow(len(listLangNames), 2)
    
		if ((len(listRatioValues[0]) * len(listRatioValues)) != intTableLen):
			return "Incorrect number of data values, please edit listRatioValues."
    	
		listData = listRatioValues	
		listRows = listLangNames
		listCols = listLangNames

		dfHeatMapData = pd.DataFrame(listData, index=listRows, columns=listCols)
		s = sns.heatmap(dfHeatMapData.head(), annot=True, cmap=strColorScheme, cbar=True,fmt='.4f')
		s.set(xlabel='Source Language', ylabel='Target Language')
		plt.savefig(strFileSaveName)

		return s

#### EXAMPLE USAGE OF HEATMAP FUNCTION ####
# listLangNames = ["English", "French", "German", "Spanish"]
# listRatioValues = ([1.0,1,1,0.267677381],
#                   [1,1.0,1,0.378540584],
#                   [1,1,1.0,0.197317444],
#                   [1,1,0.178049206,1.0])
# snsCreateHeatMap(listRatioValues, listLangNames, "opensubstest.png", "BlGr")




