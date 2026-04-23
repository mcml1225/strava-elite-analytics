"""
Strava API Client for extracting athlete activities.
Handles authentication, rate limiting, and data collection.
"""

import os
import time
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
from dotenv import load_dotenv
from stravalib import Client
# ELIMINAR esta línea: from stravalib.model import Activity
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class StravaClient:
    """
    Client for interacting with Strava API V3.
    Handles authentication, activity fetching, and rate limiting.
    """
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Strava client with authentication.
        """
        self.client = Client()
        
        if access_token:
            self.access_token = access_token
        else:
            self.access_token = os.getenv("STRAVA_ACCESS_TOKEN")
        
        if self.access_token:
            self.client.access_token = self.access_token
            logger.info("Strava client initialized successfully")
        else:
            logger.warning("No access token found. Please check your .env file")
        
        self.request_count = 0
        self.last_request_time = None
    
    def _rate_limit_wait(self):
        """Implement rate limiting to respect Strava's API limits."""
        self.request_count += 1
        
        if self.request_count >= 90:
            logger.info("Rate limit approaching. Waiting 15 minutes...")
            time.sleep(900)
            self.request_count = 0
        
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            if elapsed < 0.1:
                time.sleep(0.1 - elapsed)
        
        self.last_request_time = time.time()
    
    def get_athlete_profile(self, athlete_id: str) -> Optional[Dict]:
        """Fetch basic profile information for an athlete."""
        try:
            self._rate_limit_wait()
            athlete = self.client.get_athlete(athlete_id)
            
            return {
                "id": athlete.id,
                "name": f"{athlete.firstname} {athlete.lastname}",
                "city": athlete.city if hasattr(athlete, 'city') else None,
                "country": athlete.country if hasattr(athlete, 'country') else None,
                "sex": athlete.sex if hasattr(athlete, 'sex') else None,
                "weight": float(athlete.weight) if hasattr(athlete, 'weight') and athlete.weight else None,
            }
        except Exception as e:
            logger.error(f"Error fetching profile for athlete {athlete_id}: {e}")
            return None
    
    def get_activities(self, athlete_id: str = None, limit: int = 30) -> List:
        """
        Fetch recent activities.
        En stravalib 1.7, get_activities no acepta athlete_id como parámetro.
        Obtiene las actividades del atleta autenticado (dueño del token).
        """
        try:
            self._rate_limit_wait()
            # En versión 1.7, get_activities no toma athlete_id
            activities = list(self.client.get_activities(limit=limit))
            logger.info(f"Fetched {len(activities)} activities")
            return activities
        except Exception as e:
            logger.error(f"Error fetching activities: {e}")
            return []
    
    def activity_to_dict(self, activity, athlete_name: str, discipline: str) -> Dict:
        """Convert a Strava Activity object to a dictionary."""
        # Basic metrics (always available)
        data = {
            "athlete": athlete_name,
            "discipline": discipline,
            "date": activity.start_date,
            "activity_id": activity.id,
            "activity_name": activity.name if hasattr(activity, 'name') else None,
            "activity_type": activity.type,
            "distance_km": float(activity.distance) / 1000 if activity.distance else 0,
            "moving_time_min": float(activity.moving_time) / 60 if activity.moving_time else 0,
            "elapsed_time_min": float(activity.elapsed_time) / 60 if activity.elapsed_time else 0,
            "elevation_gain_m": float(activity.total_elevation_gain) if activity.total_elevation_gain else 0,
        }
        
        # Optional metrics
        if hasattr(activity, 'average_heartrate') and activity.average_heartrate:
            data["avg_heartrate"] = float(activity.average_heartrate)
            data["max_heartrate"] = float(activity.max_heartrate) if activity.max_heartrate else None
        else:
            data["avg_heartrate"] = None
            data["max_heartrate"] = None
        
        if hasattr(activity, 'average_watts') and activity.average_watts:
            data["avg_watts"] = float(activity.average_watts)
            data["max_watts"] = float(activity.max_watts) if hasattr(activity, 'max_watts') else None
        else:
            data["avg_watts"] = None
            data["max_watts"] = None
        
        if hasattr(activity, 'average_speed') and activity.average_speed:
            data["avg_speed_kmh"] = float(activity.average_speed) * 3.6
        else:
            data["avg_speed_kmh"] = None
        
        if hasattr(activity, 'kilojoules') and activity.kilojoules:
            data["calories"] = float(activity.kilojoules)
        else:
            data["calories"] = None
        
        return data
    
    def collect_athlete_data(self, athlete_name: str, athlete_info: Dict, 
                             activities_limit: int = 30) -> pd.DataFrame:
        """
        Collect all data for a single athlete.
        NOTA: La API de Strava solo permite ver actividades del atleta autenticado.
        """
        logger.info(f"Collecting activities for {athlete_name}...")
        
        activities = self.get_activities(limit=activities_limit)
        
        if not activities:
            logger.warning(f"No activities found")
            return pd.DataFrame()
        
        data_rows = []
        for activity in activities:
            row = self.activity_to_dict(activity, athlete_name, athlete_info["discipline"])
            
            # Add athlete metadata
            row["birth_year"] = athlete_info.get("birth_year")
            row["country"] = athlete_info.get("country")
            row["profile_type"] = athlete_info.get("profile_type")
            
            # Calculate age
            if athlete_info.get("birth_year"):
                current_year = datetime.now().year
                row["age"] = current_year - athlete_info["birth_year"]
            else:
                row["age"] = None
            
            data_rows.append(row)
        
        df = pd.DataFrame(data_rows)
        logger.info(f"Collected {len(df)} activities for {athlete_name}")
        
        return df
    
    def collect_all_athletes_data(self, athletes_db: Dict, 
                                   activities_limit: int = 30) -> pd.DataFrame:
        """
        Collect data for all athletes in the database.
        """
        all_dfs = []
        
        for athlete_name, athlete_info in athletes_db.items():
            if not athlete_info.get("strava_id"):
                logger.info(f"Skipping {athlete_name} (no Strava ID)")
                continue
                
            df = self.collect_athlete_data(athlete_name, athlete_info, activities_limit)
            if not df.empty:
                all_dfs.append(df)
            time.sleep(1)
        
        if all_dfs:
            combined = pd.concat(all_dfs, ignore_index=True)
            logger.info(f"Total data collected: {len(combined)} activities")
            return combined
        
        logger.warning("No data collected")
        return pd.DataFrame()