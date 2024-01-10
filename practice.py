import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from encodings.aliases import aliases
df_crime = pd.read_csv("state_crime.csv", encoding="ISO-8859-11")
#Are there any noticeable pattern or trends in property crime and violent crime rate from 1960 to 2019?
#df_crime_property_violent=df_crime.groupby(["Year", "State"])[["Data.Rates.Property.All", "Data.Rates.Violent.All"]].mean().reset_index()
#correlation_matrix=df_crime_property_violent.corr()
#print("Correlation Matrix:\n", correlation_matrix) #Display the correlation matrix (the Pearson correlation coefficient) that is 0.82, indicating a strong positive correlation.
plt.figure(figsize=(10,8))
scatter_plot=sns.scatterplot(x="Data.Rates.Property.All", y="Data.Rates.Violent.All",hue="Year", data=df_crime, legend="full", palette="viridis")
scatter_plot.legend(loc="center left",bbox_to_anchor=(1,0.5), title="Year")
#plt.xlim(df_crime_property_violent["Year"].min(), df_crime_property_violent["Year"].max())
plt.xlabel("Property Crime Rate")
plt.ylabel("Violent Crime Rate")
plt.title("Scatter Plot of Property and violent Crime ")
plt.show()
print("Data.Rates.Violent.All:", df_crime["Data.Rates.Violent.All"].max())

#pd.set_option("display.max_columns", None) 
#df_years_by_state=df_crime.groupby("State")["Year"].unique().reset_index()

#print("years available for each state:", df_years_by_state)
#check if all states have the same years
#same_years=all(np.array_equal(df_years_by_state.iloc[0],years) for years in df_years_by_state)
#print("All states have the same years:", same_years)