# Import Matplotlib, pandas, and plotly
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


df1 = pd.read_csv("data/brasil-real-estate-1.csv")
df1.head()
df1.info()


df1.dropna(inplace=True)
df1.info()


#here i previously did mistake 
#df1[["lat", "lon"]] = df1["lat-lon"].str.split(",",expand = True).head() , this only splited 5 values rest are NaN
#after that i dropped lat-lon now how to recover in this platform??
#here redo all step from first i.e. reload df in df1 and do cleaning process
#if same accident happen in other id repeat same process and it's better to keep copy of original df
df1[["lat", "lon"]] = df1["lat-lon"].str.split(",",expand = True)# double[[]] is used to make 2 variable
df1.head()
df1.info()
#here in output below lat and lon column is object datatype so converting its datatype to float
df1["lat"]=df1["lat"].astype(float)
df1.info()


df1["lon"]=df1["lon"].astype(float)
df1.info()


df1["state"] = df1["place_with_parent_names"].str.split("|",expand = True)[2]
df1.head()
df1.info()


df1["price_usd"]=df1["price_usd"].str.replace("$","",regex=False).str.replace(",","",regex=False).astype(float)
df1.info()


df1.drop(columns=["place_with_parent_names","lat-lon"],inplace= True) 
df1.info()


df2 = pd.read_csv("data/brasil-real-estate-2.csv")
df2.info()
df2.head()



#1 USD = 5.47 Brazilian Real
df2["price_usd"] = (df2["price_brl"] / 19).round(2)
df2.head()
df2.info()


df2.drop(columns = ["price_brl"],inplace = True)
df2.dropna(inplace = True)
df2.info()


df = df =pd.concat([df1,df2]) 
print("df shape:", df.shape)
df.to_csv("data/brasil-real-estate-clean.csv",index=False)


df= pd.read_csv("data/brasil-real-estate-clean.csv")
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
                                   #plt.subplot( ) is used to display 1 plot only
)                  
#fig,(ax1,ax2) = plt.subplot(1,2) is used to display 2 plot side by side
#ax1. is used for 1st variable plot,ax2. is used for 2nd variable plot
# Build histogram
ax.hist(df["area_m2"])
# Label axes
ax.set_xlabel("Area[sq meter]")
ax.set_ylabel("Frequency")
# Add title
ax.set_title("Distribution of home size")
#for price
# Build histogram
ax.hist(df["price_usd"])
# Label axes
ax.set_xlabel("Price[USD]")
ax.set_ylabel("Frequency")
# Add title
ax.set_title("Distribution of home Price")


# Don't change the code below 👇
fig, ax = plt.subplots()
#Build box plot
ax.boxplot(df["area_m2"],vert= False)
# Label axes
ax.set_xlabel("Area[sq meter]")
# Add title
ax.set_title("Distribution of home size")
#for price_usd column:
#Build box plot
ax.boxplot(df["price_usd"],vert= False)
# Label axes
ax.set_xlabel("Price[USD]")
# Add title
ax.set_title("Distribution of home price")


mean_price_by_region = df.groupby("region")["price_usd"].mean().sort_values(ascending=False)
mean_price_by_region


# Don't change the code below 👇
fig, ax = plt.subplots()
# Build bar chart, label axes, add title
mean_price_by_region.plot(
    kind="bar",
    xlabel="region",
    ylabel="Mean Price (USD)",
    title="Mean house Price by region",
    ax=ax
)


#this hint suggest make subset dataset for south and south is region name
df_south = df[df["region"]=="South"]
df_south.head()


homes_by_state = df_south["state"].value_counts()        #home_by_state means how many home are there in each state?
homes_by_state                                           #this is found by counting values


#here this hint suggest to make subset dataset of dataset df_south based on state rgs
#maybe rgs is abbreviation of Rio Grande do Sul
# # Subset data
df_south_rgs = df_south[df_south["state"] == "Rio Grande do Sul"]
df_south_rgs.head()
# Don't change the code below 👇
fig, ax = plt.subplots()
# Build scatter plot
ax.scatter(x=df_south_rgs["area_m2"] , y=df_south_rgs["price_usd"])
# Label axes
ax.set_xlabel("Area[sq meter]")
ax.set_ylabel("Price[USD]")
# Add title
ax.set_title("Rio Grande do Sul: Price vs. Area")


south_states_corr = df_south_rgs["area_m2"].corr(df_south_rgs["price_usd"])
south_states_corr




