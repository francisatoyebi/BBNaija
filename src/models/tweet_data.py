"""
Data models for tweet analysis.

This module defines immutable data structures following the
Single Responsibility Principle.
"""

from dataclasses import dataclass, field
from typing import Dict, List
import pandas as pd


@dataclass(frozen=True)
class TweetData:
    """
    Immutable data class representing tweet data for a housemate.
    
    Attributes:
        housemate_name: Name of the BBNaija housemate
        dataframe: Pandas DataFrame containing tweet data
        file_path: Path to the source CSV file
    """
    housemate_name: str
    dataframe: pd.DataFrame
    file_path: str
    
    def __post_init__(self):
        """Validate data after initialization."""
        if self.dataframe.empty:
            raise ValueError(f"DataFrame for {self.housemate_name} is empty")
        
        if not self.housemate_name:
            raise ValueError("Housemate name cannot be empty")
    
    @property
    def tweet_count(self) -> int:
        """Get the number of tweets in the dataset."""
        return len(self.dataframe)
    
    def __repr__(self) -> str:
        """String representation of TweetData."""
        return (f"TweetData(housemate='{self.housemate_name}', "
                f"tweets={self.tweet_count}, file='{self.file_path}')")


@dataclass
class AnalysisResult:
    """
    Data class representing sentiment analysis results.
    
    Attributes:
        housemate_ratings: Dictionary mapping housemate names to percentage ratings
        raw_scores: Dictionary mapping housemate names to raw sentiment scores
        total_tweets: Dictionary mapping housemate names to tweet counts
        results_dataframe: Pandas DataFrame with aggregated results
    """
    housemate_ratings: Dict[str, float] = field(default_factory=dict)
    raw_scores: Dict[str, float] = field(default_factory=dict)
    total_tweets: Dict[str, int] = field(default_factory=dict)
    results_dataframe: pd.DataFrame = field(default_factory=pd.DataFrame)
    
    def add_housemate_result(
        self, 
        name: str, 
        rating: float, 
        raw_score: float, 
        tweet_count: int
    ) -> None:
        """
        Add analysis result for a housemate.
        
        Args:
            name: Housemate name
            rating: Percentage rating (0-100)
            raw_score: Raw sentiment score
            tweet_count: Number of tweets analyzed
        """
        self.housemate_ratings[name] = rating
        self.raw_scores[name] = raw_score
        self.total_tweets[name] = tweet_count
    
    def get_sorted_ratings(self) -> List[tuple]:
        """
        Get ratings sorted by value (descending).
        
        Returns:
            List of (housemate, rating) tuples sorted by rating
        """
        return sorted(
            self.housemate_ratings.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
    
    def get_lowest_rated(self) -> tuple:
        """
        Get the housemate with the lowest rating.
        
        Returns:
            Tuple of (housemate_name, rating)
        """
        if not self.housemate_ratings:
            return None, 0.0
        
        return min(self.housemate_ratings.items(), key=lambda x: x[1])
    
    def get_highest_rated(self) -> tuple:
        """
        Get the housemate with the highest rating.
        
        Returns:
            Tuple of (housemate_name, rating)
        """
        if not self.housemate_ratings:
            return None, 0.0
        
        return max(self.housemate_ratings.items(), key=lambda x: x[1])
    
    def __repr__(self) -> str:
        """String representation of AnalysisResult."""
        return (f"AnalysisResult(housemates={len(self.housemate_ratings)}, "
                f"total_tweets={sum(self.total_tweets.values())})")

