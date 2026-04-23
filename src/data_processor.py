"""
Data processing and cleaning utilities for Strava activities.
Handles missing values, outliers, and data validation.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Data cleaning and preprocessing for Strava activity data.
    """
    
    @staticmethod
    def remove_outliers(df: pd.DataFrame, 
                       columns: list = ['distance_km', 'moving_time_min', 'elevation_gain_m'],
                       method: str = 'iqr',
                       threshold: float = 3.0) -> pd.DataFrame:
        """
        Remove outliers from specified columns.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input DataFrame
        columns : list
            Columns to check for outliers
        method : str, default 'iqr'
            Method for outlier detection ('iqr' or 'zscore')
        threshold : float, default 3.0
            Threshold for outlier detection
            
        Returns:
        --------
        pd.DataFrame : DataFrame with outliers removed
        """
        df_clean = df.copy()
        initial_rows = len(df_clean)
        
        for col in columns:
            if col not in df_clean.columns:
                continue
            
            if method == 'iqr':
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                mask = (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)
                
            elif method == 'zscore':
                z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
                mask = z_scores < threshold
            else:
                raise ValueError(f"Unknown method: {method}")
            
            df_clean = df_clean[mask]
        
        removed = initial_rows - len(df_clean)
        if removed > 0:
            logger.info(f"Removed {removed} outlier rows ({removed/initial_rows*100:.1f}%)")
        
        return df_clean
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, 
                             strategy: str = 'median') -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input DataFrame
        strategy : str, default 'median'
            Imputation strategy ('median', 'mean', 'drop', or 'forward')
            
        Returns:
        --------
        pd.DataFrame : DataFrame with missing values handled
        """
        df_clean = df.copy()
        
        numeric_cols = ['avg_heartrate', 'avg_watts', 'avg_speed_kmh', 'calories']
        
        for col in numeric_cols:
            if col in df_clean.columns and df_clean[col].isna().any():
                if strategy == 'median':
                    df_clean[col] = df_clean[col].fillna(df_clean[col].median())
                elif strategy == 'mean':
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
                elif strategy == 'forward':
                    df_clean[col] = df_clean[col].fillna(method='ffill')
                else:
                    logger.warning(f"Unknown strategy '{strategy}' for column {col}")
        
        critical_cols = ['distance_km', 'moving_time_min', 'activity_type']
        df_clean = df_clean.dropna(subset=critical_cols)
        
        return df_clean
    
    @staticmethod
    def validate_data(df: pd.DataFrame) -> Tuple[bool, dict]:
        """
        Validate data quality and return validation report.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input DataFrame
            
        Returns:
        --------
        tuple : (is_valid, report_dict)
        """
        report = {
            "total_rows": len(df),
            "total_athletes": df['athlete'].nunique() if 'athlete' in df.columns else 0,
            "date_range": None,
            "missing_values": df.isnull().sum().to_dict(),
            "duplicates": df.duplicated().sum(),
            "negative_values": {}
        }
        
        if 'date' in df.columns:
            report["date_range"] = {
                "min": df['date'].min(),
                "max": df['date'].max()
            }
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            negative_count = (df[col] < 0).sum()
            if negative_count > 0:
                report["negative_values"][col] = negative_count
        
        is_valid = (report["duplicates"] == 0 and 
                   len(report["negative_values"]) == 0 and
                   report["total_rows"] > 0)
        
        return is_valid, report
    
    @staticmethod
    def aggregate_weekly(df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate activity data by week for each athlete.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input DataFrame with 'date' column
            
        Returns:
        --------
        pd.DataFrame : Weekly aggregated statistics
        """
        if 'date' not in df.columns:
            raise ValueError("DataFrame must contain 'date' column")
        
        df_agg = df.copy()
        df_agg['date'] = pd.to_datetime(df_agg['date'])
        df_agg['week'] = df_agg['date'].dt.isocalendar().week
        df_agg['year'] = df_agg['date'].dt.year
        
        weekly_stats = df_agg.groupby(['athlete', 'year', 'week']).agg({
            'distance_km': ['sum', 'mean', 'std'],
            'moving_time_min': ['sum', 'mean'],
            'elevation_gain_m': ['sum', 'mean'],
            'activity_type': 'count',
            'avg_heartrate': 'mean',
            'avg_watts': 'mean'
        }).round(2)
        
        weekly_stats.columns = ['_'.join(col).strip() for col in weekly_stats.columns.values]
        weekly_stats = weekly_stats.rename(columns={'activity_type_count': 'activities_count'})
        weekly_stats = weekly_stats.reset_index()
        
        return weekly_stats
    
    @staticmethod
    def filter_by_date(df: pd.DataFrame, 
                       start_date: Optional[str] = None, 
                       end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Filter activities by date range.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input DataFrame
        start_date : str, optional
            Start date (YYYY-MM-DD)
        end_date : str, optional
            End date (YYYY-MM-DD)
            
        Returns:
        --------
        pd.DataFrame : Filtered DataFrame
        """
        df_filtered = df.copy()
        df_filtered['date'] = pd.to_datetime(df_filtered['date'])
        
        if start_date:
            df_filtered = df_filtered[df_filtered['date'] >= pd.to_datetime(start_date)]
        if end_date:
            df_filtered = df_filtered[df_filtered['date'] <= pd.to_datetime(end_date)]
        
        logger.info(f"Filtered from {len(df)} to {len(df_filtered)} rows")
        return df_filtered