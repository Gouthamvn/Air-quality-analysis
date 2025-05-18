from flask import Flask, render_template, request, url_for
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Load the dataset
data_path = 'air_pollution_data.csv'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Dataset not found: {data_path}")

data = pd.read_csv(data_path)

# Standardize column names
data.columns = data.columns.str.strip().str.lower()

# Expected column mappings
column_mapping = {
    'datetime': 'Date',
    'pm2.5': 'PM2.5',
    'pm10': 'PM10',
    'no2': 'NO2',
    'co': 'CO',
    'o3': 'O3',
    'city': 'City'
}
data.rename(columns=column_mapping, inplace=True)

# Ensure required columns exist
required_columns = {'Date', 'PM2.5', 'PM10', 'NO2', 'CO', 'O3', 'City'}
missing_columns = required_columns - set(data.columns)
if missing_columns:
    raise ValueError(f"Dataset is missing required columns: {missing_columns}")

# Convert Date column to datetime format
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data.dropna(subset=['Date'], inplace=True)
data.sort_values(by='Date', inplace=True)

# Function to categorize AQI based on PM2.5 levels
def calculate_aqi_category(pm25_value):
    if pd.isna(pm25_value):
        return 'Unknown'
    if pm25_value <= 50:
        return 'Good'
    elif pm25_value <= 100:
        return 'Satisfactory'
    elif pm25_value <= 200:
        return 'Moderate'
    elif pm25_value <= 300:
        return 'Poor'
    elif pm25_value <= 400:
        return 'Very Poor'
    else:
        return 'Severe'

data['AQI_Category'] = data['PM2.5'].apply(calculate_aqi_category)

# Ensure static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

# Generate overall PM2.5 plot
def generate_pm25_plot():
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='Date', y='PM2.5', hue='AQI_Category', palette='viridis')
    plt.title('PM2.5 Levels Over Time (India 2020-2024)')
    plt.xlabel('Date')
    plt.ylabel('PM2.5 Concentration (µg/m³)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plot_path = os.path.join('static', 'plot.png')
    plt.savefig(plot_path)
    plt.close()

generate_pm25_plot()

@app.route('/')
def index():
    plot_url = url_for('static', filename='plot.png')
    return render_template('index.html', plot_url=plot_url)

@app.route('/data-preview')
def data_preview():
    first_5_rows = data.head().to_html(classes="styled-table", index=False)
    return render_template('table.html', title="First 5 Rows of the Dataset", table_data=first_5_rows)

@app.route('/null-check')
def null_check():
    null_values = data.isnull().sum().to_frame(name="Missing Values").reset_index()
    null_values_html = null_values.to_html(classes="styled-table", index=False)
    return render_template('table.html', title="Missing Values in the Dataset", table_data=null_values_html)

@app.route('/city', methods=['GET', 'POST'])
def city_analysis():
    if request.method == 'POST':
        city_name = request.form['city'].strip()
        city_data = data[data['City'].str.lower() == city_name.lower()]
        if city_data.empty:
            return render_template('city.html', city=city_name, plot_url=None, message="No data found for this city.")
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=city_data, x='Date', y='PM2.5', hue='AQI_Category', palette='coolwarm')
        plt.title(f'PM2.5 Levels Over Time in {city_name}')
        plt.xlabel('Date')
        plt.ylabel('PM2.5 Concentration (µg/m³)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot_filename = f'plot_{city_name.lower().replace(" ", "_")}.png'
        plot_path = os.path.join('static', plot_filename)
        plt.savefig(plot_path)
        plt.close()
        plot_url = url_for('static', filename=plot_filename)
        return render_template('city.html', city=city_name, plot_url=plot_url, message=None)
    return render_template('city_form.html')

if __name__ == '__main__':
    app.run(debug=True)
