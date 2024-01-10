import os
print(os.getcwd())

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_crime = pd.read_csv("/home/heewa/Desktop/portfolio_crime_projects/state_crime.csv", encoding="ISO-8859-11")
limited_df_crime=df_crime[df_crime["Year"]>2000][["State","Year","Data.Rates.Property.All","Data.Rates.Violent.All" ]]
print(limited_df_crime.head(3))
plt.figure(figsize=(12, 8))
sns.scatterplot(x="Data.Rates.Property.All", y="Data.Rates.Violent.All", hue="Year", data=limited_df_crime, palette="viridis")
plt.xlabel("Property Crime Rate", fontsize='medium')
plt.ylabel("Violent Crime Rate", fontsize='medium')
plt.title("Scatter Plot of Property and Violent Crime", fontsize='large')
plt.show()


mean_std_per_year=df_crime.groupby("Year")[["Data.Rates.Property.All","Data.Rates.Violent.All" ]].agg(["mean","std"]) # Calculate mean and standard deviation for each year
def calculate_z_score(row, column_name):
    mean=mean_std_per_year.loc[row["Year"],(column_name,"mean")]
    std_dev=mean_std_per_year.loc[row["Year"],(column_name,"std")]
    z_score=(row[column_name]-mean)/std_dev
    return z_score
df_crime["Z_Score_Property"]=df_crime.apply(lambda row: calculate_z_score(row,"Data.Rates.Property.All"), axis=1) #Apply the function to create a new column "Z_Score_Property"
df_crime["Z_Score_Violent"]=df_crime.apply(lambda row: calculate_z_score(row,"Data.Rates.Violent.All"), axis=1) #Apply the function to create a new column "Z_Score_Violent"


# Identifying outliers based on a threshold(e.g., consider z_score greater than 2)
outliers=df_crime[df_crime["Z_Score_Property"].abs()>3] 
print("Outliers based on Z-score for property:")
print(outliers[["State","Year", "Data.Rates.Property.All","Z_Score_Property"]])
outliers=df_crime[df_crime["Z_Score_Property"].abs()>2] 
print("Outliers based on Z-score for property:")
print(outliers[["State","Year", "Data.Rates.Property.All","Z_Score_Property"]])
z_score_threshold=2
filtered_df_crime=df_crime[(df_crime["Z_Score_Property"].abs() <= z_score_threshold)&(df_crime["Z_Score_Violent"].abs() <= z_score_threshold)]
plt.figure(figsize=(12, 8))
sns.scatterplot(x="Data.Rates.Property.All", y="Data.Rates.Violent.All", hue="Year", data=filtered_df_crime, palette="viridis")
plt.xlabel("Property Crime Rate", fontsize='medium')
plt.ylabel("Violent Crime Rate", fontsize='medium')
plt.title("Scatter Plot of Property and Violent Crime", fontsize='large')
plt.show()

average_property_crime_by_state=df_crime.groupby("State")["Data.Rates.Property.All"].mean()
average_violent_crime_by_state=df_crime.groupby("State")["Data.Rates.Violent.All"].mean()
#Identify states with high or low averages:
top_states_property=round(average_property_crime_by_state,2).nlargest(5,keep="all")
bottom_states_property=average_property_crime_by_state.nsmallest(5,keep="all")
top_states_violent=average_violent_crime_by_state.nlargest(5,keep="all")
bottom_states_violent=average_violent_crime_by_state.nsmallest(5,keep="all")
print("States with high property  crime rate:\n", top_states_property)
print("States with low property crime rate:\n", bottom_states_property)
print("States with high violent  crime rate:\n", top_states_violent)
print("States with low violent crime rate:\n", bottom_states_violent)
