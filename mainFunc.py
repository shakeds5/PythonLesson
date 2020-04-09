import pandas as pd
import matplotlib.pyplot as plt

def main(filePath):
    fields = ['dateRep','cases','deaths','countriesAndTerritories']
    data_df = pd.read_csv(filePath,sep=",",header=0, encoding="utf-8",usecols=fields,
     dayfirst=True, parse_dates=[0]) 
    data_df.rename(columns={'countriesAndTerritories': 'countries', 'dateRep':'date'}, inplace=True)

    data_df = data_df.loc[(data_df['cases'] > 0) & (data_df['deaths'] > 0)]

    lastUpdatedData = data_df.loc[data_df['date'].idxmax()]
    mostDeaths = data_df.loc[data_df['deaths'].idxmax()]
    informationToPrint = "last updated: {0} at {1}\nand the highest value of deaths ({2}) occurred in {3}".format(lastUpdatedData['date'],lastUpdatedData['countries'],mostDeaths['deaths'],mostDeaths['countries'])

    del data_df['date']

    data_df = data_df.groupby(["countries"]).sum().reset_index()
    data_df = data_df.loc[(data_df['countries'] == 'China') | (data_df['countries'] == 'France') | (data_df['countries'] == 'Israel') | (data_df['countries'] == 'Japan')].reset_index(drop=True)
    
    ax = plt.gca() 
    data_df.set_index('countries', inplace=True)
    data_df.plot.line(rot=0,ax=ax,color=["red","blue"])

    # add text annotation to plot
    rows, cols = data_df.shape
    for col in range(cols):
        for i in range(rows):
            ax.annotate('{}'.format(data_df.iloc[i, col]), xy=(i, data_df.iloc[i, col]))

    plt.title("the COVID-19")
    plt.figtext(.5, .5, informationToPrint, wrap=True)
    plt.tight_layout()
    plt.show()