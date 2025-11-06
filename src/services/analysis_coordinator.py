"""
Analysis coordination service.

This module orchestrates the entire analysis workflow following the
Single Responsibility Principle and Dependency Inversion Principle.
"""

import logging
from typing import Optional

from ..config import Config
from ..data.data_loader import TweetDataLoader
from ..data.data_cleaner import TweetDataCleaner
from ..analysis.sentiment_analyzer import SentimentAnalyzer
from ..analysis.rating_calculator import RatingCalculator
from ..visualization.chart_visualizer import ChartVisualizer
from ..models.tweet_data import AnalysisResult

logger = logging.getLogger(__name__)


class BBNaijaAnalysisCoordinator:
    """
    Coordinates the entire BBNaija sentiment analysis workflow.
    
    This class follows the Dependency Inversion Principle by depending
    on abstractions (injected dependencies) rather than concrete implementations.
    It orchestrates the workflow without handling the details of each step.
    """
    
    def __init__(
        self,
        config: Optional[Config] = None,
        data_loader: Optional[TweetDataLoader] = None,
        data_cleaner: Optional[TweetDataCleaner] = None,
        sentiment_analyzer: Optional[SentimentAnalyzer] = None,
        rating_calculator: Optional[RatingCalculator] = None,
        chart_visualizer: Optional[ChartVisualizer] = None
    ):
        """
        Initialize the coordinator with dependencies.
        
        Args:
            config: Configuration object (creates default if None)
            data_loader: Data loader instance (creates if None)
            data_cleaner: Data cleaner instance (creates if None)
            sentiment_analyzer: Sentiment analyzer instance (creates if None)
            rating_calculator: Rating calculator instance (creates if None)
            chart_visualizer: Chart visualizer instance (creates if None)
        """
        # Use provided config or create default
        self.config = config if config else Config()
        
        # Inject dependencies or create defaults
        self.data_loader = data_loader if data_loader else TweetDataLoader(self.config)
        self.data_cleaner = data_cleaner if data_cleaner else TweetDataCleaner(self.config)
        self.sentiment_analyzer = sentiment_analyzer if sentiment_analyzer else SentimentAnalyzer()
        self.rating_calculator = rating_calculator if rating_calculator else RatingCalculator()
        self.chart_visualizer = chart_visualizer if chart_visualizer else ChartVisualizer(self.config)
        
        logger.info("Initialized BBNaija Analysis Coordinator")
    
    def run_analysis(self, display_summary: bool = True) -> AnalysisResult:
        """
        Execute the complete analysis workflow.
        
        Workflow steps:
        1. Validate configuration
        2. Load tweet data from CSV files
        3. Clean and preprocess data
        4. Perform sentiment analysis
        5. Calculate ratings
        6. Generate visualizations
        7. Display results summary
        
        Args:
            display_summary: Whether to display text summary (default: True)
            
        Returns:
            AnalysisResult object containing all results
            
        Raises:
            Exception: If any step in the workflow fails
        """
        logger.info("Starting BBNaija sentiment analysis workflow")
        
        try:
            # Step 1: Validate configuration
            logger.info("Step 1: Validating configuration")
            self.config.validate_paths()
            
            # Step 2: Load data
            logger.info("Step 2: Loading tweet data")
            tweet_data_list = self.data_loader.load_all_tweets()
            logger.info(f"Loaded data for {len(tweet_data_list)} housemate(s)")
            
            # Step 3: Clean data
            logger.info("Step 3: Cleaning data")
            cleaned_data = self.data_cleaner.clean_all_tweet_data(tweet_data_list)
            logger.info(f"Cleaned data for {len(cleaned_data)} housemate(s)")
            
            # Step 4: Analyze sentiment
            logger.info("Step 4: Performing sentiment analysis")
            analyzed_data = self._analyze_sentiment(cleaned_data)
            logger.info(f"Analyzed sentiment for {len(analyzed_data)} housemate(s)")
            
            # Step 5: Calculate ratings
            logger.info("Step 5: Calculating ratings")
            result = self.rating_calculator.calculate_all_ratings(analyzed_data)
            logger.info("Ratings calculated successfully")
            
            # Step 6: Generate visualizations
            logger.info("Step 6: Generating visualizations")
            self.chart_visualizer.create_all_charts(result)
            logger.info("Visualizations created successfully")
            
            # Step 7: Display summary
            if display_summary:
                logger.info("Step 7: Displaying results summary")
                self.chart_visualizer.display_results_summary(result)
            
            logger.info("Analysis workflow completed successfully")
            
            return result
            
        except Exception as e:
            logger.error(f"Analysis workflow failed: {e}")
            raise e
    
    def _analyze_sentiment(self, cleaned_data):
        """
        Analyze sentiment for all cleaned data.
        
        Args:
            cleaned_data: List of tuples (housemate_name, cleaned_dataframe)
            
        Returns:
            List of tuples (housemate_name, dataframe_with_sentiment)
        """
        analyzed_data = []
        
        for housemate_name, df in cleaned_data:
            try:
                # Perform sentiment analysis
                df_with_sentiment = self.sentiment_analyzer.analyze_dataframe(df)
                analyzed_data.append((housemate_name, df_with_sentiment))
                
                # Get statistics
                stats = self.sentiment_analyzer.get_sentiment_statistics(df_with_sentiment)
                
                logger.info(
                    f"Sentiment for {housemate_name}: "
                    f"mean={stats['mean']:.4f}, "
                    f"pos={stats['positive_ratio']:.1%}, "
                    f"neg={stats['negative_ratio']:.1%}"
                )
                
            except Exception as e:
                logger.error(f"Failed to analyze sentiment for {housemate_name}: {e}")
                continue
        
        return analyzed_data
    
    def get_eviction_prediction(self, result: AnalysisResult) -> tuple:
        """
        Get eviction prediction from analysis results.
        
        Args:
            result: AnalysisResult object
            
        Returns:
            Tuple of (housemate_name, rating)
        """
        return self.rating_calculator.get_eviction_prediction(result)

