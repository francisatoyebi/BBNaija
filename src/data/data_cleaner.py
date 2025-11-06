"""
Data cleaning module for tweet data.

This module handles cleaning and preprocessing of tweet data following
the Single Responsibility Principle.
"""

import pandas as pd
import numpy as np
import logging
from typing import List

from ..models.tweet_data import TweetData
from ..config import Config

logger = logging.getLogger(__name__)


class TweetDataCleaner:
    """
    Cleans and preprocesses tweet data.
    
    Responsible for data cleaning operations including URL cleaning,
    ad removal, and column selection.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the data cleaner.
        
        Args:
            config: Configuration object
        """
        self.config = config
    
    def clean_tweet_data(self, tweet_data: TweetData) -> pd.DataFrame:
        """
        Clean tweet data for a single housemate.
        
        Args:
            tweet_data: TweetData object to clean
            
        Returns:
            Cleaned pandas DataFrame
        """
        logger.info(f"Cleaning data for {tweet_data.housemate_name}")
        
        # Create a copy to avoid modifying original
        df = tweet_data.dataframe.copy()
        
        # Select required columns
        df = self._select_required_columns(df)
        
        # Clean URL column
        df = self._clean_urls(df)
        
        # Remove ads
        df = self._remove_ads(df)
        
        # Remove rows with missing data
        df = self._remove_missing_data(df)
        
        logger.info(
            f"Cleaned data for {tweet_data.housemate_name}: "
            f"{len(df)} tweets remaining (from {tweet_data.tweet_count})"
        )
        
        return df
    
    def clean_all_tweet_data(self, tweet_data_list: List[TweetData]) -> List[tuple]:
        """
        Clean data for all housemates.
        
        Args:
            tweet_data_list: List of TweetData objects
            
        Returns:
            List of tuples (housemate_name, cleaned_dataframe)
        """
        cleaned_data = []
        
        for tweet_data in tweet_data_list:
            try:
                cleaned_df = self.clean_tweet_data(tweet_data)
                cleaned_data.append((tweet_data.housemate_name, cleaned_df))
            except Exception as e:
                logger.error(
                    f"Failed to clean data for {tweet_data.housemate_name}: {e}"
                )
                # Continue with other housemates
                continue
        
        return cleaned_data
    
    def _select_required_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Select only required columns from DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with only required columns
        """
        try:
            df = df[self.config.REQUIRED_COLUMNS].copy()
            logger.debug("Selected required columns")
            return df
        except KeyError as e:
            logger.error(f"Missing required columns: {e}")
            raise
    
    def _clean_urls(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the URLs column by extracting domain.
        
        Args:
            df: DataFrame with 'urls' column
            
        Returns:
            DataFrame with cleaned URLs
        """
        try:
            # Strip brackets
            df['urls'] = df['urls'].apply(lambda text: str(text).strip('[]'))
            
            # Split by forward slash
            df['urls'] = df['urls'].apply(lambda text: text.split('/'))
            
            # Extract domain (third element if exists)
            df['urls'] = df['urls'].apply(
                lambda parts: '' if len(parts) < 3 else parts[2]
            )
            
            logger.debug("Cleaned URLs column")
            return df
            
        except Exception as e:
            logger.error(f"Error cleaning URLs: {e}")
            raise
    
    def _remove_ads(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove advertisement posts from data.
        
        Ads are identified as posts with URLs that are not from twitter.com.
        
        Args:
            df: DataFrame with cleaned 'urls' column
            
        Returns:
            DataFrame with ads removed
        """
        try:
            df['urls'] = df['urls'].apply(self._filter_non_twitter_urls)
            logger.debug("Removed advertisement posts")
            return df
            
        except Exception as e:
            logger.error(f"Error removing ads: {e}")
            raise
    
    def _filter_non_twitter_urls(self, url: str) -> str:
        """
        Filter out non-Twitter URLs (likely ads).
        
        Args:
            url: URL string to check
            
        Returns:
            URL if valid, NaN if ad
        """
        # If URL is longer than twitter.com domain and not twitter.com, it's likely an ad
        if len(url) > len(self.config.TWITTER_DOMAIN):
            if url != self.config.TWITTER_DOMAIN:
                return np.nan
        
        return url
    
    def _remove_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows with missing data.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            DataFrame with missing data removed
        """
        initial_count = len(df)
        df = df.dropna()
        removed_count = initial_count - len(df)
        
        if removed_count > 0:
            logger.debug(f"Removed {removed_count} rows with missing data")
        
        return df

