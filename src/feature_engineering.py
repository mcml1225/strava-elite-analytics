"""
Feature engineering for Strava activity data.
Calculates advanced metrics like TRIMP, intensity zones, and training load.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Feature engineering class for creating advanced training metrics.
    """
    
    @staticmethod
    def calculate_age(row, current_year: int = None) -> Optional[int]:
        """
        Calculate age from birth year.
        
        Parameters:
        -----------
        row : pd.Series
            Row containing 'birth_year'
        current_year : int, optional
            Current year for age calculation
            
        Returns:
        --------
        int or None: Age or None if birth_year missing
        """
        if current_year is None:
            current_year = pd.Timestamp.now().year
        
        birth_year = row.get('birth_year')
        if birth_year and not pd.isna(birth_year):
            return current_year - birth_year
        return None
    
    @staticmethod
    def calculate_intensity_zone(heartrate: float, max_hr: float = None, age: int = None) -> str:
        """
        Calculate heart rate intensity zone.
        
        Parameters:
        -----------
        heartrate : float
            Average heart rate for the activity
        max_hr : float, optional
            Maximum heart rate (if known)
        age : int, optional
            Age to estimate max HR (220 - age)
            
        Returns:
        --------
        str : Intensity zone label
        """
        if heartrate is None or pd.isna(heartrate):
            return "No data"
        
        # Estimate max HR if not provided
        if max_hr is None and age is not None:
            max_hr = 220 - age
        elif max_hr is None:
            return "No max HR"
        
        percentage = (heartrate / max_hr) * 100
        
        if percentage < 60:
            return "Zone 1 (Recovery)"
        elif percentage < 70:
            return "Zone 2 (Endurance)"
        elif percentage < 80:
            return "Zone 3 (Tempo)"
        elif percentage < 90:
            return "Zone 4 (Threshold)"
        else:
            return "Zone 5 (Maximum)"
    
    @staticmethod
    def calculate_trimp(heartrate: float, duration_min: float, age: int = None, 
                        max_hr: float = None, rest_hr: float = 60) -> Optional[float]:
        """
        Calculate TRIMP (Training Impulse) - a measure of training load.
        
        Parameters:
        -----------
        heartrate : float
            Average heart rate during activity
        duration_min : float
            Activity duration in minutes
        age : int, optional
            Age for max HR estimation
        max_hr : float, optional
            Maximum heart rate (if known)
        rest_hr : float, default 60
            Resting heart rate
            
        Returns:
        --------
        float or None : TRIMP value
        """
        if heartrate is None or pd.isna(heartrate) or duration_min is None:
            return None
        
        # Estimate max HR if not provided
        if max_hr is None and age is not None:
            max_hr = 220 - age
        elif max_hr is None:
            return None
        
        # Calculate heart rate ratio
        hr_ratio = (heartrate - rest_hr) / (max_hr - rest_hr)
        
        # TRIMP exponential formula
        # TRIMP = duration * HR_ratio * 0.64 * exp(1.92 * HR_ratio)
        trimp = duration_min * hr_ratio * 0.64 * np.exp(1.92 * hr_ratio)
        
        return round(trimp, 2)
    
    @staticmethod
    def calculate_training_load(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate additional training load metrics.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with activities
            
        Returns:
        --------
        pd.DataFrame : DataFrame with training load columns added
        """
        df_copy = df.copy()
        
        # Calculate intensity zone for each activity
        df_copy['intensity_zone'] = df_copy.apply(
            lambda row: FeatureEngineer.calculate_intensity_zone(
                row.get('avg_heartrate'), 
                age=row.get('age')
            ), 
            axis=1
        )
        
        # Calculate TRIMP for each activity
        df_copy['trimp'] = df_copy.apply(
            lambda row: FeatureEngineer.calculate_trimp(
                row.get('avg_heartrate'),
                row.get('moving_time_min'),
                age=row.get('age')
            ),
            axis=1
        )
        
        # Calculate training pace (min/km)
        df_copy['pace_min_per_km'] = df_copy.apply(
            lambda row: row['moving_time_min'] / row['distance_km'] 
            if row['distance_km'] > 0 else None,
            axis=1
        )
        
        return df_copy
    
    @staticmethod
    def calculate_intensity_zones(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate and add intensity zones to DataFrame.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with heart rate data
            
        Returns:
        --------
        pd.DataFrame : DataFrame with intensity_zone column
        """
        df_copy = df.copy()
        
        df_copy['intensity_zone'] = df_copy.apply(
            lambda row: FeatureEngineer.calculate_intensity_zone(
                row.get('avg_heartrate'),
                age=row.get('age')
            ),
            axis=1
        )
        
        return df_copy
    
    @staticmethod
    def get_weekly_summary(df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate weekly training summary.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with activities
            
        Returns:
        --------
        pd.DataFrame : Weekly summary statistics
        """
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['date'])
        df_copy['week'] = df_copy['date'].dt.isocalendar().week
        df_copy['year'] = df_copy['date'].dt.year
        
        weekly_summary = df_copy.groupby(['athlete', 'year', 'week']).agg({
            'distance_km': ['sum', 'mean', 'count'],
            'moving_time_min': ['sum', 'mean'],
            'elevation_gain_m': ['sum'],
            'avg_heartrate': 'mean',
            'trimp': 'sum'
        }).round(2)
        
        # Flatten column names
        weekly_summary.columns = ['_'.join(col).strip() for col in weekly_summary.columns.values]
        weekly_summary = weekly_summary.rename(columns={'distance_km_count': 'activities_count'})
        
        return weekly_summary.reset_index()
    
    @staticmethod
    def get_discipline_distribution(df: pd.DataFrame) -> pd.DataFrame:
        """
        Get distribution of activity types per athlete.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with activities
            
        Returns:
        --------
        pd.DataFrame : Pivot table of activity types
        """
        return pd.crosstab(df['athlete'], df['activity_type'])