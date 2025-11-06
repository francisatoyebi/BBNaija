"""
Configuration management for BBNaija sentiment analysis.

This module centralizes all configuration settings following the
Single Responsibility Principle.
"""

from typing import Dict, Any
from pathlib import Path


class Config:
    """
    Configuration manager for BBNaija analysis.
    
    Handles all application settings including file paths, chart settings,
    and analysis parameters.
    """
    
    # Default paths
    DEFAULT_DATA_PATH = "Scraped_tweets/"
    DEFAULT_OUTPUT_PATH = "Analysis_results/"
    
    # Chart settings
    CHART_DPI = 500
    CHART_TITLE_SIZE = 15
    PIE_OUTER_RADIUS = 1.0
    PIE_INNER_RADIUS = 0.6
    PIE_CENTER_COLOR = 'white'
    
    # File settings
    VALID_FILE_EXTENSION = ".csv"
    REQUIRED_COLUMNS = ['date', 'tweet', 'urls']
    
    # Analysis settings
    TWITTER_DOMAIN = "twitter.com"
    
    def __init__(self, data_path: str = None, output_path: str = None):
        """
        Initialize configuration.
        
        Args:
            data_path: Path to directory containing tweet CSV files
            output_path: Path to save output charts
        """
        self.data_path = Path(data_path) if data_path else Path(self.DEFAULT_DATA_PATH)
        self.output_path = Path(output_path) if output_path else Path(self.DEFAULT_OUTPUT_PATH)
        
    def get_pie_chart_path(self) -> Path:
        """Get the full path for pie chart output."""
        return self.output_path / "bbnaija_pie.png"
    
    def get_bar_chart_path(self) -> Path:
        """Get the full path for bar chart output."""
        return self.output_path / "bbnaija_bar.png"
    
    def validate_paths(self) -> bool:
        """
        Validate that required paths exist.
        
        Returns:
            bool: True if paths are valid, False otherwise
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data path does not exist: {self.data_path}")
        
        if not self.data_path.is_dir():
            raise NotADirectoryError(f"Data path is not a directory: {self.data_path}")
        
        # Create output directory if it doesn't exist
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict containing configuration parameters
        """
        return {
            'data_path': str(self.data_path),
            'output_path': str(self.output_path),
            'chart_dpi': self.CHART_DPI,
            'chart_title_size': self.CHART_TITLE_SIZE,
            'valid_extension': self.VALID_FILE_EXTENSION,
            'required_columns': self.REQUIRED_COLUMNS
        }

