# Air-quality-analysis
This web application is built using Flask and provides insightful visualizations and analyses of air pollution levels across Indian cities from 2020 to 2024. It includes features such as city-wise PM2.5 trend analysis, AQI categorization, and data preview, using interactive plots generated with Seaborn and Matplotlib.
 Dataset Collection Information
Dataset File: air_pollution_data.csv

Data Columns Required:

Date, PM2.5, PM10, NO2, CO, O3, City

Source Assumption: The dataset is expected to be a time-series CSV file, possibly collected from open government data portals such as the Central Pollution Control Board (CPCB) or data.gov.in.

Data Processing Includes:

Standardization of column names

Missing data handling

Conversion of date strings to datetime objects

Categorization of air quality levels based on PM2.5 values
