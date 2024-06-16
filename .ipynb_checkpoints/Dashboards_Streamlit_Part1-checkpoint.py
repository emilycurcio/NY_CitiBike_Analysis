################################################ CITIBIKES DASHABOARD ###########################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

############################################ INITIAL SETTINGS FOR THE DASHBOARD ##################################################

st.set_page_config(page_title = 'CitiBike Strategy Dashboard', layout = 'wide')
st.title('CitiBike Strategy Dashboard')
st.markdown('The dashboard will help with the expansion problems CitiBike currently faces.')
st.markdown('Right now, CitiBike runs into a situation where customers complain about bikes not being avaibale at certain times. This analysis aims to look at the potential reasons behind this.')

################################################# IMPORT DATA #####################################################################

df = pd.read_csv('subset_new_york_data.csv', index_col = 0)
top20 = pd.read_csv('top20.csv', index_col = 0)

############################################ DEFINE THE CHARTS #####################################################################

### BAR CHART

fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color': top20['value'], 'colorscale': 'Greens'}))

fig.update_layout(
    title = 'Top 20 Most Popular Bike Stations in NYC 2022',
    xaxis_title = 'Start Stations',
    yaxis_title ='Sum of Trips',
    width = 900, height = 600
)

st.plotly_chart(fig, use_container_width = True)


### LINE CHART

# Aggregate the data by datetime
df_aggregated = df.groupby('date').agg({
    'bike_rides_daily': 'mean',  # You can also use 'mean' or another aggregate function
    'avgTemp': 'mean'
}).reset_index()

# Create the figure
fig2 = go.Figure()

# Primary Y-axis (Bike rides)
fig2.add_trace(
    go.Scatter(
        x = df_aggregated['date'],
        y = df_aggregated['bike_rides_daily'],
        name = 'Daily Bike Rides',
        yaxis = 'y1',  # Specify primary y-axis
        line = dict(color = 'green')  # Set the color for bike rides
    )
)

# Secondary Y-axis (Avg Temp)
fig2.add_trace(
    go.Scatter(
        x = df_aggregated['date'],
        y = df_aggregated['avgTemp'],
        name = 'Daily Temperature',
        yaxis = 'y2',  # Specify secondary y-axis
        line = dict(color = 'red')  # Set the color for average temperature
    )
)

# Customize the chart layout
fig2.update_layout(
    title = 'Temperature vs Rides in NYC 2022',
    xaxis_title = 'Date',
    yaxis = dict(
        title = 'Daily Total Bike Rides',
        titlefont = dict(color = 'green'),
        tickfont = dict(color = 'green')
    ),
    yaxis2 = dict(
        title = 'Daily Avg Temperature',
        titlefont = dict(color = 'red'),
        tickfont = dict(color = 'red'),
        anchor = 'x',
        overlaying = 'y',
        side = 'right'
    ),
    legend = dict(
        x = 0,
        y = 1.1,
        orientation = 'h'
    )
)

# Show the plot
st.plotly_chart(fig2, use_container_width = True)


### MAP

path_to_html = "CitiBike Trips Aggregated.html" 

# Read file and keep in variable
with open(path_to_html, 'r') as f: 
    html_data = f.read()

# Show in webpage
st.header('Aggregated Bike Trips in NYC 2022')
st.components.v1.html(html_data,height = 1000)
