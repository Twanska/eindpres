#!/usr/bin/env python
# coding: utf-8

# ## Packages importeren

# In[13]:


import pandas as pd
import plotly.express as px
import statsmodels
import json
import streamlit
#import session_info


# In[15]:


#session_info.show()


# ### Bronnen

# https://www.kaggle.com/sveneschlbeck/alcohol-consumption-per-capita-year-and-country?select=alcohol-consumption.csv
# https://ourworldindata.org/grapher/gdp-per-capita-worldbank
# https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth_mapbox.html
# https://plotly.com/python-api-reference/generated/plotly.express.scatter
# Extra dataset kan zijn: Werkloosheid, barsluitingstijden, domestic violence, healthcare kwaliteits index, prijs per liter pure alcohol per land, happiness rating

# ## Random Useful Code 

# In[ ]:


#pd.options.display.max_rows = None
#pd.options.display.max_columns = None

#regios2 = ['HEG0802']
#df_HEG2 = df_HEG[df_HEG['LocationCode'].isin(regios2)]

#nullen['Dagen'] = nullen['Datum_Verschil'].str.strip(' days').astype(int)

#df_clean_sorted1 = nullen.groupby(['BoltId', 'LocationCode'])['Y_Verschil', 'permaand_y', 'X_Verschil', 'permaand_x', 'Z_Verschil', 'permaand_z'].min().sort_values('Y_Verschil')


# ## Bestanden inladen

# In[2]:


alc = pd.read_csv('alcohol_per_capita.csv', sep=',')
gdp = pd.read_csv('gdp_per_capita.csv', sep=',')
countries = json.load(open('countries.geojson', 'r'))


# In[ ]:


#alc.head()


# In[ ]:


#gdp.head()


# ## Data inspecteren

# In[ ]:


#alc.info()


# In[ ]:


#alc['Year'].value_counts()


# In[ ]:


#gdp.info()


# In[ ]:


#gdp['Year'].value_counts()


# In[ ]:


## Kijken welke items de dictionary bevat
countries['features'][0].keys()


# In[ ]:


## Kijken wat er in properties van de dictionary staat
countries['features'][0]['properties']


# ## Data Manipulatie

# In[3]:


df_merged = alc.merge(gdp, how='inner', on=['Entity', 'Year'])
#df_merged.head()


# In[ ]:


#df_merged.info()


# In[4]:


df_merged['Code_x'] = df_merged['Code_x'].astype('string')
df_merged['Year'] = df_merged['Year'].astype('string')
df_merged = df_merged[df_merged['Code_x']!= 'NaN']
df_merged = df_merged[df_merged['Code_x']!= 'OWID_WRL']
df_merged = df_merged.drop(columns='Code_y')
df_merged = df_merged.rename(columns= {'Code_x': 'Code', 'Total alcohol consumption per capita (liters of pure alcohol, projected estimates, 15+ years of age)': 'Alcohol Consumption per Capita', 'GDP per capita, PPP (constant 2017 international $)': 'GDP per Capita'})


# In[5]:


# For loop om de countries.geojson met de df_merged te verbinden
iso_id_map = {}
for feature in countries['features']:
    feature['id'] = feature['properties']['ISO_A3']
    iso_id_map[feature['properties']['ISO_A3']] = feature['id']
# Nieuwe kolom maken in de dataframe
df_merged['id'] = df_merged['Code'].apply(lambda x: iso_id_map[x])
df_merged.head()


# In[6]:


df_merged.info()


# ## Visualisaties

# ### 1D Boxplots

# In[ ]:


fig = px.box(data_frame=df_merged, x='Year', y='Alcohol Consumption per Capita',
             title='Boxplot globale alcohol consumptie per meetjaar',
             category_orders={'Year': ['2000', '2005', '2010', '2015', '2018']}, 
             #color_discrete_map={'Adelie': 'royalblue', 'Chinstrap': 'tomato', 'Gentoo': 'mediumaquamarine'}, 
             #color='Year',
             labels={'Year': 'Meetjaar', 'Alcohol Consumption per Capita': 'Totale alcohol consumptie per capita in liters (L)'})

fig.update_layout(title_text='Boxplot globale alcohol consumptie per meetjaar', title_x=0.5)          
fig.show()


# In[ ]:


fig1 = px.box(data_frame=df_merged, x='Year', y='GDP per Capita',
             title='Boxplot globale GDP per meetjaar',
             category_orders={'Year': ['2000', '2005', '2010', '2015', '2018']}, 
             #color_discrete_map={'Adelie': 'royalblue', 'Chinstrap': 'tomato', 'Gentoo': 'mediumaquamarine'}, 
             #color='Year',
             labels={'Year': 'Meetjaar', 'GDP per Capita': 'Totale GDP per capita in dollars ($)'})

fig1.update_layout(title_text='Boxplot globale GDP per meetjaar', title_x=0.5)          
fig1.show()


# ### 1D Histograms (Weet niet of deze handig zijn)

# In[ ]:


#fig2 = px.histogram(data_frame=df_merged, x='GDP per Capita')
#fig2.show()


# In[ ]:


#fig3 = px.histogram(data_frame=df_merged, x='Alcohol Consumption per Capita')
#fig3.show()


# ### 2D Spreidingsdiagram

# In[12]:


# NOG TOEVOEGEN:
# - DROP DOWN DIE DE JAREN SELECTEERT

fig4 = px.scatter(data_frame=df_merged, x='GDP per Capita', y='Alcohol Consumption per Capita',
                 trendline='ols', trendline_scope='overall',
                  category_orders={'Year': ['2000', '2005', '2010', '2015', '2018']},
                  color_discrete_map={'2000': 'royalblue', '2005': 'tomato', '2010': 'mediumaquamarine', '2015': 'gold', '2018': 'purple'},
                  color='Year',
                 title='Relatie tussen GDP en Alcohol Consumptie per Capita',
                  hover_data=['Entity'],
                labels={'GDP per Capita': 'Totale GDP per capita in dollars ($)', 'Alcohol Consumption per Capita': 'Totale alcohol consumptie per capita in liters (L)', 'Year': 'Meetjaar', 'Entity': 'Land'})

my_buttons = [{'label': 'Alle jaren', 'method': 'update',
                  'args':[{'visible': [True, True, True, True, True]}]},
              {'label': '2000', 'method': 'update',
                  'args':[{'visible': [True, False, False, False, False, False]}]},
              {'label': '2005', 'method': 'update',
                  'args':[{'visible': [False, True, False, False, False, False]}]},
              {'label': '2010', 'method': 'update',
                  'args':[{'visible': [False, False, True, False, False, False]}]},
              {'label': '2015', 'method': 'update',
                  'args':[{'visible': [False, False, False, True, False, False]}]},
              {'label': '2018', 'method': 'update',
                  'args':[{'visible': [False, False, False, False, True, False]}]}]

fig4.update_layout({'updatemenus':[{'type': "dropdown",
                  'direction': 'down',
                  'x': 0.15, 'y': 1.15,
                  'showactive': True,
                  'active': 0,
                  'buttons': my_buttons}]})

fig4.update_layout(title_x=0.5)
fig4.show()


# ### Geospatiale inspectie kaart Folium Choropleth

# In[ ]:


# #NOG TOEVOEGEN:
# # - HOVER CONTROLS OM INFORMATIE TE ZIEN PER LAND
# # - LAAT NU ALLEEN NOG MAAR LAATSTE JAAR ZIEN
# # - LAAT JAREN ZIEN D.M.V. EEN SLIDER
# # HAAL ALLE ##### WEG MET 'CTRL + /'

# import geopandas as gpd #Werkt alleen in de Geo_env
# import folium
# countries = gpd.read_file('countries.geojson')

# geo_df = countries.merge(df_merged, how = 'inner', right_on = 'Code', left_on = 'ISO_A3')

# ALCOHOL = folium.Choropleth(geo_data=geo_df,
#              name='ALCOHOL',
#              data=geo_df,
#              columns=['ADMIN','Alcohol Consumption per Capita'],
#              key_on='feature.properties.ADMIN',
#              fill_color='YlGn',
#              fill_opacity=0.75,
#              line_opacity=0.5,
#              legend_name='Totale alcohol consumptie per capita in liters (L)')

# GDP = folium.Choropleth(geo_data=geo_df,
#              name='GDP',
#              data=geo_df,
#              columns=['ADMIN','GDP per Capita'],
#              key_on='feature.properties.ADMIN',
#              fill_color='RdPu',
#              fill_opacity=0.75,
#              line_opacity=0.5,
#              legend_name='Totale GDP per capita in dollars ($)')

# m = folium.Map(Location=[0,0],
#                zoom_start=2.5,
#                scrollWheelZoom=True,
#                zoom_control=True,
#                tiles='https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
#                attr="https://www.openstreetmap.org/")

# m.add_child(ALCOHOL).add_child(GDP)
# m.add_child(folium.map.LayerControl())

# display(m)


# ### Geospatiale inspectiekaart Plotly.Choropleth 

# In[ ]:


# Plotly.express choropleth map Alcohol
fig5 = px.choropleth_mapbox(df_merged, 
                    locations='id', 
                    geojson=countries, 
                    color='Alcohol Consumption per Capita',
                    color_continuous_scale=[(0,"yellow"), (1,"blue")],
                    category_orders={'Year': ['2000', '2005', '2010', '2015', '2018']},
                    hover_name='Entity',
                    mapbox_style="carto-positron",
                    center={'lat': 50, 'lon':0},
                    zoom=0.62, opacity=0.5,
                    animation_frame='Year',
                    title= 'Alcohol consumptie per capita per meetjaar',
                    labels={'Alcohol Consumption per Capita': 'Liters'})
fig5.update_layout(title_x=0.5, width=975, height=725)
fig5.show()
st.write(fig5)


# In[ ]:


# Plotly.express choropleth map GDP
fig6 = px.choropleth_mapbox(df_merged, 
                    locations='id', 
                    geojson=countries, 
                    color='GDP per Capita',
                    color_continuous_scale=[(0,"yellow"), (1,"green")],
                    category_orders={'Year': ['2000', '2005', '2010', '2015', '2018']},
                    hover_name='Entity',
                    mapbox_style="carto-positron",
                    center={'lat': 50, 'lon':0},
                    zoom=0.62, opacity=0.5,
                    animation_frame='Year',
                    title= 'Bruto Binnenlands Product per meetjaar',
                    labels={'GDP per Capita': 'Dollars ($)'})
fig6.update_layout(title_x=0.5, width=975, height=725)
fig6.show()

