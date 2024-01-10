import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
colors = ["#89CFF0", "#FF69B4", "#FFD700", "#7B68EE", "#FF4500",
          "#9370DB", "#32CD32", "#8A2BE2", "#FF6347", "#20B2AA",
          "#FF69B4", "#00CED1", "#FF7F50", "#7FFF00", "#DA70D6"]

df_crime=pd.read_csv("/home/heewa/Desktop/portfolio_crime_projects/state_crime.csv", encoding="ISO-8859-11")

#Are there any noticeable pattern or trends in property and violent crime rate from 1960 to 2019?

average_property_violent_crime=df_crime.groupby("Year")[["Data.Rates.Property.All", "Data.Rates.Violent.All"]].mean()
#plotting the trend
sns.set(style="darkgrid")
plt.figure(figsize=(10,6))
sns.lineplot(x=average_property_violent_crime.index, y=average_property_violent_crime["Data.Rates.Property.All"],color="darkgreen",marker="*",markersize=8,label="Average Property Crime Rate")
sns.lineplot(x=average_property_violent_crime.index, y=average_property_violent_crime["Data.Rates.Violent.All"],color="darkviolet",marker="o",markersize=6,label="Average Violent Crime Rate")
plt.title("Average Crime Rate Over the Years")
plt.xlabel("Years")
plt.ylabel("Average Crime Rate")
plt.legend()
plt.show() 


#Are there any noticeable correlation between property crime and violent crime rates?
limited_df_crime=df_crime[df_crime["Year"]][["State","Year","Data.Rates.Property.All","Data.Rates.Violent.All" ]]
print(limited_df_crime.head(3))
plt.figure(figsize=(12, 8))
sns.scatterplot(x="Data.Rates.Property.All", y="Data.Rates.Violent.All", hue="Year", data=limited_df_crime, palette="viridis")
plt.xlabel("Property Crime Rate", fontsize='medium')
plt.ylabel("Violent Crime Rate", fontsize='medium')
plt.title("Scatter Plot of Property and Violent Crime", fontsize='large')
plt.show()





# Assuming df_crime is your DataFrame with columns including "Year", "Data.Rates.Property.All", "Data.Rates.Violent.All", and "State"

#Looking at the most recent years(2010-2019)'property crime rates

recent_years_df = df_crime[df_crime["Year"].between(2010, 2019)] # Filter the data for the years 2010-2019
heatmap_data = recent_years_df.pivot_table(index="Year", columns="State", values="Data.Rates.Property.All").sort_index(ascending=False) # Creating a pivot table to prepare data for heatmap
plt.figure(figsize=(24, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", linewidths=0.5, cbar_kws={'label': 'Property Crime Rate'}, annot=False)
plt.xlabel('State', weight="bold",fontsize=12)
plt.ylabel('Year', weight="bold",fontsize=12)
plt.xticks(rotation=80, fontsize=7)
plt.yticks(rotation=0,fontsize=8)
plt.subplots_adjust(bottom=0.2)
plt.show()


#Looking at the most recent years(2010-2019)'violent crime rates
heatmap_data = recent_years_df.pivot_table(index="Year", columns="State", values="Data.Rates.Violent.All").sort_index(ascending=False) # Creating a pivot table to prepare data for heatmap
plt.figure(figsize=(24, 8))
sns.heatmap(heatmap_data, cmap="Reds", linewidths=0.5, cbar_kws={'label': 'Violent Crime Rate'}, annot=False)
plt.xlabel('State', weight="bold", fontsize=12)
plt.ylabel('Year', weight="bold",fontsize=12)
plt.xticks(rotation=80, fontsize=7)
plt.yticks(rotation=0,fontsize=8)
plt.subplots_adjust(bottom=0.2)
plt.show()




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