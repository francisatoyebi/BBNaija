"""
Sentiment analysis module for tweets.

This module handles sentiment analysis of tweets using VADER following
the Single Responsibility Principle.
"""

import pandas as pd
import logging
from typing import Dict
from nltk.sentiment.vader import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """
    Performs sentiment analysis on tweet text.
    
    Uses VADER (Valence Aware Dictionary and sEntiment Reasoner)
    for sentiment analysis of social media text.
    """
    
    def __init__(self):
        """Initialize the sentiment analyzer with VADER."""
        try:
            self.analyzer = SentimentIntensityAnalyzer()
            logger.info("Initialized VADER sentiment analyzer")
        except LookupError as e:
            logger.error(
                "VADER lexicon not found. Please run: "
                "nltk.download('vader_lexicon')"
            )
            raise e
    
    def analyze_tweet(self, tweet_text: str) -> Dict[str, float]:
        """
        Analyze sentiment of a single tweet.
        
        Args:
            tweet_text: Text content of the tweet
            
        Returns:
            Dictionary containing sentiment scores:
                - 'neg': Negative sentiment score (0-1)
                - 'neu': Neutral sentiment score (0-1)
                - 'pos': Positive sentiment score (0-1)
                - 'compound': Compound score (-1 to +1)
        """
        try:
            scores = self.analyzer.polarity_scores(tweet_text)
            return scores
        except Exception as e:
            logger.warning(f"Error analyzing tweet: {e}")
            # Return neutral scores on error
            return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
    
    def analyze_dataframe(self, df: pd.DataFrame, text_column: str = 'tweet') -> pd.DataFrame:
        """
        Analyze sentiment for all tweets in a DataFrame.
        
        Args:
            df: DataFrame containing tweets
            text_column: Name of column containing tweet text
            
        Returns:
            DataFrame with added sentiment scores
            
        Raises:
            KeyError: If text_column doesn't exist in DataFrame
        """
        if text_column not in df.columns:
            raise KeyError(f"Column '{text_column}' not found in DataFrame")
        
        logger.info(f"Analyzing sentiment for {len(df)} tweets")
        
        # Create a copy to avoid modifying original
        df = df.copy()
        
        # Analyze each tweet
        df['scores'] = df[text_column].apply(self.analyze_tweet)
        
        # Extract compound score for easy access
        df['compound'] = df['scores'].apply(lambda x: x['compound'])
        
        # Extract individual sentiment components
        df['positive'] = df['scores'].apply(lambda x: x['pos'])
        df['negative'] = df['scores'].apply(lambda x: x['neg'])
        df['neutral'] = df['scores'].apply(lambda x: x['neu'])
        
        logger.info("Sentiment analysis completed")
        
        return df
    
    def get_average_sentiment(self, df: pd.DataFrame) -> float:
        """
        Calculate average compound sentiment score.
        
        Args:
            df: DataFrame with 'compound' column
            
        Returns:
            Average compound sentiment score
            
        Raises:
            KeyError: If 'compound' column doesn't exist
            ValueError: If DataFrame is empty
        """
        if df.empty:
            raise ValueError("Cannot calculate average sentiment for empty DataFrame")
        
        if 'compound' not in df.columns:
            raise KeyError("DataFrame must have 'compound' column")
        
        average_sentiment = df['compound'].mean()
        
        logger.debug(f"Average sentiment: {average_sentiment:.4f}")
        
        return average_sentiment
    
    def get_sentiment_statistics(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Get detailed sentiment statistics.
        
        Args:
            df: DataFrame with sentiment scores
            
        Returns:
            Dictionary containing:
                - 'mean': Mean compound score
                - 'median': Median compound score
                - 'std': Standard deviation
                - 'min': Minimum score
                - 'max': Maximum score
                - 'positive_ratio': Ratio of positive tweets (compound > 0.05)
                - 'negative_ratio': Ratio of negative tweets (compound < -0.05)
                - 'neutral_ratio': Ratio of neutral tweets
        """
        if 'compound' not in df.columns:
            raise KeyError("DataFrame must have 'compound' column")
        
        if df.empty:
            return {}
        
        compound_scores = df['compound']
        
        # Calculate ratios based on compound score thresholds
        positive_count = (compound_scores > 0.05).sum()
        negative_count = (compound_scores < -0.05).sum()
        neutral_count = len(compound_scores) - positive_count - negative_count
        
        total = len(compound_scores)
        
        statistics = {
            'mean': compound_scores.mean(),
            'median': compound_scores.median(),
            'std': compound_scores.std(),
            'min': compound_scores.min(),
            'max': compound_scores.max(),
            'positive_ratio': positive_count / total if total > 0 else 0,
            'negative_ratio': negative_count / total if total > 0 else 0,
            'neutral_ratio': neutral_count / total if total > 0 else 0,
        }
        
        return statistics

