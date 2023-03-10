#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Dependencies
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hvplot.pandas
from scipy.stats import linregress


# In[2]:


#Read in layoff csv data and show
layoff_DF = pd.read_csv("Resources/layoffs_data.csv")
citiesUS_DF = pd.read_csv("Resources/cities_us.csv")
layoff_DF


# In[3]:


#Clean data to only focus on Countries headquartered in the United States
US_layoff_DF = layoff_DF.loc[layoff_DF["Country"]=="United States"]

#Show the data
US_layoff_DF


# In[4]:


#adjust city names to make sure they are found when merging of datasets
replaceData = US_layoff_DF.replace("SF Bay Area" , "San Francisco")
replaceData = replaceData.replace("Washington D.C.","Washington")
replaceData = replaceData.replace("New York City","New York")
renameCity = citiesUS_DF.rename(columns = {"city_ascii": "Location_HQ"})


# A) The location HQ is not US only (e.g: Sao Paulo, Beijing, Berlin). 
# 
# Solution: merge with cities_us.csv (link: https://www.kaggle.com/datasets/sergejnuss/united-states-cities-database) and drop any cities that is not in US.
# 
# 
# B) There are many cities in US that have global names, such as Vancouver, WA. 
# 
# C) There are many cities in US with duplicated names, such as Portland, Oregon and Portland, Maine. 
# 
# Solution: use only ranking 1 cities.
# (we lost 48 cities , such as Berlin in New Hampshire, London in Kentucky and Boulder Colorado. However, with 1 and 2 ranking we lost approx. 20 entries(e.g.: London in Kentucky, Toronto in Ohio, Vancouver in WA and San Luis Obispo in California), but got around 20 duplicated cities)

# In[5]:


# filter the cities file to prevent duplicated for the same city in different states when merging
renameCity = renameCity.loc[renameCity["ranking"] == 1.0]
renameCity.tail()


# In[6]:


#merge the 2 data sets on the "Location_HQ" column
mergedData = pd.merge(replaceData,renameCity,how="left", on=["Location_HQ"])
mergedData


# In[7]:


#drop columns that are not relevant
updated_mergedData= mergedData.drop(columns=['Percentage',"Source","Date_Added","List_of_Employees_Laid_Off","city","county_fips", "county_name","source","military","incorporated","timezone","zips","id","population", "density","ranking"])
updated_mergedData


# In[8]:


cleaned_mergedData = updated_mergedData.dropna()
cleaned_mergedData.head()

# should we remove line for drip company where funds raised equal to zero, if so either
# cleaned_mergedData = cleaned_mergedData.loc[cleaned_mergedData["Funds_Raised"] > 0] 
#cleaned_mergedData = cleaned_mergedData.loc[cleaned_mergedData["Funds_Raised"] !=0]


# In[9]:


#check for duplicates (such as same company, same number of lay offs - manually I found 5, different dates but some were close)


# In[10]:


#reset index
cleaned_mergedData = cleaned_mergedData.reset_index(drop=True)
cleaned_mergedData


# In[11]:


# export csv to double check - to be removed later
cleaned_mergedData.to_csv("cleaned_mergedData.csv", index_label="Company")


# ## Question 1: Which industries have the most layoffs for the years 2022 and 2023?
# #### Team Members: Ratima Chowadee, Lorena Egea

# In[12]:


# companies count
companies_count = len(cleaned_mergedData["Company"].unique())
companies_count


# In[13]:


US_layoffNew = cleaned_mergedData.copy()

# split Date column to get Year
split_date = [row.split('/') for row in US_layoffNew['Date']]
split_date = pd.DataFrame(split_date)
split_date = [row.split(' ') for row in split_date[2]]
split_date = pd.DataFrame(split_date)
split_date[0]
US_layoffNew['Year'] = split_date[0]
US_layoffNew

US_layoffNew = US_layoffNew[['Company', 'Location_HQ', 'Industry', 'Laid_Off_Count', 'state_id', 'state_name', 'Year']]
US_layoffNew


# In[14]:


count_by_industry = US_layoffNew.groupby('Industry')['Laid_Off_Count'].sum().sort_values(ascending=False)
count_by_industry


# In[15]:


layoffs_by_year = US_layoffNew.groupby('Year').sum()['Laid_Off_Count']
layoffs_by_year = pd.DataFrame(layoffs_by_year)

print(layoffs_by_year)

layoffs_by_year.plot.pie(y= 'Laid_Off_Count', figsize=(5, 5), )


# In[16]:


# find total laid off for 2020 by industry
data2020df = US_layoffNew.loc[US_layoffNew['Year'] == '2020']
total_2020lay = data2020df.groupby(['Industry']).sum()['Laid_Off_Count']
total_2020layDF = pd.DataFrame(total_2020lay)

# print(total_2020layDF)

# find total laid off for 2021 by industry
data2021df = US_layoffNew.loc[US_layoffNew['Year'] == '2021']
total_2021lay = data2021df.groupby(['Industry']).sum()['Laid_Off_Count']
total_2021layDF = pd.DataFrame(total_2021lay)
# print(total_2021layDF)

# find total laid off for 2022 by industry
data2022df = US_layoffNew.loc[US_layoffNew['Year'] == '2022']
total_2022lay = data2022df.groupby(['Industry']).sum()['Laid_Off_Count']
total_2022layDF = pd.DataFrame(total_2022lay)
# print(total_2022layDF)

# find total laid off for 2023 by industry
data2023df = US_layoffNew.loc[US_layoffNew['Year'] == '2023']
total_2023lay = data2023df.groupby(['Industry']).sum()['Laid_Off_Count']
total_2023layDF = pd.DataFrame(total_2023lay)
# print(total_2023layDF)


plt.figure(figsize=(20, 40))

plt.subplot(4,1,1)
plt.bar(total_2020layDF.index, total_2020layDF['Laid_Off_Count'], color='r', alpha=0.5, align="center")
plt.xticks(total_2020layDF.index, rotation="45", fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("Number of Layoffs", fontsize=16)
plt.title("2020", fontsize=18)

plt.subplot(4,1,2)
plt.bar(total_2021layDF.index, total_2021layDF['Laid_Off_Count'], color='r', alpha=0.5, align="center")
plt.xticks(total_2021layDF.index, rotation="45", fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("Number of Layoffs", fontsize=18)
plt.title("2021", fontsize=18)

plt.subplot(4,1,3)
plt.bar(total_2022layDF.index, total_2022layDF['Laid_Off_Count'], color='r', alpha=0.5, align="center")
plt.xticks(total_2022layDF.index, rotation="45", fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("Number of Layoffs", fontsize=18)
plt.title("2022", fontsize=18)

plt.subplot(4,1,4)
plt.bar(total_2023layDF.index, total_2023layDF['Laid_Off_Count'], color='r', alpha=0.5, align="center")
plt.xticks(total_2023layDF.index, rotation="45", fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel("Number of Layoffs", fontsize=18)
plt.title("2023", fontsize=18)

plt.suptitle('Layoffs Per Industries in 2020-2023', fontsize = 25)
plt.show()


# ## Question  2: Is there a correlation between the US state and the layoff rate? Which state has the most layoffs?
# #### Team Members: Toyin Olaye, Leslie Trejo, Camilla Inhapim

# In[ ]:





# In[ ]:





# ## Question 3: Do companies have more layoffs pre-IPO or post-IPO?
# #### Team Members: Julie Tang, Sam Gantman

# In[17]:


Pre_Post_data = cleaned_mergedData.loc[cleaned_mergedData["Stage"]!="Unknown"]
Pre_Post_data


# In[18]:


#Get rid of of rows with Stage= "Unknown"
cleaned_mergedData = cleaned_mergedData[cleaned_mergedData["Stage"] != "Unknown"]
Pre_Post_data = cleaned_mergedData["Stage"].unique()


# In[19]:


Pre_Post_data = cleaned_mergedData[cleaned_mergedData["Stage"] != "Unknown"]
grouped_Pre_Post= Pre_Post_data.groupby("Stage").sum("Laid_Off_Count")

grouped_Pre_Post


# In[23]:


#Pie Chart of Total Laid_Off_count for all Stages
labels = grouped_Pre_Post.index
plt.pie(grouped_Pre_Post["Laid_Off_Count"],labels=labels, rotatelabels=True)


# In[24]:


plt.barh(labels, width=grouped_Pre_Post["Laid_Off_Count"])


# In[25]:


#Look at Post-IPO companies
Post_IPO_companies = Pre_Post_data.loc[Pre_Post_data["Stage"]=="Post-IPO"] #& "2023" in Pre_Post_data["Date"]]
sorted_post_ipo_companies=Post_IPO_companies.sort_values("Laid_Off_Count",ascending=False).reset_index()
top10 = sorted_post_ipo_companies.iloc[0:10,:]
top10
#plt.barh(top10["Company"], width=top10["Laid_Off_Count"])


# In[26]:


#Drop everything but company, Laid_Off_Count, and Stage
q3_data = cleaned_mergedData[["Company", "Laid_Off_Count", "Stage"]]
#d3_data = d3_data.drop(['index', 'Location_HQ', 'Industry', 'Date', 'Funds_Raised', 'State_id', 'state_id', 'state_name', 'lat', 'lng'], axis=1)


# In[27]:


q3_data


# In[28]:


company_layoff_counts= q3_data.groupby("Company").sum()["Laid_Off_Count"]
company_layoff_counts


# In[29]:


#top 10 companies with highest amount in layoffs after group by

#top_10 = company_layoff_counts.sort_values("Laid_Off_Count", ascending=False).head(10)

#print(top_10)
top10= q3_data.groupby("Company").sum()["Laid_Off_Count"]
top10= company_layoff_counts.sort_values(ascending=False).reset_index()
top10


# In[30]:


#Plot top 10 companies with layoffs
top10


# In[31]:


#Plot top 10 companies with layoffs
labels = top10.iloc[0:10,0]
plt.bar(range(0,10), top10.iloc[0:10,1])
plt.xticks(range(0,10),labels,rotation="vertical")


# In[32]:


plt.barh(labels, width= top10["Laid_Off_Count"])


# In[33]:


#q3_data_cleaned = q3_data[q3_data["Stage"]!= "Unknown"]
#q3_data_cleaned = q3_data[q3_data["Stage"]!= "Post-IPO"]
#q3_data_cleaned = q3_data[q3_data["Stage"]!= "Acquired"]
#stage_preipo_layoffs = q3_data_cleaned.groupby("Stage").sum["Laid_Off_Count"]
#stage_preipo_layoffs = stage_preipo_layoffs.sort_values(ascending=False).reset_index()
#stage_preipo_layoffs
# Filter out rows with "Unknown", "Post-IPO", and "Acquired" values in the "Stage" column
q3_data_cleaned = q3_data[q3_data["Stage"].isin(["Seed", "Series A", "Series B", "Series C", "Series D","Series E", "Series F","Series G", "Series H", "Series I"])]
# Group the cleaned data by "Stage" and calculate the sum of "Laid_Off_Count"
stage_preipo_layoffs = q3_data_cleaned.groupby("Stage").sum()["Laid_Off_Count"].reset_index()
# Sort the resulting series in descending order and reset the index
#stage_preipo_layoffs = stage_preipo_layoffs.sort_values(ascending=False).reset_index()

stage_preipo_layoffs


# In[34]:


labels = stage_preipo_layoffs.iloc[0:10,0]
plt.barh(labels, width= stage_preipo_layoffs["Laid_Off_Count"])


# In[35]:


plt.pie(stage_preipo_layoffs["Laid_Off_Count"],labels=labels)


# In[36]:



q3_data_cleaned = q3_data[q3_data["Stage"].isin(["Post-IPO", "Private Equity","Seed", "Series A", "Series B", "Series C", "Series D","Series E", "Series F","Series G", "Series H", "Series I"])]
# Group the cleaned data by "Stage" and calculate the sum of "Laid_Off_Count"
stage_layoffs = q3_data_cleaned.groupby("Stage").sum()["Laid_Off_Count"].reset_index()
# Sort the resulting series in descending order and reset the index
#stage_preipo_layoffs = stage_preipo_layoffs.sort_values(ascending=False).reset_index()

stage_layoffs


# In[39]:


#Plot Stage comparison
labels = ["Post-IPO","Pre-IPO"]
plt.bar([0,1], [stage_layoffs["Laid_Off_Count"][0],sum(stage_layoffs["Laid_Off_Count"][1:11])])
plt.xticks([0,1],labels,rotation=45)
plt.ylabel("Number of Layoffs")
plt.xlabel("Stage")
plt.title("Layoffs Comparison for Pre vs. Post IPO Companies")


# In[53]:


#find the sum of non-ipo lay offs
sum(stage_layoffs["Laid_Off_Count"][1:11])
#


# In[62]:


frequencies =[(144930/(144930+53041)), (53041/(144930+53041))]


# In[65]:


stage_layoffs = plt.bar(np.arange(len(frequencies)), frequencies)
labels = ["Post-IPO","Pre-IPO"]
plt.bar([0,1], [stage_layoffs["Laid_Off_Count"][0],sum(stage_layoffs["Laid_Off_Count"][1:11])])
plt.xticks([0,1],labels,rotation=45)
plt.ylabel("Number of Layoffs")
plt.xlabel("Stage")
plt.title("Layoffs Comparison for Pre vs. Post IPO Companies")
for rect1 in stage_layoffs:
    height = rect1.get_height()
    plt.annotate( "{}%".format(height),(rect1.get_x() + rect1.get_width()/2, height+.05),ha="center",va="bottom",fontsize=15)

plt.show()


# In[72]:



frequencies =[73.2, 26.79]
labels = ["Post-IPO", "Pre-IPO"]
x = np.arange(len(labels))
fig, ax = plt.subplots()
ax.bar(x, frequencies, label="Laid Off Count")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("Number of Layoffs")
ax.set_xlabel("Stage")
ax.set_title("Layoffs Comparison for Pre vs. Post IPO Companies")

# Annotate each bar with the percentage value
for rect in ax.patches:
    height = rect.get_height()
    ax.annotate(f"{height}%", (rect.get_x() + rect.get_width() / 2, height + 1), ha="center", va="bottom", fontsize=15)


plt.show()


# ## Question 4: Does the amount of funds raised impact the layoff rates?
# #### Team Members: Taylor Gibson, Arthi Ranganathan

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




