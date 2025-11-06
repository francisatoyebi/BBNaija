"""
Data loading module for tweet CSV files.

This module handles loading tweet data from CSV files following the
Single Responsibility Principle.
"""

import pandas as pd
import logging
from pathlib import Path
from typing import List

from ..models.tweet_data import TweetData
from ..utils.file_utils import FileUtils
from ..config import Config

logger = logging.getLogger(__name__)


class TweetDataLoader:
    """
    Loads tweet data from CSV files.
    
    Responsible for discovering CSV files and loading them into
    TweetData objects.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the data loader.
        
        Args:
            config: Configuration object containing data paths
        """
        self.config = config
        self.file_utils = FileUtils()
    
    def load_all_tweets(self) -> List[TweetData]:
        """
        Load all tweet CSV files from the configured directory.
        
        Returns:
            List of TweetData objects
            
        Raises:
            FileNotFoundError: If data directory doesn't exist
            ValueError: If no valid CSV files found
        """
        logger.info(f"Loading tweets from: {self.config.data_path}")
        
        # Find all CSV files
        csv_files = self.file_utils.find_csv_files(self.config.data_path)
        
        if not csv_files:
            raise ValueError(f"No CSV files found in {self.config.data_path}")
        
        # Load each CSV file
        tweet_data_list = []
        for filename, housemate_name in csv_files:
            try:
                tweet_data = self._load_single_file(filename, housemate_name)
                tweet_data_list.append(tweet_data)
                logger.info(f"Loaded {tweet_data.tweet_count} tweets for {housemate_name}")
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}")
                # Continue loading other files
                continue
        
        if not tweet_data_list:
            raise ValueError("Failed to load any valid tweet data")
        
        logger.info(f"Successfully loaded data for {len(tweet_data_list)} housemate(s)")
        return tweet_data_list
    
    def _load_single_file(self, filename: str, housemate_name: str) -> TweetData:
        """
        Load a single CSV file into a TweetData object.
        
        Args:
            filename: Name of the CSV file
            housemate_name: Name of the housemate
            
        Returns:
            TweetData object
            
        Raises:
            FileNotFoundError: If file doesn't exist
            pd.errors.EmptyDataError: If file is empty
            ValueError: If required columns are missing
        """
        file_path = self.config.data_path / filename
        
        # Validate file exists
        if not self.file_utils.validate_file_path(file_path):
            raise FileNotFoundError(f"Cannot read file: {file_path}")
        
        try:
            # Load CSV
            df = pd.read_csv(file_path)
            
            # Validate DataFrame
            if df.empty:
                raise ValueError(f"CSV file is empty: {filename}")
            
            # Check for required columns
            self._validate_columns(df, filename)
            
            # Create TweetData object
            tweet_data = TweetData(
                housemate_name=housemate_name,
                dataframe=df,
                file_path=str(file_path)
            )
            
            return tweet_data
            
        except pd.errors.EmptyDataError:
            logger.error(f"Empty CSV file: {filename}")
            raise
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            raise
    
    def _validate_columns(self, df: pd.DataFrame, filename: str) -> None:
        """
        Validate that DataFrame has required columns.
        
        Args:
            df: DataFrame to validate
            filename: Name of the file (for error messages)
            
        Raises:
            ValueError: If required columns are missing
        """
        required_cols = set(self.config.REQUIRED_COLUMNS)
        actual_cols = set(df.columns)
        
        missing_cols = required_cols - actual_cols
        
        if missing_cols:
            raise ValueError(
                f"File {filename} is missing required columns: {missing_cols}"
            )
        
        logger.debug(f"Validated columns for {filename}")

