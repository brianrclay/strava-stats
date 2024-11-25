import requests
from datetime import datetime, timedelta

class StravaClient:
    def __init__(self, client_id, client_secret, refresh_token):
        print(f"\nInitializing StravaClient...")
        print(f"Client ID: {client_id}")
        print(f"Client Secret: {client_secret[:4]}...{client_secret[-4:]}")
        print(f"Refresh Token: {refresh_token[:4]}...{refresh_token[-4:]}")
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = self._refresh_access_token()

    def _refresh_access_token(self):
        """Refresh Strava access token"""
        print("\nRefreshing access token...")
        try:
            response = requests.post(
                'https://www.strava.com/oauth/token',
                data={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'grant_type': 'refresh_token',
                    'refresh_token': self.refresh_token
                }
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            token_data = response.json()
            print("Successfully refreshed access token")
            return token_data['access_token']
        except Exception as e:
            print(f"Error refreshing access token: {str(e)}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            raise

    def get_activities(self, limit=100):
        """Fetch Strava activities"""
        print("\nFetching Strava activities...")
        try:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            params = {
                'per_page': limit,
                'page': 1
            }
            
            response = requests.get(
                'https://www.strava.com/api/v3/athlete/activities',
                headers=headers,
                params=params
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            
            activities = []
            for activity in response.json():
                activities.append({
                    'name': activity['name'],
                    'type': activity['type'],
                    'start_date': activity['start_date'],
                    'distance': activity['distance'],  # in meters
                    'moving_time': activity['moving_time'],  # in seconds
                    'total_elevation_gain': activity['total_elevation_gain']  # in meters
                })
            
            print(f"Successfully retrieved {len(activities)} activities")
            return activities
        except Exception as e:
            print(f"Error fetching activities: {str(e)}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            raise
