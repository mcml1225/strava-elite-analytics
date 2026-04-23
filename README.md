# Strava Elite Athletes Analytics Platform (SEAAP)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Strava API](https://img.shields.io/badge/Strava-API-orange.svg)](https://developers.strava.com)

## IMPORTANT DISCLAIMER

> **This project demonstrates a complete data science pipeline for elite athlete analysis.**
>
> **Current Status:** The code is FULLY FUNCTIONAL and ready to extract real Strava data. However, due to Strava's API privacy restrictions, it can only access data from athletes who have explicitly authorized your application.
>
> **What This Project Does:**
> - Connects to Strava API with OAuth authentication
> - Extracts activities, heart rate, power, and elevation data
> - Processes and cleans real athletic data
> - Engineers features (TRIMP, intensity zones, weekly aggregates)
> - Runs clustering and predictive ML models
> - Generates professional visualizations
>
> **To Use With Real Data:** You need authorization from the athletes you want to analyze. The code is ready.

## Project Overview

SEAAP is a production-ready data science platform that:
1. Authenticates with Strava API using OAuth 2.0
2. Extracts training data (HR, power, distance, elevation)
3. Processes and cleans the data
4. Engineers advanced features (TRIMP, intensity zones)
5. Models athlete clusters and predicts performance
6. Visualizes training patterns and insights

## Architecture
Strava API (with athlete authorization)
|
v
OAuth Authentication
|
v
Data Extractor (strava_client.py)
|
v
Data Processor (data_processor.py)
|
v
Feature Engineer (feature_engineering.py)
|
v
+-----------+-----------+
| |
v v
Clustering Prediction
(K-Means) (Random Forest)
| |
+-----------+-----------+
|
v
Visualizer (visualizer.py)
|
v
Reports & CSV Exports



## Installation


### Clone repository
git clone https://github.com/yourusername/strava-elite-analytics.git
cd strava-elite-analytics

### Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### Install dependencies
pip install -r requirements.txt

### Configure Strava API credentials
cp .env.example .env
### Edit .env with your Strava API credentials
Authentication Setup
Create an app at Strava API Settings

Get your Client ID and Client Secret

Generate an access token with scopes: read,activity:read_all,profile:read_all

Add credentials to .env:

env
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_ACCESS_TOKEN=your_access_token
Running the Pipeline

python main.py
What Happens During Execution:
Authentication - Connects to Strava API with your token

Data Extraction - Fetches activities from athletes in the database

Processing - Cleans and validates the data

Feature Engineering - Calculates TRIMP, intensity zones, weekly aggregates

ML Models - Runs clustering and prediction algorithms

Visualization - Generates plots and reports

Expected Output (with authorized athletes):

============================================================
### STRAVA ELITE ATHLETES ANALYTICS PLATFORM
============================================================

[1/6] Initializing Strava client...
Authenticated as: [Your Name]

[2/6] Collecting athlete data...
Found 23 athletes with Strava IDs
Collecting data for Gerda Steyn (ID: 17233801)...
Fetched 30 activities
Collected 30 activities for Gerda Steyn
...
Total data collected: 480 activities from 23 athletes

[3/6] Processing and cleaning data...
Removed 12 outlier rows (2.5%)

[4/6] Engineering features...
Calculated intensity zones for 468 activities
Calculated TRIMP for 468 activities

[5/6] Running machine learning models...
Identified 3 athlete clusters
Heart rate prediction model - R-squared: 0.723

[6/6] Generating visualizations...
Weekly volume plot saved
Intensity distribution plot saved
Athlete comparison plot saved

ANALYSIS COMPLETE!
Output Files
File	Description
data/raw/strava_elite_data.csv	Raw activities from Strava API
data/processed/strava_elite_features.csv	Engineered features (TRIMP, zones)
data/processed/weekly_aggregates.csv	Weekly training summaries
reports/figures/weekly_volume.png	Weekly distance by athlete
reports/figures/intensity_distribution.png	Heart rate zone distribution
reports/figures/athlete_comparison.png	Radar chart comparison
reports/analysis_report.txt	Complete  report
Research Questions
With proper athlete authorization, this platform can answer:

Periodization Patterns: How do athletes taper before competitions?

Intensity Distribution: What percentage of training is in each HR zone?

Athlete Profiling: Can we cluster athletes by training style?

Predictive Modeling: Can training load predict performance?

Technical Stack
Component	Technology
API Client	Stravalib
Data Processing	Pandas, NumPy
ML Models	Scikit-learn (K-Means, Random Forest)
Visualization	Matplotlib, Seaborn
Authentication	OAuth 2.0
Code Structure

strava-elite-analytics/
├── src/
│   ├── athletes_db.py          # 23 elite athlete profiles
│   ├── strava_client.py        # OAuth + API calls
│   ├── data_processor.py       # Cleaning & validation
│   ├── feature_engineering.py  # TRIMP, zones, pace
│   ├── models.py               # K-Means, Random Forest
│   └── visualizer.py           # Matplotlib plots
├── data/                       # Extracted data (CSV)
├── reports/                    # Outputs & figures
├── main.py                     # Complete pipeline
├── requirements.txt            # Dependencies
└── README.md                   # This file
Privacy & Ethics
This project:

Does not collect any personal data without authorization

Respects Strava's API Terms of Service

Is for educational purposes only

To use with real data, you must:

Have explicit authorization from athletes

Comply with Strava API Terms of Service

Respect athlete privacy preferences

License
MIT License - See LICENSE file for details

Acknowledgments
Strava for providing the API

Elite athletes who choose to share their training publicly

Open source community
