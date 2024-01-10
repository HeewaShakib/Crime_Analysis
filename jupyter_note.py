import pandas as pd
import sys
print(sys.version)
print("pandas version", pd.__version__)

##pandas has a lot of different methods for Reading in different file types. all of these methods start with read and they include reading from a CSV file, 
#Excel files ,and many other file formats, each read method comes with its own parameters that can be set when reading and the files.
df=pd.read_csv("/home/heewa/Desktop/portfolio_project/flights.csv")

#df.to_csv("flights.csv", index=False) #there's a lot of different ways you can write your dataframe to_files or to databases using the  to_SQL .

pd.set_option("display.max_columns", 500) #depending on how many columns you have it may hide the middle columns when displaying this. 
#but you can override this by setting this option to display a larger maximum columns.

df.head()

df.tail() #a tail command which as you might expect we'll show the last five rows in the data frame

df.sample(frac=0.1, random_state=529)  #will pull a random subset of Rows from your entire data set. you can provide it a number which will return that number of rows or a fraction which will provide that fraction of the entire dataset.
#because the results of dot sample are random it can be helpful to add a random state and this will help with reproducibility.

df.columns  #the head command can be given any number to show that number of

df.index

df.info() # a built-in methods will give you information about the dataframe 
#including the size listing each column and the data type of each column

df[["TAIL_NUMBER"]]describe # handle non-numeric columns show the count number of unique values , top occurring value and the Frequency

df.shape, len(df)

#subsetting a DataFrame
df[["FLIGHT_NUMBER",	"TAIL_NUMBER",	"ORIGIN_AIRPORT",	"DESTINATION_AIRPORT",	"SCHEDULED_DEPARTURE"]]

df[df.columns[:5]]# take the first five columns

df[df.columns[-5]] # take the last five columns

df[[c for c in df.columns if "Time" in c]]  #to filter down the columns based on certain criteria 
                                        #for instance columns that have the text time in their name
                                        
df.select_dtype("int") #filtering columns is by using the select d-types method

#selecting a single column 
df["SCHEDULED_TIME"] #return the series of that data column
df[["SCHEDULED_TIME"]] # return a DataFrame with a single column

#Filtering based on rows
df.loc[] # determine location using name
df.iloc[1,2] #determine location using index, we'd be looking for row number one and column number three remember
df.iloc[:5,:5] #to pull the first five rows and the first five columns
df.iloc[5] #only filter to the row
df.iloc[[5]] #if we put this in a list then we'll be filtering to row number five as a dataframe

#Filtering based on rows
df.loc[] # determine location using name
df.iloc[1,2] #determine location using index, we'd be looking for row number one and column number three remember
df.iloc[:5,:5] #to pull the first five rows and the first five columns
df.iloc[5] #only filter to the row
df.iloc[[5]] #if we put this in a list then we'll be filtering to row number five as a dataframe

#filtering on boolean expression
df.loc[df["ARRIVAL_DELAY"]=>0] #we'll filter our dataframe down to only when this boolean expression is true.
df.loc[(df["ARRIVAL_DELAY"]=>0)&(df["DESTINATION_AIRPORT"]=="SEA")]

df.loc[~((df["ARRIVAL_DELAY"]=>0)&(df["DESTINATION_AIRPORT"]=="SEA")) #take the inverse of the expression by Simply adding a Tilda before it and if we use loc to filter to this expression we've now returned all rows except for the rows with spirit Airlines and this specific date.take the inverse of the expression by Simply adding a Tilda before it and if we use loc to filter to this expression we've now returned all rows except for these two 

#n alternate way to query your data frame based on boolean expressions using .query method
df.query("(DEPARTURE_TIME>100) and (ORIGIN_AIRPORT=='SFO')") #the doc query method takes in a string representation of the boolean expression you wish to filter on
                                                            #any values in the query method are assumed to be columns but you can represent strings by wrapping the value in quotes 
min_time=100
df.query("(DEPARTURE_TIME>@min_time) and (ORIGIN_AIRPORT=='SFO')") #our query expression can access an external variable by using the at symbol before the name in your query string

#Summarizing Data  
#n the data frame there are a number of summarization methods that can be run on either a single column or multiple columns. 
df["DEPARTURE_TIME"].count()
df["DEPARTURE_TIME"].mean()
df["DEPARTURE_TIME"].min()
df["DEPARTURE_TIME"].max()
df["DEPARTURE_TIME"].std()
df["DEPARTURE_TIME"].var()
df["DEPARTURE_TIME"].sum()
df["DEPARTURE_TIME"].Quantile(0.5)
df["DEPARTURE_TIME"].Quantile([0.25,0.75])
#any of these summarization methods can be run on multiple columns this will return a pandas series, where the index are the column names and the values are the summary values statistics. 
df[["ARRIVAL_DELAY","DESTINATION_AIRPORT", "DEPARTURE_DELAY"]].mean()

#if you want to run multiple statistics on various columns you can use the agg method by providing agg  a list of the statistics you'd like to run. 
# pandas will return a data frame with those statistics for each of the columns

df[["ARRIVAL_DELAY","DESTINATION_AIRPORT", "DEPARTURE_DELAY"]].agg(['mean', 'max', 'min'])

#the agg method can also take a dictionary where the keys are the column names and the values are a list of the aggregations
df[["ARRIVAL_DELAY","DESTINATION_AIRPORT","DEPARTURE_DELAY"]].agg({"ARRIVAL_DELAY":["mean","min"],"DESTINATION_AIRPORT":["count"], "ARRIVAL_DELAY":["min","max" ] }) #pandas will return only the summary statistics that you put in this dictionary

#summarizing categorical variables that also will work on numeric values
df["DESTINATION_AIRPORT"].unique() #will return an array of all the unique fields in the column 
df["DESTINATION_AIRPORT"].nunique() #nunique will give the number of unique values in a column 
df["DESTINATION_AIRPORT"].value_counts (normalize=True) #give you the number of counts for each value in that field
                                                        #setting normalized to true will give you a fractional value of the count within that column.                                      

#Running value counts on multiple columns will give you the count of those column combinations because we had multiple columns selected we now have a multi-index series.
df[["ARRIVAL_DELAY","DESTINATION_AIRPORT"]].value-counts()

#if we reset this index we then have a panda's dataframe with the count for every combination.
df[["ARRIVAL_DELAY","DESTINATION_AIRPORT"]].value-counts().reset_index()

#Advanced column methods that can be used on a panda series or pandas column 
df[["ARRIVAL_DELAY"]].rank() # compute the numerical data rank of one through the max value in that column

#there are a few different types of methods for ranking 
df[["ARRIVAL_DELAY"]].rank(method='dense') #which might have multiple values for the same rank 

df[["ARRIVAL_DELAY"]].rank(method='first') # give the first value in that column, the lower value

df[["ARRIVAL_DELAY"]].shift(1) # shift all the values in that column by the number you provide
df[["ARRIVAL_DELAY"]].shift(3,fill_value=0) #when the values are shifted at the beginning or end of the series will be empty values.
                                             #and you can set a fill value to fill these in if you'd like

df[["ARRIVAL_DELAY"]].cumsum()
df[["ARRIVAL_DELAY"]].cummax()
df[["ARRIVAL_DELAY"]].cummin()

#Rolling Methods
df[["DEPARTURE_TIME"]].rolling(window=5) #with the numeric column we can use the rolling method and provide it a window period where it will look at when running our aggregation
df[["DEPARTURE_TIME"]].rolling(window=5).mean() #by running something like mean we are returned with the average value at a rolling window of 5
#there's a lot of advanced features with rolling like adding the number of periods. 
# you can set center to true if you want the rolling window to center around the value for that column.

#Clip method
df["DEPARTURE_TIME"].clip(1000,2000) # this will clip the numeric value to a lower or upper window depending on what you provided

#groupby method
df.groupby("FLIGHT_NUMBER")[["DEPARTURE_TIME"]].mean()
df_agg=df.groupby("FLIGHT_NUMBER")[["DEPARTURE_TIME","DEPARTURE_DELAY"]].agg9["mean", "max", "min"] #the result of this is a DataFrame with multi index columns that can be complicated
df_agg.columns.to_flat_index() #give us a list of tuples
df_agg.columns=["_".join(c) for c in df_agg.columns] #to rename the columns. this way the columns for your aggregations are flattened and have names that are meaningful

# creating ne Columns
df["DEPARTURE_DELAY_2"]=df["DEPARTURE_DELAY"]/60

df=df.assign(DEPARTURE_DELAY_3=df["DEPARTURE_DELAY"]/60) #the assign method is nice because it can be chained with other operations

#sorting data by specific column type
df[["FLIGHT_NUMBER","ORIGIN_AIRPORT","SCHEDULED_DEPARTURE"]].sort_values("SCHEDULED_DEPARTURE", ascending=False)\
    .reset_index(drop=True)  #this will do the sort on this column and then reset our index values so now our lowest index value is with the highest arrival delay 

df[["FLIGHT_NUMBER","ORIGIN_AIRPORT","SCHEDULED_DEPARTURE"]].sort_index() #will sort your index if it is numeric

#Handling missing Data
df[["FLIGHT_NUMBER","ORIGIN_AIRPORT","SCHEDULED_DEPARTURE"]].isna() #will return true or false for each value in your data frame if it's missing

df[["FLIGHT_NUMBER","ORIGIN_AIRPORT","SCHEDULED_DEPARTURE"]].isna().sum() #because boolean values for true or false are actually ones and Zeros, we then can run sum on this which will give us a count of all the missing values

df[["FLIGHT_NUMBER","ORIGIN_AIRPORT","SCHEDULED_DEPARTURE"]].dropna() #will drop any of these rows that contain missing values
df[["FLIGHT_NUMBER","ORIGIN_AIRPORT","SCHEDULED_DEPARTURE"]].dropna(subset=["SCHEDULED_DEPARTURE"]) #you can provide it a subset of columns then it will only drop the rows where missing values occur in these columns.

df["SCHEDULED_DEPARTURE"].fillna(df["SCHEDULED_DEPARTURE"].mean()) #fill any of those missing values with whatever value provided

#combining Data
df1=df.copy()
df2=pd.read_csv("/home/heewa/Desktop/portfolio_project/humidity.csv").copy()
df3=pd.read_csv("/home/heewa/Desktop/portfolio_project/pressure.csv").copy()
df4=pd.read_csv(/"/home/heewa/Desktop/portfolio_project/weather_description.csv").copy() 