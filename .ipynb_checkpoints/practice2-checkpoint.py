import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_crime = pd.read_csv("state_crime.csv", encoding="ISO-8859-11")

# Increase figure size
plt.figure(figsize=(12, 8))

# Scatter plot without grouping
scatter_plot = sns.scatterplot(x="Data.Rates.Property.All", y="Data.Rates.Violent.All", hue="Year", data=df_crime, palette="viridis")

# Move legend outside the plot and adjust its size and font size
scatter_plot.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Year", fontsize='small')

# Display every n years in the legend
#n = 5 # You can adjust this value based on your preference
#legend_labels = df_crime["Year"].unique()[::n]
#scatter_plot.set_xticks(legend_labels)
#plt.xticks(rotation=45)
# Adjust font size of x and y labels
plt.xlabel("Property Crime Rate", fontsize='medium')
plt.ylabel("Violent Crime Rate", fontsize='medium')

# Title and axis label font size
plt.title("Scatter Plot of Property and Violent Crime", fontsize='large')

plt.show()