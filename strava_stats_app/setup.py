from setuptools import setup, find_packages

setup(
    name="strava_stats_app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.2',
        'gunicorn==21.2.0',
        'requests==2.31.0',
        'python-dotenv==1.0.0',
        'pandas==2.0.1',
        'plotly==5.15.0',
        'numpy==1.24.3',
        'Werkzeug==2.3.7',
    ],
)
