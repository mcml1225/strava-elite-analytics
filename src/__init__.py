"""
Strava Elite Athletes Analytics Platform (SEAAP)
A data science project for analyzing training patterns of elite athletes
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .athletes_db import ATHLETES_DB, get_athletes_by_discipline, get_active_athletes, get_athlete_ids
from .strava_client import StravaClient
from .data_processor import DataProcessor
from .feature_engineering import FeatureEngineer
from .models import AthleteClusterer, IntensityPredictor
from .visualizer import Visualizer

__all__ = [
    "ATHLETES_DB",
    "get_athletes_by_discipline",
    "get_active_athletes",
    "get_athlete_ids",
    "StravaClient",
    "DataProcessor",
    "FeatureEngineer",
    "AthleteClusterer",
    "IntensityPredictor",
    "Visualizer",
]