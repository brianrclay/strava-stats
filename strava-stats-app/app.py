import os
import json
from datetime import datetime
import pandas as pd
import plotly
import plotly.express as px
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from src.utils.strava_client import StravaClient

# Load environment variables
load_dotenv()

# Debug: Print environment variables (without sensitive info)
print("Environment variables loaded:")
print(f"STRAVA_CLIENT_ID exists: {'STRAVA_CLIENT_ID' in os.environ}")
print(f"STRAVA_CLIENT_SECRET exists: {'STRAVA_CLIENT_SECRET' in os.environ}")
print(f"STRAVA_REFRESH_TOKEN exists: {'STRAVA_REFRESH_TOKEN' in os.environ}")

app = Flask(__name__, static_folder='src/static', template_folder='src/templates')
app.secret_key = os.getenv('SECRET_KEY', 'dev_key')

# Initialize Strava Client
strava_client = StravaClient(
    client_id=os.getenv('STRAVA_CLIENT_ID'),
    client_secret=os.getenv('STRAVA_CLIENT_SECRET'),
    refresh_token=os.getenv('STRAVA_REFRESH_TOKEN')
)

@app.route('/')
def index():
    print("Accessing index route")
    return render_template('index.html')

@app.route('/stats')
def get_stats():
    try:
        print("Fetching Strava activities...")
        # Fetch activities
        activities = strava_client.get_activities()
        print(f"Retrieved {len(activities)} activities")
        
        # Convert to DataFrame
        df = pd.DataFrame(activities)
        df['start_date'] = pd.to_datetime(df['start_date'])
        
        # Monthly Aggregations
        monthly_stats = df.groupby(pd.Grouper(key='start_date', freq='M')).agg({
            'distance': 'sum',
            'moving_time': 'sum',
            'total_elevation_gain': 'sum',
            'name': 'count'  # Count number of activities
        }).reset_index()
        
        # Yearly Aggregations
        yearly_stats = df.groupby(pd.Grouper(key='start_date', freq='Y')).agg({
            'distance': 'sum',
            'moving_time': 'sum',
            'total_elevation_gain': 'sum',
            'name': 'count'  # Count number of activities
        }).reset_index()
        
        # Create visualizations
        monthly_distance_fig = px.bar(
            monthly_stats, 
            x='start_date', 
            y='distance',
            title='Monthly Distance'
        )
        monthly_distance_json = json.dumps(monthly_distance_fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        yearly_distance_fig = px.bar(
            yearly_stats, 
            x='start_date', 
            y='distance',
            title='Yearly Distance'
        )
        yearly_distance_json = json.dumps(yearly_distance_fig, cls=plotly.utils.PlotlyJSONEncoder)
        
        response_data = {
            'monthly_stats': monthly_stats.to_dict(orient='records'),
            'yearly_stats': yearly_stats.to_dict(orient='records'),
            'monthly_distance_chart': monthly_distance_json,
            'yearly_distance_chart': yearly_distance_json
        }
        print("Successfully processed stats")
        return jsonify(response_data)
    except Exception as e:
        print(f"Error in /stats endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5050)
