
# coding: utf-8

# In[2]:

# crunching data from DOE Global Energy Storage Database
# http://www.energystorageexchange.org/projects

get_ipython().magic('matplotlib inline')
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np
import pandas_profiling
import seaborn as sns
sns.set(color_codes=True)


# In[3]:

# load the excel file
root = "/Users/monnedepraetere/Documents/Python/1. projects/storage data/"
filename = "storageprojects.xls"
path = root + filename
df = pd.read_excel(path,sheetname = "Worksheet1",index_col=[0])
df = df[~df.index.duplicated(keep='last')] #remove duplicate project names
df = df.reset_index()
df = df.rename(columns=lambda x: x.strip()) #remove whitespace from column names

# fix duration datatype to float and filter out outliers  
df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce') #force duration as float datatype
#df = df[df['Duration']<20] #drop open loop hydro


# In[4]:

select_columns = ['Project Name','Technology Type','Technology Type Category 1','Technology Type Category 2'
                  ,'Rated Power in kW','Duration','Status','Service/Use Case 1',
                  'Service/Use Case 2','Service/Use Case 3','Country','Capital Expenditure $']

df = df[select_columns]


# In[5]:

# function to list all variables with unique values and datatype
get_ipython().magic('run "/Users/monnedepraetere/Google Drive/3. Coding/unique_col_values.py"')

# function to deliver unit count per type 
def agg_count(df, group_field):
    grouped = df.groupby(group_field, as_index=False).size()
    grouped.sort_values(ascending = False,inplace=True)
    grouped = pd.DataFrame(grouped).reset_index()
    grouped.columns = [group_field, 'Count']
    return grouped


# function to deliver sum per type 
def agg_sum(df, group_field,sum_field):
    grouped = df[sum_field].groupby(df[group_field]).sum()
    grouped.sort_values(ascending = False,inplace=True)
    grouped = pd.DataFrame(grouped).reset_index()
    grouped.columns = [group_field, sum_field]
    return grouped


# In[6]:

unique_col_values(df)


# In[24]:

#pandas_profiling.ProfileReport(df)

#exclude pumped hydro
df = df[df['Technology Type Category 2']<>'Pumped Hydro Storage']

#calculate total capacity and units per technology type
plt.style.use('ggplot')
fig0, (ax0,ax1) = plt.subplots(nrows=1,ncols=2,figsize=(8,3),sharey=True)

tech_cap = agg_sum(df,'Technology Type Category 2','Rated Power in kW')
tech_cap['Rated Power in GW']= tech_cap['Rated Power in kW'] / 1000000
tech_count = agg_count(df,'Technology Type Category 2')
stats_by_tech = pd.merge(tech_count,tech_cap,on='Technology Type Category 2')


stats_by_tech.plot(kind='barh',ax=ax0,y='Count',x='Technology Type Category 2')
ax0.set(title ='Count of storage project by type', xlabel ='Count',ylabel='Technology type')
ax0.legend().set_visible(False)

stats_by_tech.plot(kind='barh',ax=ax1,y='Rated Power in GW',x='Technology Type Category 2')
ax1.set(title ='Total storage rated power by type', xlabel ='Rated power (GW)',ylabel='Technology type')
ax1.legend().set_visible(False)


# In[33]:

# Plot duration per technology type

median_duration = df['Duration'].groupby(df['Technology Type Category 2']).median().sort_values(axis=0, ascending=True)
#plt.style.available
plt.style.use('ggplot')
fig1, ax1 = plt.subplots(nrows=1,ncols=1,figsize=(4,2))
median_duration.plot(kind='barh',ax=ax1)
ax1.set(title ='Median duration per high-level technology type', xlabel ='Duration (Hours)',ylabel='Technology type')
ax1.set_xlim([0,10])


# In[ ]:




# In[35]:

#plot duration
duration = df['Duration'].dropna().tolist()
sns.distplot(duration)
sns.plt.xlim(0,10)


# In[ ]:




# In[ ]:




# In[64]:




# In[8]:

get_ipython().system('pwd')


# In[ ]:




# In[ ]:




# In[ ]:




# In[36]:

# examine status

# get capacity by status
df_group = df.groupby([df['Status']])
status = df_group['Rated Power in kW'].sum()

# plot bar chart
fig1, ax1 = plt.subplots()
fig1.subplots_adjust(top=0.85)
ax1.set_title('Storage projects capacity by status (kW)')
width = 0.5
ax1.bar(np.arange(6),status,width)
ax1.set_xticklabels(status.index)
ax1.set_xticks(np.arange(6)+width/2)
ax1.set_ylabel('Capacity (kW)')
#ax1.get_yaxis().set_major_formatter(
#    plt.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.xticks(rotation=90)
plt.show()


# In[59]:

# look at the technology split

#focus on operational projects only
dfop = df.loc[df['Status']=='Operational']
dfop_group = dfop.groupby([dfop['Technology Type Category 2']])
technologies = dfop_group['Rated Power in kW'].sum()


# In[ ]:




# In[60]:

fig2, ax1 = plt.subplots()
fig1.suptitle("Almost all global storage capacity is pumped hydro", 
              fontsize=14, fontweight='bold')
fig1.subplots_adjust(top=0.85)
explode = (0.5,0.5 ,0.5,0.5,0,0.5)
ax1.pie(technologies,explode = explode, 
        autopct='%1.1f%%',shadow=False, pctdistance=1.2)
ax1.axis('equal')
ax1.set_title('Output of storage projects broken down by technology (%)')
plt.legend(labels = technologies.index,bbox_to_anchor=(0.0,1))
plt.show()


# In[1]:




# In[ ]:




# In[ ]:




# In[164]:




# In[ ]:




# In[ ]:



