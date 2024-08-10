# Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

## Table of Contents


- [About the Project](#about-the-project)
- [Live Demo](#live-demo)
- [Live Application Screenshots](#live-demo)
- [Skills Takeaway](#skills-takeaway)
- [Domain](#domain)
- [Problem Statement](#problem-statement)
- [Business Use Cases](#business-use-cases)
- [Approach](#approach)
  - [Data Scraping](#data-scraping)
  - [Data Storage](#data-storage)
  - [Data Analysis/Filtering using Streamlit](#data-analysisfiltering-using-streamlit)
- [Results](#results)
- [Data Set](#data-set)
- [Database Schema](#database-schema)
- [Project Deliverables](#project-deliverables)
 
  
## Live Demo

Explore the live demo currently deployed in render.com at: [Streamlit Redbus Data Dashboard Application](https://redbus-webscraping-proj.onrender.com/)

## Screenshots
![screenshot1](https://github.com/praveenRI007/Redbus-Webscraping-proj/blob/master/screenshots/redbus1.PNG)
![screenshot2](https://github.com/praveenRI007/Redbus-Webscraping-proj/blob/master/screenshots/redbus2.PNG)
![screenshot3](https://github.com/praveenRI007/Redbus-Webscraping-proj/blob/master/screenshots/redbus3.PNG)
![screenshot4](https://github.com/praveenRI007/Redbus-Webscraping-proj/blob/master/screenshots/redbus4.PNG)

## About the Project

The **Redbus Data Scraping and Filtering with Streamlit Application** provides a comprehensive solution for collecting, analyzing, and visualizing bus travel data. Using Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability. The project enhances data collection and decision-making, thereby improving operational efficiency and strategic planning in the transportation industry.

## Skills Takeaway

- Web Scraping using Selenium
- Python
- Streamlit
- SQL

## Domain

- Transportation

## Problem Statement

The project aims to revolutionize the transportation industry by providing a solution for collecting, analyzing, and visualizing bus travel data. By automating data extraction from Redbus and offering tools for data-driven decision-making, the project helps in improving operational efficiency and strategic planning.

## Business Use Cases

The solution can be applied to various scenarios including:
- **Travel Aggregators**: Providing real-time bus schedules and seat availability for customers.
- **Market Analysis**: Analyzing travel patterns and preferences for market research.
- **Customer Service**: Enhancing user experience with customized travel options based on data insights.
- **Competitor Analysis**: Comparing pricing and service levels with competitors.

## Approach

### Data Scraping

Automated the extraction of Redbus data, including routes, schedules, prices, and seat availability using Selenium.

### Data Storage

Stored the scraped data in a SQL database (SQLite).

### Data Analysis/Filtering using Streamlit

- Developed a Streamlit application to display and filter the scraped data. Incorporated filters such as bus type, route, price range, star rating, and availability. 
- Used sql and pandas queries to retrieve and filter data based on user inputs.

## Results

- Successfully scraped 4,396 bus information records from Redbus, including both private and government bus data for selected routes.
- Stored the data in a structured SQL database.
- Developed an interactive and user-friendly Streamlit application for data filtering and viewing.

## Data Set

- **Source**: Data scraped from the Redbus website.
- **Link**: [Redbus](https://www.redbus.in/)
- **Format**: The scraped data is stored in a SQL database.

### Data Set Requirements & Explanation

The dataset contains detailed information about bus services available on Redbus. Fields include:
- **Bus Routes Name**: Start and end locations of each bus journey.
- **Bus Routes Link**: Link for all the route details.
- **Bus Name**: Name of the bus or service provider.
- **Bus Type (Sleeper/Seater/AC/Non-AC)**: Specifies the bus type.
- **Departing Time**: Scheduled departure time.
- **Duration**: Total journey duration.
- **Reaching Time**: Expected arrival time.
- **Star Rating**: Rating provided by passengers.
- **Price**: Ticket cost.
- **Seat Availability**: Number of available seats.

## Database Schema

Table: **red-bus-data**

| Column Name    | Data Type | Description                            |
|----------------|------------|----------------------------------------|
| id             | INT        | Primary Key (Auto-increment)           |
| route_name     | TEXT       | Bus Route information for each state transport |
| route_link     | TEXT       | Link to the route details              |
| busname        | TEXT       | Name of the bus                        |
| bustype        | TEXT       | Type of the bus                        |
| departing_time | TIME       | Departure time                         |
| duration       | TEXT       | Duration of the journey                |
| reaching_time  | TIME       | Arrival time                           |
| star_rating    | FLOAT      | Rating of the bus                      |
| price          | DECIMAL    | Price of the ticket                    |
| seats_available| INT        | Number of seats available              |

## Project Deliverables

- **Source Code**: Python scripts for data scraping (`main.py`), SQL database interaction (`database.py`), and Streamlit application (`streamlitgui.py`).
- **Application using Streamlit**: Screenshots or links to the Streamlit application showing data filtering/analysis.


