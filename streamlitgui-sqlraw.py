import numpy as np
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

db_url = r"sqlite:///red-bus-data.db"


# Function to open a database connection
def open_db_connection(db_url):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# Function to close a database connection
def close_db_connection(session):
    session.close()


conn = open_db_connection(db_url)

list_of_unique_bus_types = [row[0] for row in
                            conn.execute(text("select distinct(bustype) from 'red-bus-data'")).fetchall()]
list_of_unique_bus_routes = [row[0] for row in
                             conn.execute(text("select distinct(route_name) from 'red-bus-data'")).fetchall()]

list_of_bus_operators = [(row[0], row[1]) for row in
                         conn.execute(text("select * from 'red-bus-operators' ")).fetchall()]

max_price = conn.execute(text("select max(price) from 'red-bus-data'")).fetchone()[0]
min_price = conn.execute(text("select min(price) from 'red-bus-data'")).fetchone()[0]

max_rating = conn.execute(text("select max(star_rating) from 'red-bus-data'")).fetchone()[0]
min_rating = conn.execute(text("select min(star_rating) from 'red-bus-data'")).fetchone()[0]

max_seats_available = conn.execute(text("select max(seats_available) from 'red-bus-data'")).fetchone()[0]
min_seats_available = conn.execute(text("select min(seats_available) from 'red-bus-data'")).fetchone()[0]

close_db_connection(conn)

# Title of the app
st.title('Red Bus Routes Information')

# Filters
st.sidebar.header('Filters')

# Bus operator Filter (Dropdown)
bus_operator = st.sidebar.selectbox(
    'Select State wise Bus Operator',
    options=['All'] + [x[1] for x in list_of_bus_operators]
)

# Bus Type Filter (Dropdown)
bustype = st.sidebar.selectbox(
    'Select Bus Type',
    options=['All'] + list_of_unique_bus_types
)

# Route Filter
routes = st.sidebar.selectbox(
    'Select Routes',
    options=['All'] + list_of_unique_bus_routes
)

# Price Range Filter
price_range = st.sidebar.slider(
    'Select Price Range',
    min_value=int(max_price),
    max_value=int(min_price),
    value=(int(min_price), int(max_price))
)

# Star Rating Filter
star_rating = st.sidebar.slider(
    'Select Star Rating',
    min_value=float(min_rating),
    max_value=float(max_rating),
    value=(float(min_rating), float(max_rating))
)

# Seat Availability Filter
seat_availability = st.sidebar.slider(
    'Select Seat Availability',
    min_value=int(min_seats_available),
    max_value=int(max_seats_available),
    value=(int(min_seats_available), int(max_seats_available))
)


# route_name,bus_route_link,busname,bustype,departing_time,duration,reaching_time,star_rating,price,seats_available
def get_acc_to_bustype(bustype):
    con = create_engine(db_url)
    result = pd.read_sql_query(
        f"select * from 'red-bus-data' where bustype = '{bustype}'",
        con)
    return result


def get_all_data():
    con = create_engine(db_url)
    result = pd.read_sql_query("select * from 'red-bus-data'", con)
    return result


def get_acc_to_routes(routes):
    con = create_engine(db_url)
    result = pd.read_sql_query(
        f"select * from 'red-bus-data' where route_name = '{routes}'",
        con)
    return result


def get_acc_to_routes_and_bustype_and_busoperator(bustype, routes, bus_operator):
    con = create_engine(db_url)
    result = pd.read_sql_query(
        f"select * from 'red-bus-data' where route_name = '{routes}' and bustype = '{bustype}' and bus_operator_id = ( select id from 'red-bus-operators' where operator_name = '{bus_operator}')",
        con)
    return result


def get_acc_to_bus_operator(bus_op):
    con = create_engine(db_url)
    result = pd.read_sql_query(
        f"select * from 'red-bus-data' where bus_operator_id = ( select id from 'red-bus-operators' where operator_name = '{bus_op}')",
        con)
    return result


def get_acc_to_bus_operator_and_bustype(bus_operator, bustype):
    con = create_engine(db_url)
    result = pd.read_sql_query(
        f"select * from 'red-bus-data' where bustype = '{bustype}' and bus_operator_id = ( select id from 'red-bus-operators' where operator_name = '{bus_operator}')",
        con)
    return result


def get_acc_to_bus_operator_and_routes(bus_operator, routes):
    con = create_engine(db_url)
    result = pd.read_sql_query(
        f"select * from 'red-bus-data' where route_name = '{routes}' and bus_operator_id = ( select id from 'red-bus-operators' where operator_name = '{bus_operator}')",
        con)
    return result


def get_acc_to_bustype_and_routes(bustype, routes):
    con = create_engine(db_url)
    result = pd.read_sql_query(
        f"select * from 'red-bus-data' where bustype = '{bustype}' and route_name = '{routes}'",
        con)

    return result


filtered_data = get_all_data()

# Apply Filters

if bus_operator != 'All':
    filtered_data = get_acc_to_bus_operator(bus_operator)

if bustype != 'All':
    filtered_data = get_acc_to_bustype(bustype)

if routes != 'All':
    filtered_data = get_acc_to_routes(routes)

if bus_operator != 'All' and bustype != 'All':
    filtered_data = get_acc_to_bus_operator_and_bustype(bus_operator, bustype)

if bus_operator != 'All' and routes != 'All':
    filtered_data = get_acc_to_bus_operator_and_routes(bus_operator, routes)

if bustype != 'All' and routes != 'All':
    filtered_data = get_acc_to_bustype_and_routes(bustype, routes)

if bustype != 'All' and routes != 'All' and bus_operator != 'All':
    filtered_data = get_acc_to_routes_and_bustype_and_busoperator(bustype, routes, bus_operator)


def get_filtered_data(a, b, c, d, e, f):
    con = create_engine(db_url)
    result = pd.read_sql_query(
        f"select * from 'red-bus-data' where price >= {price_range[0]} and price <= {price_range[1]} and star_rating >= {star_rating[0]} and star_rating <= {star_rating[1]} and seats_available >= {seat_availability[0]} and seats_available <= {seat_availability[1]} ",
        con)
    return result


# Apply Filters
filtered_data_temp = get_filtered_data(price_range[0], price_range[1], star_rating[0], star_rating[1],
                                       seat_availability[0], seat_availability[1])
filtered_data = filtered_data_temp[filtered_data_temp['id'].isin(filtered_data['id'])]

filtered_data['departing_time'] = filtered_data['departing_time'].str[:8]
filtered_data['reaching_time'] = filtered_data['reaching_time'].str[:8]

# Display total row count
st.write(f"Total rows in the filtered data: {filtered_data.shape[0]}")

# Display the filtered data
st.dataframe(filtered_data, height=1000, width=1000)

# Additional Information
st.sidebar.subheader('Selected Bus Details')
selected_bus = st.sidebar.selectbox('Select a bus to see details', filtered_data['busname'])

bus_details = filtered_data[filtered_data['busname'] == selected_bus]
if not bus_details.empty:
    st.sidebar.table(bus_details.to_dict('records')[0])
