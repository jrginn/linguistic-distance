def snsCreateHeatMap(listRatioValues, listLangNames, strFileSaveName):
    intTableLen = pow(len(listLangNames), 2)
    
    if ((len(listRatioValues[0]) * len(listRatioValues)) != intTableLen):
        return "Incorrect number of data values, please edit listRatioValues."
    
    listData = listRatioValues
    listRows = listLangNames
    listCols = listLangNames

    df = pd.DataFrame(listData, index=listRows, columns=listCols)
    s = sns.heatmap(df.head(), annot=True, cmap='YlOrRd', cbar=True,fmt='.4f')
    plt.savefig(strFileSaveName)
    s.set(xlabel='Source Language', ylabel='Target Language')


listLangNames = ["English", "French", "German", "Spanish"]
listRatioValues = ([1.0,0.2841656669969923,0.323188215,0.267677381],
                    [0.318653064,1.0,0.1918611835278502,0.378540584],
                    [0.332824098,0.18952406978459083,1.0,0.197317444],
                    [0.298173016,0.3988728349839461,0.178049206,1.0])
                    
snsCreateHeatMap(listRatioValues, listLangNames, "opensubstest.png")