"""
Rating calculation module.

This module handles calculation and normalization of ratings following
the Single Responsibility Principle.
"""

import pandas as pd
import logging
from typing import Dict, List, Tuple

from ..models.tweet_data import AnalysisResult

logger = logging.getLogger(__name__)


class RatingCalculator:
    """
    Calculates and normalizes ratings from sentiment scores.
    
    Responsible for converting sentiment scores into percentage ratings
    and aggregating results.
    """
    
    def __init__(self):
        """Initialize the rating calculator."""
        logger.info("Initialized rating calculator")
    
    def calculate_rating(
        self, 
        df: pd.DataFrame, 
        housemate_name: str
    ) -> Tuple[float, int]:
        """
        Calculate rating for a single housemate.
        
        Args:
            df: DataFrame with 'compound' sentiment scores
            housemate_name: Name of the housemate
            
        Returns:
            Tuple of (average_rating, tweet_count)
            
        Raises:
            ValueError: If DataFrame is empty or missing 'compound' column
        """
        if df.empty:
            raise ValueError(f"Cannot calculate rating for empty DataFrame ({housemate_name})")
        
        if 'compound' not in df.columns:
            raise KeyError(f"DataFrame must have 'compound' column ({housemate_name})")
        
        tweet_count = len(df)
        average_rating = df['compound'].mean()
        
        logger.info(
            f"Rating for {housemate_name}: {average_rating:.4f} "
            f"(from {tweet_count} tweets)"
        )
        
        return average_rating, tweet_count
    
    def calculate_all_ratings(
        self, 
        analyzed_data: List[Tuple[str, pd.DataFrame]]
    ) -> AnalysisResult:
        """
        Calculate ratings for all housemates and normalize to percentages.
        
        Args:
            analyzed_data: List of tuples (housemate_name, dataframe_with_scores)
            
        Returns:
            AnalysisResult object with all ratings and statistics
        """
        logger.info("Calculating ratings for all housemates")
        
        if not analyzed_data:
            raise ValueError("No data provided for rating calculation")
        
        # Calculate raw ratings for each housemate
        raw_ratings = {}
        tweet_counts = {}
        
        for housemate_name, df in analyzed_data:
            try:
                rating, count = self.calculate_rating(df, housemate_name)
                raw_ratings[housemate_name] = rating
                tweet_counts[housemate_name] = count
            except Exception as e:
                logger.error(f"Failed to calculate rating for {housemate_name}: {e}")
                continue
        
        if not raw_ratings:
            raise ValueError("Failed to calculate any ratings")
        
        # Normalize ratings to percentages
        normalized_ratings = self._normalize_to_percentages(raw_ratings)
        
        # Create result object
        result = AnalysisResult()
        
        for housemate_name in raw_ratings.keys():
            result.add_housemate_result(
                name=housemate_name,
                rating=normalized_ratings[housemate_name],
                raw_score=raw_ratings[housemate_name],
                tweet_count=tweet_counts[housemate_name]
            )
        
        # Create results DataFrame
        result.results_dataframe = self._create_results_dataframe(
            normalized_ratings, 
            raw_ratings, 
            tweet_counts
        )
        
        logger.info(f"Calculated ratings for {len(raw_ratings)} housemate(s)")
        
        return result
    
    def _normalize_to_percentages(self, raw_ratings: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize ratings to percentages that sum to 100.
        
        Args:
            raw_ratings: Dictionary of housemate: raw_rating
            
        Returns:
            Dictionary of housemate: percentage_rating
        """
        # Calculate total of all ratings
        total = sum(raw_ratings.values())
        
        if total == 0:
            logger.warning("Total rating is zero, using equal distribution")
            # If all ratings are zero, distribute equally
            equal_share = 100.0 / len(raw_ratings)
            return {name: equal_share for name in raw_ratings.keys()}
        
        # Normalize to percentages
        normalized = {
            name: (rating / total) * 100 
            for name, rating in raw_ratings.items()
        }
        
        logger.debug(f"Normalized ratings: {normalized}")
        
        return normalized
    
    def _create_results_dataframe(
        self, 
        normalized_ratings: Dict[str, float],
        raw_ratings: Dict[str, float],
        tweet_counts: Dict[str, int]
    ) -> pd.DataFrame:
        """
        Create a DataFrame summarizing all results.
        
        Args:
            normalized_ratings: Percentage ratings
            raw_ratings: Raw sentiment scores
            tweet_counts: Tweet counts per housemate
            
        Returns:
            DataFrame with columns: housemate, rating, raw_score, tweet_count
        """
        df = pd.DataFrame({
            'housemate': list(normalized_ratings.keys()),
            'rating': list(normalized_ratings.values()),
            'raw_score': [raw_ratings[name] for name in normalized_ratings.keys()],
            'tweet_count': [tweet_counts[name] for name in normalized_ratings.keys()]
        })
        
        # Sort by rating (descending)
        df = df.sort_values('rating', ascending=False).reset_index(drop=True)
        
        logger.debug(f"Created results DataFrame with {len(df)} rows")
        
        return df
    
    def get_eviction_prediction(self, result: AnalysisResult) -> Tuple[str, float]:
        """
        Predict which housemate is most likely to be evicted.
        
        Based on sentiment analysis, the housemate with the lowest
        rating is most likely to be evicted.
        
        Args:
            result: AnalysisResult object
            
        Returns:
            Tuple of (housemate_name, rating)
        """
        lowest_rated = result.get_lowest_rated()
        
        if lowest_rated[0] is None:
            logger.warning("No housemate data available for prediction")
            return None, 0.0
        
        logger.info(
            f"Eviction prediction: {lowest_rated[0]} "
            f"(rating: {lowest_rated[1]:.2f}%)"
        )
        
        return lowest_rated

