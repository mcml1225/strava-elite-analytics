"""
Machine learning models for athlete analysis.
Includes clustering for athlete profiling and predictive models for intensity.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from typing import Optional, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


class AthleteClusterer:
    """
    Clustering model to identify athlete training profiles.
    """
    
    def __init__(self, n_clusters: int = 3, random_state: int = 42):
        """
        Initialize the clusterer.
        
        Parameters:
        -----------
        n_clusters : int, default 3
            Number of clusters to create
        random_state : int, default 42
            Random seed for reproducibility
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = None
        self.scaler = None
    
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for clustering.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with athlete activities
            
        Returns:
        --------
        pd.DataFrame : Aggregated features per athlete
        """
        # Aggregate metrics per athlete
        athlete_features = df.groupby('athlete').agg({
            'distance_km': ['mean', 'std', 'sum'],
            'moving_time_min': ['mean', 'sum'],
            'avg_heartrate': 'mean',
            'elevation_gain_m': ['mean', 'sum'],
            'activity_type': lambda x: x.nunique()  # Sport diversity
        }).round(2)
        
        # Flatten column names
        athlete_features.columns = ['_'.join(col).strip() for col in athlete_features.columns.values]
        
        # Rename for clarity
        athlete_features = athlete_features.rename(columns={
            'activity_type_<lambda_0>': 'sport_diversity'
        })
        
        # Fill NaN values
        athlete_features = athlete_features.fillna(0)
        
        return athlete_features
    
    def cluster_athletes(self, df: pd.DataFrame, n_clusters: int = None) -> Tuple[pd.DataFrame, Any, Any]:
        """
        Cluster athletes based on their training patterns.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with athlete activities
        n_clusters : int, optional
            Number of clusters (overrides instance value)
            
        Returns:
        --------
        tuple : (clustered_df, kmeans_model, scaler)
        """
        if n_clusters is None:
            n_clusters = self.n_clusters
        
        # Prepare features
        features_df = self.prepare_features(df)
        
        if len(features_df) < n_clusters:
            logger.warning(f"Not enough athletes ({len(features_df)}) for {n_clusters} clusters")
            features_df['cluster'] = 0
            return features_df, None, None
        
        # Scale features
        self.scaler = StandardScaler()
        features_scaled = self.scaler.fit_transform(features_df)
        
        # Apply K-Means
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state, n_init=10)
        clusters = self.kmeans.fit_predict(features_scaled)
        
        # Add cluster labels to dataframe
        features_df['cluster'] = clusters
        
        # Add cluster centers to features_df for interpretation
        cluster_centers = self.scaler.inverse_transform(self.kmeans.cluster_centers_)
        center_cols = [f'center_{col}' for col in features_df.columns[:-1]]
        for i, center in enumerate(cluster_centers):
            for j, col in enumerate(features_df.columns[:-1]):
                features_df.loc[features_df['cluster'] == i, f'center_{col}'] = center[j]
        
        logger.info(f"Created {n_clusters} clusters with {len(features_df)} athletes")
        
        return features_df, self.kmeans, self.scaler
    
    def get_cluster_profiles(self, clustered_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate descriptive profiles for each cluster.
        
        Parameters:
        -----------
        clustered_df : pd.DataFrame
            DataFrame with cluster assignments
            
        Returns:
        --------
        pd.DataFrame : Cluster profiles
        """
        # Exclude center columns for profile calculation
        feature_cols = [col for col in clustered_df.columns if not col.startswith('center_') and col != 'cluster']
        
        profile = clustered_df.groupby('cluster')[feature_cols].mean().round(2)
        
        # Add cluster size
        profile['cluster_size'] = clustered_df['cluster'].value_counts().sort_index()
        
        return profile


class IntensityPredictor:
    """
    Predictive model for heart rate intensity based on training load.
    """
    
    def __init__(self, model_type: str = 'random_forest', random_state: int = 42):
        """
        Initialize the predictor.
        
        Parameters:
        -----------
        model_type : str, default 'random_forest'
            Type of model to use ('linear' or 'random_forest')
        random_state : int, default 42
            Random seed for reproducibility
        """
        self.model_type = model_type
        self.random_state = random_state
        self.model = None
        self.feature_names = None
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare features for prediction.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with activities
            
        Returns:
        --------
        tuple : (X_features, y_target)
        """
        # Sort by date for each athlete
        df_sorted = df.sort_values(['athlete', 'date']).copy()
        
        # Create lag features
        df_sorted['prev_distance'] = df_sorted.groupby('athlete')['distance_km'].shift(1)
        df_sorted['prev_duration'] = df_sorted.groupby('athlete')['moving_time_min'].shift(1)
        df_sorted['prev_elevation'] = df_sorted.groupby('athlete')['elevation_gain_m'].shift(1)
        
        # Rolling averages (last 3 activities)
        df_sorted['rolling_3_volume'] = df_sorted.groupby('athlete')['distance_km'].transform(
            lambda x: x.rolling(3, min_periods=1).mean()
        )
        
        # Day of week
        df_sorted['day_of_week'] = pd.to_datetime(df_sorted['date']).dt.dayofweek
        
        # Feature columns
        feature_cols = [
            'prev_distance', 'prev_duration', 'prev_elevation',
            'rolling_3_volume', 'day_of_week', 'elevation_gain_m'
        ]
        
        # Drop rows with NaN in features or target
        df_clean = df_sorted.dropna(subset=feature_cols + ['avg_heartrate'])
        
        if len(df_clean) < 10:
            logger.warning(f"Not enough data for prediction: {len(df_clean)} rows")
            return None, None
        
        X = df_clean[feature_cols]
        y = df_clean['avg_heartrate']
        
        self.feature_names = feature_cols
        
        return X, y
    
    def train_model(self, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """
        Train the prediction model.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with activities
            
        Returns:
        --------
        dict or None : Model results including metrics and coefficients
        """
        X, y = self.prepare_features(df)
        
        if X is None or len(X) < 10:
            logger.warning("Insufficient data for model training")
            return None
        
        # Select model
        if self.model_type == 'linear':
            self.model = LinearRegression()
        else:
            self.model = RandomForestRegressor(n_estimators=100, random_state=self.random_state)
        
        # Train model
        self.model.fit(X, y)
        
        # Make predictions
        predictions = self.model.predict(X)
        
        # Calculate metrics
        rmse = np.sqrt(mean_squared_error(y, predictions))
        r2 = r2_score(y, predictions)
        
        results = {
            'model': self.model,
            'rmse': round(rmse, 2),
            'r2': round(r2, 3),
            'predictions': predictions,
            'actual': y.values,
            'feature_names': self.feature_names
        }
        
        # Add coefficients for linear regression
        if self.model_type == 'linear':
            results['coefficients'] = dict(zip(self.feature_names, self.model.coef_))
            results['intercept'] = self.model.intercept_
        else:
            # Feature importance for Random Forest
            results['feature_importance'] = dict(zip(self.feature_names, self.model.feature_importances_))
        
        logger.info(f"Model trained - R²: {r2:.3f}, RMSE: {rmse:.2f}")
        
        return results
    
    def predict(self, features: pd.DataFrame) -> np.ndarray:
        """
        Make predictions using trained model.
        
        Parameters:
        -----------
        features : pd.DataFrame
            Features for prediction
            
        Returns:
        --------
        np.ndarray : Predicted heart rate values
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        return self.model.predict(features)
    
    def get_feature_importance(self) -> Optional[pd.DataFrame]:
        """
        Get feature importance if using Random Forest.
        
        Returns:
        --------
        pd.DataFrame or None : Feature importance DataFrame
        """
        if self.model is None:
            return None
        
        if self.model_type == 'random_forest' and hasattr(self.model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
            return importance_df
        
        return None