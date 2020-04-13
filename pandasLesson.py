# Load the Pandas libraries with alias 'pd'
import pandas as pd
import matplotlib.pyplot as plt

# File Loading: Absolute and Relative Paths
filePath = "COVID-19.csv"
# https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide
####################################################
####################################################

# Read File:
# Other Delimiters/Separators – TSV files
# sepstr = default ‘,’ || delimiterstr = default None (Alias for sep)

# engine |optional| C is faster while the python engine is currently more feature-complete.
# true_valueslist |optional| Values to consider as True.
# false_valueslist |optional| Values to consider as False.
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html

fields = ['dateRep','cases','deaths','countriesAndTerritories']
data_df = pd.read_csv(filePath,sep=",", header=0, encoding="utf-8", usecols=fields) 
data_df.rename(columns={'countriesAndTerritories': 'countries', 'dateRep':'date'}, inplace=True)

####################################################
####################################################
# Dates:

# if we want to do dates calculations we need to defined the column as date type
# we can applay date calculation to column:
from datetime import datetime as dt
dateType = lambda x: dt.strptime(str(x), "%d/%m/%Y")
data_df["date"] = data_df["date"].apply(dateType) # datetime64[ns]
# OR
# read it again while specifying the date column
# data_df = pd.read_csv(filePath,sep=",",header=0, encoding="utf-8",usecols=fields,
#  dayfirst=True, parse_dates=[0]) 
# dayfirst |bool, default False| DD/MM format dates, international and European format.

# print(data_df['date'].dtype) 
# before: object, after: datetime64[ns]

####################################################
####################################################
# Filter unnecessary data:

# Which Is Faster:

# data_df = data_df[data_df['deaths'] > 0 & (data_df['deaths'] > 0 )]
# row_number , col_number = data_df.shape
# OR
# data_df = data_df.loc[(data_df['cases'] > 0) & (data_df['deaths'] > 0)]

############

row_number , col_number = data_df.shape # unpacking values
print("original naumber of rows:", row_number)

# pandas boolean vectors to filter the data: | for or, & for and, and ~ for not
data_df = data_df.loc[(data_df['cases'] > 0) & (data_df['deaths'] > 0)]

row_number , col_number = data_df.shape
print("after filtering naumber of rows:", row_number)
####################################################
####################################################
# Print some data:

# Assuming df has a unique index, this gives the row with the maximum date value
lastUpdatedData = data_df.loc[data_df['date'].idxmax()]
mostDeaths = data_df.loc[data_df['deaths'].idxmax()]
informationToPrint = "last updated: {0} at {1}\nand the highest value of deaths ({2}) occurred in {3}".format(lastUpdatedData['date'],lastUpdatedData['countries'],mostDeaths['deaths'],mostDeaths['countries'])
print("some information:", informationToPrint)

print(data_df.head()) # Preview 5 lines of the loaded data

del data_df['date']
####################################################
####################################################
# the gist of it:

data_df = data_df.groupby(["countries"]).sum().reset_index()

####################################################
####################################################
# Plot the df:

# we have lots of countries, lets narrow it down a little for this example...
data_df = data_df.loc[(data_df['countries'] == 'China') | (data_df['countries'] == 'France') | (data_df['countries'] == 'Israel') | (data_df['countries'] == 'Japan')].reset_index(drop=True)
# reset_index(drop=True), We can use the drop parameter to avoid the
#  old index being added as a column

# gca stands for 'get current axis' (matplotlib axes)
ax = plt.gca() 
# doing it will let us combine 2 plot on the same figure
# or just add more data to the plot

# one way is this-
# data_df.plot(kind='line',x='countries',y='deaths',label='deaths',color='red',ax=ax)
# data_df.plot(kind='line',x='countries',y='cases',label='cases',ax=ax)
# plt.show()

# the other way is this-
data_df.set_index('countries', inplace=True)
# inplace=True == Modify the DataFrame in place (do not create a new object).
# without inplace the pd created inedx with numeric values and index with str
data_df.plot.line(rot=0,ax=ax,color=["red","blue"]) # OR data_df.plot.bar(rot=0)
# rot=0 == change the labels rotation

# add text annotation to plot
rows, cols = data_df.shape
for col in range(cols):
    for i in range(rows):
        ax.annotate('{}'.format(data_df.iloc[i, col]), xy=(i, data_df.iloc[i, col]))

plt.title("the COVID-19")
plt.figtext(.5, .5, informationToPrint, wrap=True)
plt.tight_layout()

plt.show()