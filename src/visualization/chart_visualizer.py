"""
Chart visualization module.

This module handles creation of charts and plots following the
Single Responsibility Principle.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import logging
from typing import List
from pathlib import Path

from ..models.tweet_data import AnalysisResult
from ..config import Config

logger = logging.getLogger(__name__)


class ChartVisualizer:
    """
    Creates and saves visualization charts.
    
    Responsible for generating pie charts and bar charts from
    analysis results.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the chart visualizer.
        
        Args:
            config: Configuration object containing chart settings
        """
        self.config = config
        
        # Set style for better-looking charts
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (10, 8)
        
        logger.info("Initialized chart visualizer")
    
    def create_all_charts(self, result: AnalysisResult) -> None:
        """
        Create and save all visualization charts.
        
        Args:
            result: AnalysisResult object containing rating data
        """
        logger.info("Creating visualization charts")
        
        if not result.housemate_ratings:
            logger.warning("No data to visualize")
            return
        
        # Create pie chart
        self.create_pie_chart(result)
        
        # Create bar chart
        self.create_bar_chart(result)
        
        logger.info("All charts created successfully")
    
    def create_pie_chart(self, result: AnalysisResult) -> None:
        """
        Create and save a donut pie chart of ratings.
        
        Args:
            result: AnalysisResult object containing rating data
        """
        logger.info("Creating pie chart")
        
        # Extract data
        housemates = list(result.housemate_ratings.keys())
        ratings = list(result.housemate_ratings.values())
        
        # Create figure
        plt.figure(figsize=(10, 8))
        
        # Create outer pie chart with data
        plt.pie(
            ratings, 
            labels=housemates, 
            autopct='%1.1f%%',
            startangle=90,
            radius=self.config.PIE_OUTER_RADIUS,
            normalize=True
        )
        
        # Create inner circle for donut effect
        centre_circle = plt.Circle(
            (0, 0), 
            self.config.PIE_INNER_RADIUS, 
            fc=self.config.PIE_CENTER_COLOR
        )
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        
        # Set title
        plt.title(
            'Viewers Tweet Rating for This Week', 
            size=self.config.CHART_TITLE_SIZE,
            weight='bold',
            pad=20
        )
        
        # Equal aspect ratio ensures circular pie
        plt.axis('equal')
        
        # Save chart
        output_path = self.config.get_pie_chart_path()
        plt.savefig(output_path, dpi=self.config.CHART_DPI, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Pie chart saved to: {output_path}")
    
    def create_bar_chart(self, result: AnalysisResult) -> None:
        """
        Create and save a bar chart of ratings.
        
        Args:
            result: AnalysisResult object containing rating data
        """
        logger.info("Creating bar chart")
        
        # Extract data
        housemates = list(result.housemate_ratings.keys())
        ratings = list(result.housemate_ratings.values())
        
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Create bar plot
        bars = plt.bar(housemates, ratings, color=sns.color_palette("husl", len(housemates)))
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2., 
                height,
                f'{height:.1f}%',
                ha='center', 
                va='bottom',
                fontsize=10,
                weight='bold'
            )
        
        # Set labels and title
        plt.ylabel('Percentage Rating', fontsize=12, weight='bold')
        plt.xlabel('Housemates', fontsize=12, weight='bold')
        plt.title(
            'Viewers Tweet Rating for This Week', 
            size=self.config.CHART_TITLE_SIZE,
            weight='bold',
            pad=20
        )
        
        # Rotate x-axis labels if needed
        plt.xticks(rotation=45, ha='right')
        
        # Add grid for better readability
        plt.grid(axis='y', alpha=0.3)
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save chart
        output_path = self.config.get_bar_chart_path()
        plt.savefig(output_path, dpi=self.config.CHART_DPI, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Bar chart saved to: {output_path}")
    
    def display_results_summary(self, result: AnalysisResult) -> None:
        """
        Display a text summary of analysis results.
        
        Args:
            result: AnalysisResult object containing rating data
        """
        print("\n" + "=" * 60)
        print("BBNaija Sentiment Analysis Results")
        print("=" * 60)
        
        # Sort by rating (descending)
        sorted_ratings = result.get_sorted_ratings()
        
        print("\nHousemate Ratings (sorted by percentage):")
        print("-" * 60)
        
        for rank, (housemate, rating) in enumerate(sorted_ratings, 1):
            tweet_count = result.total_tweets.get(housemate, 0)
            raw_score = result.raw_scores.get(housemate, 0)
            
            print(f"{rank}. {housemate:15s} | "
                  f"Rating: {rating:6.2f}% | "
                  f"Tweets: {tweet_count:5d} | "
                  f"Sentiment: {raw_score:+.4f}")
        
        print("-" * 60)
        
        # Display eviction prediction
        lowest = result.get_lowest_rated()
        highest = result.get_highest_rated()
        
        if lowest[0]:
            print(f"\n🔴 Most likely to be EVICTED: {lowest[0]} ({lowest[1]:.2f}%)")
        
        if highest[0]:
            print(f"🟢 Most likely to be SAVED: {highest[0]} ({highest[1]:.2f}%)")
        
        total_tweets = sum(result.total_tweets.values())
        print(f"\nTotal tweets analyzed: {total_tweets:,}")
        
        print("=" * 60 + "\n")

