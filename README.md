# Car Subscription Dashboard

A data analytics dashboard built with Streamlit that visualizes metrics for a car subscription service.

## Features

- Usage insights by brand and car type
- Subscription analytics and churn metrics
- Maintenance cost analysis
- Kilometer distribution trends

## Setup

1. Install requirements:
```sh
pip install -r requirements.txt
```

2. Generate sample data:
```sh 
python data/generate_data.py
```

3. Prepare visualization data:
```sh
python app/EDA.py
```

4. Run dashboard:
```sh
streamlit run app/dashboard.py
```

## Data Structure

The dashboard uses SQLite database with the following tables:
- customers: Customer information
- cars: Available car models 
- subscriptions: Active subscriptions
- usage: Monthly usage data
- maintenance: Maintenance records