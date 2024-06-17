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
from PIL import Image
from numerize import numerize

############################################ INITIAL SETTINGS FOR THE DASHBOARD ##################################################

st.set_page_config(page_title = 'CitiBike Strategy Dashboard', layout = 'wide')
st.title('CitiBike Strategy Dashboard')

### DEFINE SIDE BAR
st.sidebar.title('Aspect Selector')
page = st.sidebar.selectbox('Select an aspect of the analysis',
                            ['Intro page',
                             'Weather component and bike usage',
                             'Most popular stations',
                             'Interactive map with aggregated bike trips',
                             'Classic versus electric bikes',
                             'Recommendations'])

################################################# IMPORT DATA #####################################################################

df = pd.read_csv('subset_new_york_data.csv', index_col = 0)

############################################ DEFINE THE PAGES #####################################################################

### INTRO PAGE

if page == 'Intro page':
    st.markdown('This dashboard aims to provide helpful insights on the expansion problems NY CitiBikes currently faces. Right now, CitiBikes runs into a situation where customers complain about bikes not being available at certain times. This analysis will look at the potential reasons behind this.')
    st.markdown('#### Overall Approach:')
    st.markdown('1. Define Objective')
    st.markdown('2. Source Data')
    st.markdown('3. Geospatial Plot')
    st.markdown('4. Interactive Visualizations')
    st.markdown('5. Dashboard Creation')
    st.markdown('6. Findings and Recommendations')
    st.markdown('#### Dashboard Sections:')
    st.markdown('- Weather component and bike usage')
    st.markdown('- Most popular stations')
    st.markdown('- Interactive map with aggregated bike trips')
    st.markdown('- Classic versus electric bikes')
    st.markdown('- Recommendations')
    st.markdown('The dropdown menu on the left under "Aspect Selector" will take you to the different aspects of the analysis our team looked at.')

    myImage = Image.open('CitiBikes.jpg') # Source: https://www.nydailynews.com/2019/07/10/citi-bike-neglects-poor-nyc-neighborhoods-and-communities-of-color-report/
    st.image(myImage)
    st.markdown('Source: https://www.nydailynews.com/2019/07/10/citi-bike-neglects-poor-nyc-neighborhoods-and-communities-of-color-report')


### LINE CHART PAGE: WEATHER COMPONENT AND BIKE USAGE

elif page == 'Weather component and bike usage':
    
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
            line = dict(color = 'blue')  # Set the color for bike rides
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
            titlefont = dict(color = 'blue'),
            tickfont = dict(color = 'blue')
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
    st.markdown('There is an obvious correlation between the rise and drop of temperatures and their relationship with the frequency of bike trips taken daily. As temperatures plunge, so does bike usage. This insight indicates that the shortage problem may be prevalent merely in the warmer months, approximately from May to October.')


### BAR CHART PAGE: MOST POPULAR STATIONS

elif page == 'Most popular stations':

    # Create the filter on the side bar
    with st.sidebar:
        season_filter = st.multiselect(label = 'Select the season', options = df['season'].unique(),
    default = df['season'].unique())

    df1 = df.query('season == @season_filter')

    # Define the total rides
    total_rides = float(df1['bike_rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value = numerize.numerize(total_rides))

    # Create the chart
    df1['value'] = 1 
    df_groupby_bar = df1.groupby('start_station_name', as_index = False).agg({'value': 'sum'})
    top20 = df_groupby_bar.nlargest(20, 'value')

    fig = go.Figure(go.Bar(x = top20['start_station_name'], y = top20['value'], marker = {'color': top20['value'], 'colorscale': 'Blues'}))

    fig.update_layout(
        title = 'Top 20 Most Popular Bike Stations in NYC 2022',
        xaxis_title = 'Start Stations',
        yaxis_title ='Sum of Trips',
        width = 900, height = 600
    )

    st.plotly_chart(fig, use_container_width = True)
    st.markdown('From the bar chart it is clear that there are some start stations that are more popular than others - in the top 3 we can see West St/Chambers St, Broadway/W 58 St as well as 6 Ave/W 33 St. There is a significant jump between the highest and lowest bars of the plot, indicating some clear preferences for the leading stations. This is a finding that we could cross reference with the interactive map with aggregated bike trips.')


### MAP PAGE: INTERACTIVE MAP WITH AGGREGATED BIKE TRIPS

elif page == 'Interactive map with aggregated bike trips': 

    path_to_html = "CitiBike Trips Aggregated.html" 

    # Read file and keep in variable
    with open(path_to_html, 'r') as f: 
        html_data = f.read()

    # Show in webpage
    st.header('Aggregated Bike Trips in NYC 2022')
    st.components.v1.html(html_data,height = 1000)
    st.markdown('#### Using the filter on the left hand side of the map, we can check whether the most popular start stations also appear in the most popular trips.')
    st.markdown("The most popular start stations are West St/Chambers St, Broadway/W 58 St, as well as 6 Ave/W 33 St. While having the aggregated bike trips filter enabled, we can see that even though 6 Ave/W 33 St is a popular start station, it doesn't account for the most commonly taken trips.")
    st.markdown('Some of the most common routes are between 12 Ave/W 40 St, 10 Ave/W 14 St, and West St/Chambers St, which are located along the water, or routes located around the perimeter of Central Park.')


### HISTOGRAMS: CLASSIC VERSUS ELECTRIC BIKES

elif page == 'Classic versus electric bikes':

    # Filter DataFrame by category
    classic_bike = df[df['rideable_type'] == 'classic_bike']
    electric_bike = df[df['rideable_type'] == 'electric_bike']

    # Create histograms for each category
    hist_data_A = go.Histogram(x = classic_bike['avgTemp'], name = 'Classic Bike', marker = dict(color = 'blue'))
    hist_data_B = go.Histogram(x = electric_bike['avgTemp'], name = 'Electric Bike', marker = dict(color = 'lightblue'))

    # Create layout
    layout = go.Layout(
        title = 'Classic vs Electric Bike Rentals by Temperature',
        xaxis = dict(title = 'Average Temperature'),
        yaxis = dict(title = 'Frequency'),
        barmode = 'overlay'
    )

    # Create the figure
    fig3 = go.Figure(data = [hist_data_A, hist_data_B], layout = layout)

    # Display the figure
    st.plotly_chart(fig3)

    st.markdown('The data shows that classic bikes are rented more often when the temperature is warmer. Electric bikes are rented slightly more often when the temperature is warmer, however relative to classic bikes, electric bike rentals do not change much with the temperature.')
    st.markdown('Additionally, the data shows that classic bikes are rented over 2.5 times more often than electric bikes. This limited electric bike availability helps to explain why their rental does not change much with the weather, as they may simply not be an option most of the time.')

                
### CONCLUSIONS PAGE: RECOMMENDATIONS

else:
    
    st.header('Conclusions and Recommendations')
    bikes = Image.open('CitiBike.jpg')  # Source: https://nycdotbikeshare.info/news-and-events/citi-bike-launch-nyc
    st.image(bikes)
    st.markdown('Source: https://nycdotbikeshare.info/news-and-events/citi-bike-launch-nyc')
    st.markdown('### Our analysis has shown that NY CitiBikes should focus on the following objectives moving forward:')
    st.markdown('- There is a clear correlation between temperature and bike trips. We recommend ensuring that stations are fully stocked during the warmer months in order to meet the higher demand, but to provide a lower supply in winter and late autumn to reduce cost.')
    st.markdown('- There is a clear popularity among the stations along the water and around Central Park. We recommend adding bikes and bike parking to these locations.')
    st.markdown('- We found that classic bikes are rented over 2.5 times more often than electric bikes due to limited electric bike availability. We recommend incorporating more electric bikes into circulation when new bikes are added.')
