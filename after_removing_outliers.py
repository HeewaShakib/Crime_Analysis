import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
colors = ["#89CFF0", "#FF69B4", "#FFD700", "#7B68EE", "#FF4500",
          "#9370DB", "#32CD32", "#8A2BE2", "#FF6347", "#20B2AA",
          "#FF69B4", "#00CED1", "#FF7F50", "#7FFF00", "#DA70D6"]

df_crime=pd.read_csv("/home/heewa/Desktop/portfolio_crime_projects/state_crime.csv", encoding="ISO-8859-11")

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

#States with consistently high or low crime rate
#Calculate average crime rate by state
average_property_crime_by_state=df_crime.groupby("State")["Data.Rates.Property.All"].mean()
average_violent_crime_by_state=df_crime.groupby("State")["Data.Rates.Violent.All"].mean()

average_property_state_without_outliers=filtered_df_crime.groupby("State")["Data.Rates.Property.All"].mean()
average_violent_state_without_outliers=filtered_df_crime.groupby("State")["Data.Rates.Violent.All"].mean()
#Identify states with high or low averages:
top_states_property=round(average_property_crime_by_state,2).nlargest(10,keep="all").sort_values()
top_states_property_without_outliers=round(average_property_state_without_outliers,2).nlargest(10,keep="all").sort_values()

top_states_violent=round(average_violent_crime_by_state,2).nlargest(10,keep="all").sort_values()
top_states_violent_without_outliers=round(average_violent_state_without_outliers,2).nlargest(10,keep="all").sort_values()

print("States with high property  crime rate:\n", top_states_property)
print("States with high property crime rate without outliers:\n", top_states_property_without_outliers)
print("States with high violent  crime rate:\n", top_states_violent)
print("States with high violent crime rate without outliers:\n", average_violent_state_without_outliers)

