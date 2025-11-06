"""
File utility functions.

This module provides helper functions for file operations following
the Single Responsibility Principle.
"""

import os
from pathlib import Path
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class FileUtils:
    """
    Utility class for file operations.
    
    Handles file system operations including validation, discovery,
    and path management.
    """
    
    @staticmethod
    def is_csv_file(filename: str) -> bool:
        """
        Check if a filename has .csv extension.
        
        Args:
            filename: Name of the file to check
            
        Returns:
            bool: True if file is a CSV, False otherwise
        """
        return filename.lower().endswith('.csv')
    
    @staticmethod
    def get_filename_without_extension(filename: str) -> str:
        """
        Extract filename without extension.
        
        Args:
            filename: Full filename with extension
            
        Returns:
            str: Filename without extension
        """
        return Path(filename).stem
    
    @staticmethod
    def find_csv_files(directory: Path) -> List[Tuple[str, str]]:
        """
        Find all CSV files in a directory.
        
        Args:
            directory: Path to search for CSV files
            
        Returns:
            List of tuples (filename, housemate_name)
        """
        if not directory.exists():
            logger.error(f"Directory does not exist: {directory}")
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        if not directory.is_dir():
            logger.error(f"Path is not a directory: {directory}")
            raise NotADirectoryError(f"Not a directory: {directory}")
        
        csv_files = []
        
        try:
            for filename in os.listdir(directory):
                if FileUtils.is_csv_file(filename):
                    housemate_name = FileUtils.get_filename_without_extension(filename)
                    csv_files.append((filename, housemate_name))
                    logger.debug(f"Found CSV file: {filename} for {housemate_name}")
        except PermissionError as e:
            logger.error(f"Permission denied accessing directory: {directory}")
            raise e
        
        if not csv_files:
            logger.warning(f"No CSV files found in directory: {directory}")
        else:
            logger.info(f"Found {len(csv_files)} CSV file(s) in {directory}")
        
        return csv_files
    
    @staticmethod
    def validate_file_path(file_path: Path) -> bool:
        """
        Validate that a file path exists and is readable.
        
        Args:
            file_path: Path to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False
        
        if not file_path.is_file():
            logger.error(f"Path is not a file: {file_path}")
            return False
        
        if not os.access(file_path, os.R_OK):
            logger.error(f"File is not readable: {file_path}")
            return False
        
        return True
    
    @staticmethod
    def ensure_directory_exists(directory: Path) -> None:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            directory: Path to directory
        """
        try:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Ensured directory exists: {directory}")
        except Exception as e:
            logger.error(f"Failed to create directory {directory}: {e}")
            raise e

