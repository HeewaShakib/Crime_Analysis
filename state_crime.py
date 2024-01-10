import os
print("os:", os.getcwd())
#Import all the necessary libraries
import pandas as pd
#pd.options.display.float.format="{:,.2f}".format
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from encodings.aliases import aliases
colors = ["#89CFF0", "#FF69B4", "#FFD700", "#7B68EE", "#FF4500",
          "#9370DB", "#32CD32", "#8A2BE2", "#FF6347", "#20B2AA",
          "#FF69B4", "#00CED1", "#FF7F50", "#7FFF00", "#DA70D6"]


# Find encodings that work

# Below line creates a set of all available encodings
#df_crime=pd.read_csv("/home/heewa/Desktop/portfolio_crime_projects/state_crime.csv", encoding="ISO-8859-11")
alias_values = set(aliases.values())

for encoding in set(aliases.values()):
    try:
        df_crime=pd.read_csv("/home/heewa/Desktop/portfolio_crime_projects/state_crime.csv", encoding="ISO-8859-11") # read in only 10 lines for faster read
        print('successful', encoding)
    except:
        pass



# Read in the crime.csv file and use the timestamp as a datetime index
#df_crime = pd.read_csv("state_crime.csv", encoding="ISO-8859-11")
pd.set_option("display.max_columns", None) # set display options to show all columns
print("shape of the data:",df_crime.shape )# Checking the shape of the data.

#Explore the dataset
print(df_crime.head(5)) # Quick check of the beginning of the dataframe
print(df_crime.tail(5)) # # Quick check of the end of the dataframe
print(df_crime.sample(10)) # Quick check on how the dataset looks like

print("Duplicates:",df_crime.duplicated().sum()) # Counting the duplicate rows
print("Missing data:\n",df_crime.isnull().sum()) # checking missing data
print("info:\n", df_crime.info()) # Summary information about the dataframe
print("summary information on the numeric columns:\n",df_crime.describe()) # summary information on the numeric columns
print("summary information on the non_numeric columns:\n", df_crime.describe(include="object"))
print("Columns with no missing values:\n", df_crime.columns[np.sum(df_crime.isnull())==0])
print("Columns with missing values:\n", df_crime.columns[np.sum(df_crime.isnull())!=0])

#Potential questions to answer:
#How has the overall crime rate changed over time?
df_crime["Overall_crime_rate"]=df_crime["Data.Rates.Property.All"]+df_crime["Data.Rates.Violent.All"] #Creating a new column for the overall crime rate
crime_rate_grouped_by_year=df_crime.groupby("Year")
average_crime_rate=crime_rate_grouped_by_year["Overall_crime_rate"].mean()
#plotting
plt.plot(average_crime_rate.index,average_crime_rate.values,color="green", marker="o",linestyle="dashed", linewidth=1,markersize=5)
plt.title("Overall Crime Rate Over the Years")
plt.xlabel("Years")
plt.ylabel("Average Overall Crime Rate")
#plt.show()  

#Are there any noticeable pattern or trends in property crime and violent crime rate from 1960 to 2019?
df_crime_property_violent=df_crime[["Year", "Data.Rates.Property.All", "Data.Rates.Violent.All"]].copy()
average_grouped_df_crime_property=df_crime_property_violent.groupby("Year")[["Data.Rates.Property.All", "Data.Rates.Violent.All"]].mean()
#plotting the trend
sns.set(style="darkgrid")
plt.figure(figsize=(10,6))
sns.lineplot(x=average_grouped_df_crime_property.index, y=average_grouped_df_crime_property["Data.Rates.Property.All"],color="darkgreen",marker="*",markersize=8,label="Average Property Crime Rate")
sns.lineplot(x=average_grouped_df_crime_property.index, y=average_grouped_df_crime_property["Data.Rates.Violent.All"],color="darkviolet",marker="o",markersize=6,label="Average Violent Crime Rate")
plt.title("Average Crime Rate Over the Years")
plt.xlabel("Years")
plt.ylabel("Average Crime Rate")
plt.legend()
#plt.show() 
#Calculate the correlation matrix
correlation_matrix=average_grouped_df_crime_property.corr()
print("Correlation Matrix:\n", correlation_matrix) #Display the correlation matrix (the Pearson correlation coefficient) that is 0.82, indicating a strong positive correlation.

#Are there any noticeable correlation between property crime and violent crime rates?
limited_df_crime=df_crime[df_crime["Year"]][["State","Year","Data.Rates.Property.All","Data.Rates.Violent.All" ]]
print(limited_df_crime.head(3))
plt.figure(figsize=(12, 8))
sns.scatterplot(x="Data.Rates.Property.All", y="Data.Rates.Violent.All", hue="Year", data=limited_df_crime, palette="viridis")
plt.xlabel("Property Crime Rate", fontsize='medium')
plt.ylabel("Violent Crime Rate", fontsize='medium')
plt.title("Scatter Plot of Property and Violent Crime", fontsize='large')
plt.show()


#States with consistently high or low crime rate
#Calculate average crime rate by state
average_property_crime_by_state=df_crime.groupby("State")["Data.Rates.Property.All"].mean()
average_violent_crime_by_state=df_crime.groupby("State")["Data.Rates.Violent.All"].mean()
#Identify states with high or low averages:
top_states_property=round(average_property_crime_by_state,2).nlargest(5,keep="all")
bottom_states_property=round(average_property_crime_by_state,2).nsmallest(5,keep="all")

top_states_violent=round(average_violent_crime_by_state,2).nlargest(5,keep="all")
bottom_states_violent=round(average_violent_crime_by_state,2).nsmallest(5,keep="all")

print("States with high property  crime rate:\n", top_states_property)
print("States with low property crime rate:\n", bottom_states_property)
print("States with high violent  crime rate:\n", top_states_violent)
print("States with low violent crime rate:\n", bottom_states_violent)

#Visualize states with consistently high or low crime rate
plt.figure(figsize=(20,6))
sns.set(style="whitegrid")
plt.subplot(1,2,1)
sns.barplot(x=top_states_property.index, y=top_states_property,color="darkgreen", label="Top States_Property Crime Rate")
sns.barplot(x=bottom_states_property.index, y=bottom_states_property,color="lightgreen", label="Bottom States_Property Crime Rate")
plt.xlabel("States", weight="bold", fontsize=10, labelpad=12)
plt.ylabel("Average Property crime Rate",weight="bold", fontsize=10, labelpad=12)
plt.xticks(rotation=45, ha="right",fontsize=10)
plt.legend(fontsize=8)
plt.subplot(1,2,2)
sns.barplot(x=top_states_violent.index, y=top_states_violent,color="darkviolet", label="Top States_Violent Crime Rate")
sns.barplot(x=bottom_states_violent.index, y=bottom_states_violent,color="pink", label="Bottom States_violent Crime Rate")
plt.xlabel("States", weight="bold", fontsize=10, labelpad=6)
plt.ylabel("Average Violent crime Rate",weight="bold", fontsize=10, labelpad=6)
plt.xticks(rotation=45, ha="right",fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=8)
plt.subplots_adjust(wspace=0.5, bottom=0.3)#adjust width space between subplots
#plt.show()

#Among property crimes, which specific type (burglary, larceny, motor_related) has the highest occurrence?
print(df_crime.columns)
property_crime_df=df_crime[['Data.Rates.Property.Burglary', 'Data.Rates.Property.Larceny', 'Data.Rates.Property.Motor']] #Select relevant columns for property crimes
total_property_crimes=property_crime_df.sum()
print("Total Property Crime:", total_property_crimes)
highest_property_crime_type=total_property_crimes.idxmax()
highest_property_crime_occurrence=total_property_crimes.max()
print(f"Among property crimes, {highest_property_crime_type} has the highest occurrence with {highest_property_crime_occurrence}")

#Visualizing the share of each type of property rate

property_shares=df_crime[['Data.Rates.Property.Burglary', 'Data.Rates.Property.Larceny','Data.Rates.Property.Motor']].sum()
property_shares.index=['Burglary','Larceny','Motor']
plt.figure(figsize=(8,8))
plt.pie(property_shares, labels=property_shares.index, colors=colors, autopct=lambda p: "{:.1f}%".format(p) if p>0 else '')
plt.title("Share of Property Crime Types",weight="bold",fontsize=12)
plt.show()

violent_shares=df_crime[['Data.Rates.Violent.Assault', 'Data.Rates.Violent.Murder','Data.Rates.Violent.Rape', 'Data.Rates.Violent.Robbery']].sum()
violent_shares.index=["Assault", "Murder", "Rape","Robbery"]
explode=(0.1,0,0,0)
plt.figure(figsize=(20,6))
plt.pie(violent_shares, labels=violent_shares.index, explode=explode, colors=colors, autopct=lambda p: "{:.1f}%".format(p) if p>0 else '')
plt.title("Share of Violent Crime Types",weight="bold",fontsize=12)
plt.show()

#Among violent crimes (assault, murder, rape, robbery), which type has the the highest occurrence?
violent_crime_df=df_crime[['Data.Rates.Violent.Assault', 'Data.Rates.Violent.Murder',
       'Data.Rates.Violent.Rape', 'Data.Rates.Violent.Robbery']]
total_violent_crimes=violent_crime_df.sum()
highest_violent_crime_type=total_violent_crimes.idxmax()
highest_violent_crime_occurrence=total_violent_crimes.max()
print(f"Among violent crimes, {highest_violent_crime_type} has the highest occurrence with {highest_violent_crime_occurrence}")



# Identifying outliers based on a threshold(e.g., consider z_score greater than 2)
mean_std_per_year=df_crime.groupby("Year")[["Data.Rates.Property.All", "Data.Rates.Violent.All"]].agg(["mean", "std"]) # Calculate mean and standard deviation for each year
def calculate_z_score(row,column_name):
    mean=mean_std_per_year.loc[row["Year"], (column_name,"mean")]
    std_dev=mean_std_per_year.loc[row["Year"],(column_name, "std")]
    z_score=(row[column_name]-mean)/std_dev
    return z_score
df_crime["Z_Score_Property"]=df_crime.apply(lambda row: calculate_z_score(row,"Data.Rates.Property.All"), axis=1) #Apply the function to create a new column "Z_Score"
df_crime["Z_Score_Violent"]=df_crime.apply(lambda row: calculate_z_score(row, "Data.Rates.Violent.All"), axis=1) #Apply the function to create a new column "Z_Score"
z_score_threshold=2
filtered_df_crime=df_crime[(df_crime["Z_Score_Property"].abs()<=z_score_threshold)& (df_crime["Z_Score_Violent"].abs()<=z_score_threshold)] #Filter out data point with high z_score
plt.figure(figsize=(10,6))
sns.scatterplot(x="Data.Rates.Property.All", y="Data.Rates.Violent.All", hue="Year", data=filtered_df_crime, palette="viridis")
plt.xlabel("Property Crime Rate")
plt.ylabel("Violent crime Rate")
plt.title("Scatter Plot of Property and Violent Crime Rate(after removing outliers with high z_score)")
plt.show()

#Identify states with high or low averages:
top_states_property=round(average_property_crime_by_state,2).nlargest(5,keep="all")
bottom_states_property=round(average_property_crime_by_state,2).nsmallest(5,keep="all")

top_states_violent=round(average_violent_crime_by_state,2).nlargest(5,keep="all")
bottom_states_violent=round(average_violent_crime_by_state,2).nsmallest(5,keep="all")

print("States with high property  crime rate:\n", top_states_property)
print("States with low property crime rate:\n", bottom_states_property)
print("States with high violent  crime rate:\n", top_states_violent)
print("States with low violent crime rate:\n", bottom_states_violent)



#Looking at the most recent years(2010-2019)'crime rates

recent_years_df = df_crime[df_crime["Year"].between(2010, 2019)] # Filter the data for the years 2010-2019
recent_years_df=recent_years_df.sort_values(by="Year") # sort the data by the "Year" in ascending order
heatmap_data = recent_years_df.pivot_table(index="Year", columns="State", values="Data.Rates.Property.All") # Creating a pivot table to prepare data for heatmap
plt.figure(figsize=(24, 8))
sns.heatmap(heatmap_data, cmap="YlOrRd", linewidths=0.5, cbar_kws={'label': 'Property Crime Rate'}, annot=False)
plt.xlabel('Year', weight="bold")
plt.ylabel('State', weight="bold")
plt.xticks(rotation=80, fontsize=7)
plt.yticks(rotation=0,fontsize=8)
plt.subplots_adjust(bottom=0.2)
plt.show()



