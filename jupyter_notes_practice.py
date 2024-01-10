import pandas as pd
import sys
#print(sys.version)
#print("pandas version", pd.__version__)
df=pd.read_csv("/home/heewa/Desktop/portfolio_project/temperature.csv")
pd.set_option("display.max_columns", 500)


#combining Data
df1=df.copy()
df2=pd.read_csv("/home/heewa/Desktop/portfolio_project/humidity.csv").copy()
df3=pd.read_csv("/home/heewa/Desktop/portfolio_project/pressure.csv").copy()
df4=pd.read_csv("/home/heewa/Desktop/portfolio_project/weather_description.csv").copy() 

df_stack=pd.concat([df1,df2,df3,df4]) #pandas concat method take a list of the dataframes that we would like to concat
#print(df_stack.head(5))
#print(df_stack.tail(5))
#print(df_stack.sample(30))
#print(df_stack.shape)
#print(df1.shape)
#print(df2.shape)
#print(df3.shape)
#print(df4.shape)


#print("df2:\n",df2.columns)
#print("df3:\n",df3.columns)
#print("df4:\n",df4.columns)
#print(new_df.datetime.value_counts())
#df1=df1.reset_index(drop=True)
#df2=df2.reset_index(drop=True)
#df_stack_ax=pd.concat([df1,df2,df3,df4],axis=1) 
#print("shape of df stack:", df_stack.shape)
#print("shape of df stack_ax:", df_stack_ax.shape)
#print("shape of df1:", df1.shape)

#concatenating with the axis of one can be a little tricky because now we have multiple columns with the same name
#usually instead of concatenating like this we'd want to merge Our Data based on some similar columns. 
#merging Data on similar columns##1
merged_df1=pd.merge(df1,df2, on=["datetime"],suffixes=('_T','_H'))
print(merged_df1.head(5))
print("shape of merged df1:",merged_df1.shape)

merged_df2=pd.merge(df3,df4, on=["datetime"],suffixes=('_P','_W'))
print(merged_df2.head(5))
print("shape of merged df2:",merged_df2.shape)

merged_df_total=pd.merge(merged_df1, merged_df2, on=["datetime"])
print("shape of merged df total:",merged_df_total.shape)
print("head of merged df total:",merged_df_total.head(5))

#merging Data on similar columns##2
df1=df.groupby(["Airline", "FlightDate"])[["DepDelay"]].mean().reset_index()
df2=df.groupby(["Airline", "FlightDate"])[["ArrDelay"]].mean().rest_index()
df1.merge(df2) #this will take any similar columns between the two data sets and combine on those.
df1.merge(df2, how="inner") #we can also provide it a different merging type like left, right, inner