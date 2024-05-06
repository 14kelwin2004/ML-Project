import pandas as pd
import numpy as np

import missingno as msno

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import warnings 
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None) # to see all columns
# pd.set_option('display.max_rows', None)
pd.set_option('display.max_rows', 200) 
pd.set_option('display.max_colwidth',900) # to see full coontent of columns

%matplotlib inline
df=pd.read_csv("../input/us-highway-railgrade-crossing-accident/Highway-Rail_Grade_Crossing_Accident_Data.csv")
df.head()
#get the size of dataframe
print ("Rows     : " , df.shape[0])  #get number of rows/observations
print ("Columns  : " , df.shape[1]) #get number of columns
print ("#"*30,"\n","Features : \n", df.columns.tolist()) #get name of columns/features
df_train_car_accident=df[['Report Key','Railroad Code','Grade Crossing ID','Railroad Name',
                      'Report Year',
                      'Incident Month',
                      'Date', 
                      'Month', 'Day', 
                      'Hour', 'Minute',
                      'AM/PM','Nearest Station','Division',
                      'County Name',
                      'State Name',
                      'City Name', 'Highway Name', 
                      'Highway User', 
                      'Estimated Vehicle Speed',
                      'Vehicle Direction',
                      'Highway User Position', 
                      'Equipment Involved','Equipment Struck', 
                      'Temperature', 
                       'Visibility', 
                       'Weather Condition',
                       'Equipment Type',
                       'Track Type',
                          'Track Name', 
                        'Track Class', 
                       'Number of Locomotive Units',
                        'Number of Cars',
                       'Train Speed', 
                      'Estimated/Recorded Speed',
                       'Train Direction',
                       'Roadway Condition',
                      'Crossing Illuminated',
                      'Signaled Crossing Warning',
                      'User Age', 
                      'User Gender', 
                      'User Struck By Second Train',
                      'Highway User Action',
                      'Driver Passed Vehicle', 
                       'View Obstruction',
                       'Driver Condition',
                      'Driver In Vehicle', 
                      'Crossing Users Killed For Reporting Railroad',
                      'Crossing Users Injured For Reporting Railroad', 
                      'Vehicle Damage Cost', 
                      'Number Vehicle Occupants',
                          'Narrative',
                      'Employees Killed For Reporting Railroad', 
                      'Employees Injured For Reporting Railroad', 
                      'Number People On Train', 
                      'Passengers Killed For Reporting Railroad',
                      'Passengers Injured For Reporting Railroad',
                      'Total Killed Form 57',
                      'Total Injured Form 57', 
                      'Total Killed Form 55A',
                      'Total Injured Form 55A', 
                      'District']].copy()
df_train_car_accident.columns = [col.replace(' ','_') for col in df_train_car_accident.columns]
df_train_car_accident.info()
df_train_car_accident.isna().sum()
df_train_car_accident.describe().T
df_train_car_accident.describe(exclude='number').T
# Lets look visualize the relationship 
sns.set_palette(sns.color_palette("PuRd", 8))
plt.figure(figsize=(15,13))

sns.countplot(orient='v',y=df_train_car_accident.Report_Year,data=df_train_car_accident)
#sns.lineplot(x=df_train_car_accident.Report_Year,data=df_train_car_accident)
# Lets look visualize the relationship 
sns.set_palette(sns.color_palette("PuRd", 8))
plt.figure(figsize=(15,13))

sns.countplot(orient='v',y=df_train_car_accident.Report_Year,data=df_train_car_accident)
#sns.lineplot(x=df_train_car_accident.Report_Year,data=df_train_car_accident)

sns.set_palette(sns.color_palette("Set2", 8))
plt.figure(figsize=(15,13))

sns.distplot(x=df_train_car_accident.Report_Year)
# Lets look visualize the relationship 
sns.set_palette(sns.color_palette("PuRd", 8))
plt.figure(figsize=(15,13))
order = df_train_car_accident['State_Name'].value_counts(ascending=False).index 
sns.countplot(orient='v',y=df_train_car_accident['State_Name'],data=df_train_car_accident,order=order)
df_recent_event=df_train_car_accident.loc[df_train_car_accident.Report_Year > 2015]
df_recent_event.head()
##trying to use plotly map function
df_state=df_recent_event.groupby(['State_Name']).count()['Report_Year'].sort_values(ascending=False).reset_index()
df_state.rename(columns={'Report_Year':'Count_of_accident'},inplace=True)
code = {'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}

df_state['State_Name'] =df_state['State_Name'].str.capitalize()
df_state['Code']=df_state['State_Name'].map(code)

fig = px.choropleth(data_frame=df_state,locations=df_state['Code'],
                    locationmode='USA-states' ,
                    scope="usa",hover_name='State_Name',
                    color='Count_of_accident', 
                    title='State Wise Incident Report',
                    color_continuous_scale='sunset'
                  )
fig.add_scattergeo(
    locations=df_state['Code'],
    locationmode='USA-states',
    text=df_state['Code'],
    mode='text')
fig.show('notebook')

fig = px.choropleth(data_frame=df_state,locations=df_state['Code'],
                    locationmode='USA-states' ,
                    scope="usa",hover_name='State_Name',
                    color='Count_of_accident', 
                    title='State Wise Incident Report',
                    color_continuous_scale='sunset'
                  )
fig.add_scattergeo(
    locations=df_state['Code'],
    locationmode='USA-states',
    text=df_state['Code'],
    mode='text')
fig.show('notebook')

sns.set_palette(sns.color_palette("PuRd", 8))
plt.figure(figsize=(15,13))
order = df_recent_event['State_Name'].value_counts(ascending=False).index 
sns.countplot(orient='v',y=df_recent_event['State_Name'],data=df_recent_event,order=order)
fig = px.choropleth(data_frame=df_state,locations=df_state['Code'],
                    locationmode='USA-states' ,
                    scope="usa",hover_name='State_Name',
                    color='Count_of_accident', 
                    title='State Wise Incident Report',
                    color_continuous_scale='sunset'
                  )
fig.add_scattergeo(
    locations=df_state['Code'],
    locationmode='USA-states',
    text=df_state['Code'],
    mode='text')
fig.show('notebook')

sns.set_palette(sns.color_palette("PuRd", 8))
plt.figure(figsize=(15,13))
order = df_recent_event['State_Name'].value_counts(ascending=False).index 
sns.countplot(orient='v',y=df_recent_event['State_Name'],data=df_recent_event,order=order)

df_county=df_recent_event.groupby(['County_Name','State_Name']).count()['Report_Year'].sort_values(ascending=False).head(10).reset_index()

df_county['State_Name'] =df_county['State_Name'].str.capitalize()
df_county['Code']=df_county['State_Name'].map(code)
df_county['county_state'] =df_county['County_Name']+","+ df_county['Code']
df_county.rename(columns={'Report_Year':'Count_of_accident'},inplace=True)

sns.set_palette(sns.color_palette("PuRd", 8))
plt.figure(figsize=(15,13))
sns.barplot(y=df_county.county_state,x=df_county.Count_of_accident ,data=df_county)


