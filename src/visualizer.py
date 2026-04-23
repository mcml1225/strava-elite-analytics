"""
Visualization utilities for Strava Elite Analytics.
Creates plots for training volume, intensity distribution, and athlete comparisons.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

# Set style for better looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")


class Visualizer:
    """
    Visualization class for creating training analytics plots.
    """
    
    def __init__(self, figsize: tuple = (12, 6), dpi: int = 100):
        """
        Initialize the visualizer.
        
        Parameters:
        -----------
        figsize : tuple, default (12, 6)
            Default figure size
        dpi : int, default 100
            Default figure DPI
        """
        self.figsize = figsize
        self.dpi = dpi
    
    def plot_weekly_volume(self, weekly_df: pd.DataFrame, 
                           save_path: Optional[str] = None,
                           title: str = "Weekly Training Volume by Athlete") -> plt.Figure:
        """
        Plot weekly training distance for each athlete.
        
        Parameters:
        -----------
        weekly_df : pd.DataFrame
            DataFrame with weekly aggregated data
        save_path : str, optional
            Path to save the figure
        title : str, default "Weekly Training Volume by Athlete"
            Plot title
            
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Get unique athletes
        athletes = weekly_df['athlete'].unique()
        
        # Plot each athlete's weekly volume
        for athlete in athletes:
            athlete_data = weekly_df[weekly_df['athlete'] == athlete]
            ax.plot(athlete_data['week_start'], athlete_data['distance_km_sum'], 
                   marker='o', linewidth=2, markersize=6, label=athlete)
        
        ax.set_xlabel('Week', fontsize=12)
        ax.set_ylabel('Total Distance (km)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved weekly volume plot to {save_path}")
        
        return fig
    
    def plot_intensity_distribution(self, df: pd.DataFrame, 
                                     save_path: Optional[str] = None,
                                     title: str = "Training Intensity Distribution by Athlete") -> plt.Figure:
        """
        Plot distribution of intensity zones for each athlete.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with intensity_zone column
        save_path : str, optional
            Path to save the figure
        title : str, default "Training Intensity Distribution by Athlete"
            Plot title
            
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Filter rows with intensity zone data
        df_plot = df[df['intensity_zone'].notna()].copy()
        
        if df_plot.empty:
            ax.text(0.5, 0.5, 'No intensity data available', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        # Create crosstab for heatmap
        intensity_counts = pd.crosstab(df_plot['athlete'], df_plot['intensity_zone'])
        
        # Plot heatmap
        im = ax.imshow(intensity_counts.values, cmap='YlOrRd', aspect='auto')
        
        # Add labels
        ax.set_xticks(range(len(intensity_counts.columns)))
        ax.set_xticklabels(intensity_counts.columns, rotation=45, ha='right')
        ax.set_yticks(range(len(intensity_counts.index)))
        ax.set_yticklabels(intensity_counts.index)
        
        # Add colorbar
        plt.colorbar(im, ax=ax, label='Number of Activities')
        
        ax.set_xlabel('Intensity Zone', fontsize=12)
        ax.set_ylabel('Athlete', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved intensity distribution plot to {save_path}")
        
        return fig
    
    def plot_athlete_comparison(self, df: pd.DataFrame, 
                                 save_path: Optional[str] = None,
                                 title: str = "Athlete Training Comparison") -> plt.Figure:
        """
        Create a comparison radar chart for top athletes.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with athlete activities
        save_path : str, optional
            Path to save the figure
        title : str, default "Athlete Training Comparison"
            Plot title
            
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        # Aggregate metrics per athlete
        athlete_metrics = df.groupby('athlete').agg({
            'distance_km': 'mean',
            'moving_time_min': 'mean',
            'elevation_gain_m': 'mean',
            'avg_heartrate': 'mean'
        }).round(2)
        
        # Normalize metrics for radar chart (0-1 scale)
        metrics_normalized = (athlete_metrics - athlete_metrics.min()) / (athlete_metrics.max() - athlete_metrics.min())
        metrics_normalized = metrics_normalized.fillna(0)
        
        # Select top athletes (up to 5)
        top_athletes = metrics_normalized.head(min(5, len(metrics_normalized)))
        
        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi, subplot_kw=dict(projection='polar'))
        
        categories = metrics_normalized.columns.tolist()
        N = len(categories)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Plot each athlete
        colors = plt.cm.Set3(np.linspace(0, 1, len(top_athletes)))
        
        for i, (athlete, row) in enumerate(top_athletes.iterrows()):
            values = row.values.tolist()
            values += values[:1]  # Close the loop
            
            ax.plot(angles, values, 'o-', linewidth=2, label=athlete, color=colors[i])
            ax.fill(angles, values, alpha=0.1, color=colors[i])
        
        # Set category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(0, 1)
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved athlete comparison plot to {save_path}")
        
        return fig
    
    def plot_heartrate_trend(self, df: pd.DataFrame, 
                              athlete: Optional[str] = None,
                              save_path: Optional[str] = None,
                              title: str = "Heart Rate Trend Over Time") -> plt.Figure:
        """
        Plot heart rate trend over time for a specific athlete or all.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with activities
        athlete : str, optional
            Specific athlete to plot. If None, plots all.
        save_path : str, optional
            Path to save the figure
        title : str, default "Heart Rate Trend Over Time"
            Plot title
            
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        df_plot = df[df['avg_heartrate'].notna()].copy()
        
        if df_plot.empty:
            ax.text(0.5, 0.5, 'No heart rate data available', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        if athlete:
            df_plot = df_plot[df_plot['athlete'] == athlete]
            ax.plot(pd.to_datetime(df_plot['date']), df_plot['avg_heartrate'], 
                   'o-', linewidth=1, markersize=4, color='steelblue')
            ax.set_title(f"Heart Rate Trend - {athlete}", fontsize=14, fontweight='bold')
        else:
            # Plot each athlete with different colors
            athletes = df_plot['athlete'].unique()
            for i, ath in enumerate(athletes):
                athlete_data = df_plot[df_plot['athlete'] == ath]
                ax.plot(pd.to_datetime(athlete_data['date']), athlete_data['avg_heartrate'], 
                       'o-', linewidth=1, markersize=3, label=ath, alpha=0.7)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.set_title(title, fontsize=14, fontweight='bold')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Average Heart Rate (bpm)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved heart rate trend plot to {save_path}")
        
        return fig
    
    def plot_activity_type_distribution(self, df: pd.DataFrame, 
                                         save_path: Optional[str] = None,
                                         title: str = "Activity Type Distribution") -> plt.Figure:
        """
        Plot distribution of activity types.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with activities
        save_path : str, optional
            Path to save the figure
        title : str, default "Activity Type Distribution"
            Plot title
            
        Returns:
        --------
        plt.Figure : Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.dpi)
        
        activity_counts = df['activity_type'].value_counts()
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(activity_counts)))
        wedges, texts, autotexts = ax.pie(activity_counts.values, 
                                           labels=activity_counts.index,
                                           autopct='%1.1f%%',
                                           colors=colors,
                                           explode=[0.02] * len(activity_counts))
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Saved activity distribution plot to {save_path}")
        
        return fig