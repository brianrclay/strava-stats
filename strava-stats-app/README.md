# Strava Performance Dashboard

## Overview
A responsive web application that pulls and visualizes your Strava activity data, providing monthly and yearly performance statistics.

## Prerequisites
- Python 3.8+
- Strava Developer Account
- Strava API Credentials

## Deployment Instructions (Render.com)

1. Create a new account on [Render.com](https://render.com)

2. Click on "New +" and select "Web Service"

3. Connect your GitHub repository

4. Configure the following settings:
   - Name: strava-stats (or your preferred name)
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.app:app -c gunicorn_config.py`

5. Add the following environment variables:
   ```
   STRAVA_CLIENT_ID=your_client_id
   STRAVA_CLIENT_SECRET=your_client_secret
   STRAVA_REFRESH_TOKEN=your_refresh_token
   ```

6. Click "Create Web Service"

Your app will be deployed and available at a URL like: `https://your-app-name.onrender.com`

## Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/strava-stats-app.git
cd strava-stats-app
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure Strava API Credentials
- Go to [Strava Developers](https://www.strava.com/settings/api)
- Create an application to get your Client ID and Client Secret
- Update `.env` with your credentials

5. Run the application
```bash
python src/app.py
```

## Features
- Monthly activity statistics
- Yearly activity statistics
- Interactive charts using Plotly
- Responsive design

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Strava credentials:
   ```
   STRAVA_CLIENT_ID=your_client_id
   STRAVA_CLIENT_SECRET=your_client_secret
   STRAVA_REFRESH_TOKEN=your_refresh_token
   ```

4. Run the application:
   ```bash
   python src/app.py
   ```

Visit `http://localhost:5050` in your browser.

## Technologies
- Flask
- Pandas
- Plotly
- Strava API

## License
MIT License
