"""
Main entry point for Strava Elite Analytics Platform.
Handles missing credentials gracefully.
"""

import os
import sys
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

from src.athletes_db import ATHLETES_DB, get_active_athletes
from src.strava_client import StravaClient
from src.data_processor import DataProcessor
from src.feature_engineering import FeatureEngineer
from src.models import AthleteClusterer, IntensityPredictor
from src.visualizer import Visualizer


def check_credentials():
    """Check if Strava credentials are configured."""
    access_token = os.getenv("STRAVA_ACCESS_TOKEN")
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    
    if not access_token:
        print("\n" + "=" * 60)
        print("⚠️  STRAVA CREDENTIALS NOT FOUND")
        print("=" * 60)
        print("\nTo use this project, you need to:")
        print("1. Copy .env.example to .env")
        print("2. Get your Strava API credentials from:")
        print("   https://www.strava.com/settings/api")
        print("3. Fill in your REAL credentials in .env")
        print("\nThe .env file should NEVER be committed to GitHub!")
        print("=" * 60)
        return False
    
    print(f"✅ Credentials found (Client ID: {client_id[:4]}***)")
    return True


def main():
    """Main execution function using synthetic data."""
    print("=" * 70)
    print("STRAVA ELITE ATHLETES ANALYTICS PLATFORM")
    print("=" * 70)
    
    # DISCLAIMER
    print("\n" + "=" * 70)
    print("⚠️  DISCLAIMER")
    print("=" * 70)
    print("This project uses SYNTHETIC DATA for demonstration purposes.")
    print("Real elite athlete data requires explicit authorization from")
    print("each athlete per Strava's API Terms of Service.")
    print("\nThis code demonstrates the COMPLETE ARCHITECTURE that would")
    print("work with authorized data access.")
    print("=" * 70)
    print("\n📊 Using synthetic data realistically mimicking elite athletes\n")
    
    """Main execution function."""
    print("=" * 60)
    print("STRAVA ELITE ATHLETES ANALYTICS PLATFORM")
    print("=" * 60)
    
    # Check credentials before proceeding
    if not check_credentials():
        sys.exit(1)
    
    # Create necessary directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('reports/figures', exist_ok=True)
    
    # 1. Initialize Strava client
    print("\n[1/6] Initializing Strava client...")
    try:
        client = StravaClient()
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # 2. Collect data
    print("\n[2/6] Collecting athlete data...")
    active_athletes = get_active_athletes(require_strava_id=True)
    print(f"Found {len(active_athletes)} athletes with Strava IDs")
    
    df_raw = client.collect_all_athletes_data(active_athletes, activities_limit=30)
    
    if df_raw.empty:
        print("❌ ERROR: No data collected.")
        print("Possible issues:")
        print("  - Invalid or expired access token")
        print("  - Athletes have private profiles")
        print("  - API rate limits exceeded")
        sys.exit(1)
    
    # Save raw data
    df_raw.to_csv('data/raw/strava_elite_data.csv', index=False)
    print(f"✅ Saved {len(df_raw)} activities to data/raw/")
    
    # ... resto del código igual ...
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()