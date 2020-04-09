# importing the required module 
import timeit 
  
# code snippet to be executed only once 
mysetup = "import pandas as pd"
  
# code snippet whose execution time is to be measured 
mycode = ''' 
data_df = pd.read_csv("COVID-19.csv")
data_df = data_df[data_df['deaths'] > 0 & (data_df['deaths'] > 0 )]
'''
#
iterations = 100

# timeit statement 
check = timeit.timeit(setup = mysetup, 
                    stmt = mycode, 
                    number = iterations)
print(check) # execution time for all iterations
print(check/iterations) # execution time for single iteration 

# output of above program will be the execution time(in seconds) for all
#  iterations of the code snippet

mycode = ''' 
data_df = pd.read_csv("COVID-19.csv")
data_df = data_df.loc[(data_df['cases'] > 0) & (data_df['deaths'] > 0)]
'''
check = timeit.timeit(setup = mysetup, 
                    stmt = mycode, 
                    number = iterations)
print(check)
print(check/iterations) 