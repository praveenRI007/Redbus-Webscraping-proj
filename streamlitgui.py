import numpy as np
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Load the data
cnx = create_engine('sqlite:///red-bus-data.db').connect()

# table named 'contacts' will be returned as a dataframe.
data = pd.read_sql_table('red-bus-data', cnx)

# Title of the app
st.title('Red Bus Routes Information')

# Filters
st.sidebar.header('Filters')

# Bus Type Filter (Dropdown)
bustype = st.sidebar.selectbox(
    'Select Bus Type',
    options=['All'] + list(data['bustype'].unique())
)

# Route Filter
routes = st.sidebar.selectbox(
    'Select Routes',
    options=['All'] + list(data['route_name'].unique())
)

# Price Range Filter
price_range = st.sidebar.slider(
    'Select Price Range',
    min_value=int(data['price'].min()),
    max_value=int(data['price'].max()),
    value=(int(data['price'].min()), int(data['price'].max()))
)

# Star Rating Filter
star_rating = st.sidebar.slider(
    'Select Star Rating',
    min_value=float(data['star_rating'].min()),
    max_value=float(data['star_rating'].max()),
    value=(float(data['star_rating'].min()), float(data['star_rating'].max()))
)

# Seat Availability Filter
seat_availability = st.sidebar.slider(
    'Select Seat Availability',
    min_value=int(data['seats_available'].min()),
    max_value=int(data['seats_available'].max()),
    value=(int(data['seats_available'].min()), int(data['seats_available'].max()))
)

# route_name,bus_route_link,busname,bustype,departing_time,duration,arrival_time,star_rating,price,seats_available

# Apply Filters
if bustype != 'All':
    filtered_data = data[data['bustype'] == bustype]
else:
    filtered_data = data.copy()

if routes != 'All':
    filtered_data = data[data['route_name'] == routes]
else:
    filtered_data = data.copy()

# Apply Filters
filtered_data = filtered_data[
    (data['price'] >= price_range[0]) &
    (data['price'] <= price_range[1]) &
    (data['star_rating'] >= star_rating[0]) &
    (data['star_rating'] <= star_rating[1]) &
    (data['seats_available'] >= seat_availability[0]) &
    (data['seats_available'] <= seat_availability[1])
    ]

# Display total row count
st.write(f"Total rows in the filtered data: {filtered_data.shape[0]}")

# Display the filtered data
st.dataframe(filtered_data, height=1000, width=1000)

# Additional Information
st.sidebar.subheader('Selected Bus Details')
selected_bus = st.sidebar.selectbox('Select a bus to see details', filtered_data['busname'])

bus_details = filtered_data[filtered_data['busname'] == selected_bus]
if not bus_details.empty:
    st.sidebar.write(bus_details.to_dict('records')[0])


def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link.split('=')[1]
    return f'<a target="_blank" href="{link}">{text}</a>'