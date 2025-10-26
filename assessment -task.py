#In the last project, you learned data wrangling and visualization skills while examining the real estate market in Mexico.
# In this project, you'll build on those skills and move from descriptive to predictive data science. 
# Your focus is still real estate, but now you need to create a machine learning model that predicts apartment prices in Buenos Aires, Argentina.




# Import Matplotlib, pandas, and plotly
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


df1 = pd.read_csv("data/brasil-real-estate-1.csv")
df1.head()
df1.info()

df1.dropna(inplace=True)
df1.info()
df1.head()

df1[["lat", "lon"]] = df1["lat-lon"].str.split(",",expand = True)# double[[]] is used to make 2 variable

#here in output below: lat and lon column is object datatype so converting its datatype to float
df1["lat"]=df1["lat"].astype(float)

df1["lon"]=df1["lon"].astype(float)
df1.info()
df1.head()

df1["state"] = df1["place_with_parent_names"].str.split("|",expand = True)[2]
df1.head()

df1["price_usd"]=df1["price_usd"].str.replace("$","",regex=False).str.replace(",","",regex=False).astype(float)
df1.info()
df1.head()

df1.drop(columns=["place_with_parent_names","lat-lon"],inplace= True) 

#dropna() don't reset the index . It just drop null values but index of other entries remains same
#output: Int64Index: 11551 entries, 0 to 12833

# df1 = df1.reset_index(drop=True)   #RangeIndex: 11551 entries, 0 to 11550
# #But the grader wants no change in index here

df1.info()
df1.head()

df2 = pd.read_csv("data/brasil-real-estate-2.csv")
df2.info()
df2.head()

#1 USD = 3.19 Brazilian Real
df2["price_usd"] = (df2["price_brl"] / 3.19).round(2)
df2.head()


df2.drop(columns = ["price_brl"],inplace = True)
df2.dropna(inplace = True)

# #output: Int64Index: 11293 entries, 0 to 12832

# df2 = df2.reset_index(drop=True)   #RangeIndex: 11293 entries, 0 to 11292
# # But the grader wants no change in index here

df2.info()
df2.head()


df = df =pd.concat([df1,df2]) 
print("df shape:", df.shape)
#df.to_csv("data/brasil-real-estate-clean.csv",index=False)
df.info()
df.head()

fig = px.scatter_mapbox(
    df,
    lat="lat", 
    lon="lon", 
    center={"lat": -14.2, "lon": -51.9},  # Map will be centered on Brazil
    width=600,
    height=600,
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)
fig.update_layout(mapbox_style="open-street-map")
fig.show()


summary_stats = df[["area_m2","price_usd"]].describe()
summary_stats

# Don't change the code below 👇
fig, ax = plt.subplots(
) 
# Build histogram
ax.hist(df["price_usd"].head(20000), bins=10)
# Label axes
ax.set_xlabel("Price [USD]")
ax.set_ylabel("Frequency")
# Add title
ax.set_title("Distribution of Home Prices");

# # Use Matplotlib to create histogram of "price_usd"
# plt.hist(df["price_usd"].head(20000))
# # Add x-axis label
# plt.xlabel("Price[USD]")
# # Add y-axis label
# plt.ylabel("frequency")
# # Add title
# plt.title("Distribution of home price");


# Don't change the code below 👇
fig, ax = plt.subplots()
#Build box plot
ax.boxplot(df["area_m2"],vert= False)
# Label axes
ax.set_xlabel("Area [sq meters]")
# Add title
ax.set_title("Distribution of Home Sizes");



mean_price_by_region = df.groupby("region")["price_usd"].mean().sort_values(ascending=True)
mean_price_by_region


# Don't change the code below 👇
fig, ax = plt.subplots()
# Build bar chart, label axes, add title
mean_price_by_region.plot(
    kind="bar",
    xlabel="Region",
    ylabel="Mean Price [USD]",
    title="Mean Home Price by Region",
    ax=ax
);

df_south = df[df["region"]=="South"]
df_south.head()

homes_by_state = df_south["state"].value_counts()       
homes_by_state 

# # Subset data
df_south_rgs = df_south[df_south["state"] == "Rio Grande do Sul"]
df_south_rgs.head()
# Don't change the code below 👇
fig, ax = plt.subplots()
# Build scatter plot
ax.scatter(x=df_south_rgs["area_m2"] , y=df_south_rgs["price_usd"])
# Label axes
ax.set_xlabel("Area [sq meters]")
ax.set_ylabel("Price [USD]")
# Add title
ax.set_title("Rio Grande do Sul: Price vs. Area");


df_south["state"].unique()
#array(['Paraná', 'Rio Grande do Sul', 'Santa Catarina'], dtype=object)

#Create an empty dictionary
south_states_corr = {}

# List of South region states
south_states = ["Paraná", "Santa Catarina", "Rio Grande do Sul"]

# Loop through each state
for state in south_states:
    # Subset data for that state
    df_state = df[df["state"] == state]
    
    # Calculate correlation between area_m2 and price_usd
    corr_value = df_state["area_m2"].corr(df_state["price_usd"])
    
    # Add to dictionary
    south_states_corr[state] = corr_value

# Display the dictionary
south_states_corr


