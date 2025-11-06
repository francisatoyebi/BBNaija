#!/usr/bin/env python3
"""
BBNaija Sentiment Analysis - Main Entry Point

This script performs sentiment analysis on BBNaija tweets to predict
which housemate is most likely to be evicted based on viewer sentiment.

Usage:
    python main.py [--data-path PATH] [--output-path PATH] [--no-display]

Example:
    python main.py --data-path Scraped_tweets/ --output-path Scraped_tweets/
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.services.analysis_coordinator import BBNaijaAnalysisCoordinator


def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging for the application.
    
    Args:
        verbose: Enable verbose logging (DEBUG level)
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='BBNaija Sentiment Analysis - Predict evictions based on tweet sentiment',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--data-path',
        type=str,
        default=None,
        help='Path to directory containing tweet CSV files (default: Scraped_tweets/)'
    )
    
    parser.add_argument(
        '--output-path',
        type=str,
        default=None,
        help='Path to save output charts (default: Analysis_results/)'
    )
    
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Do not display results summary'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def main():
    """
    Main entry point for the application.
    """
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    try:
        # Print banner
        print("\n" + "=" * 60)
        print("BBNaija Sentiment Analysis System")
        print("=" * 60 + "\n")
        
        # Create configuration
        config = Config(
            data_path=args.data_path,
            output_path=args.output_path
        )
        
        logger.info(f"Data path: {config.data_path}")
        logger.info(f"Output path: {config.output_path}")
        
        # Download NLTK data if needed
        logger.info("Ensuring NLTK data is available...")
        import nltk
        try:
            nltk.data.find('vader_lexicon')
            logger.info("VADER lexicon found")
        except LookupError:
            logger.info("Downloading VADER lexicon...")
            nltk.download('vader_lexicon', quiet=True)
            logger.info("VADER lexicon downloaded")
        
        try:
            nltk.data.find('punkt')
            logger.info("Punkt tokenizer found")
        except LookupError:
            logger.info("Downloading Punkt tokenizer...")
            nltk.download('punkt', quiet=True)
            logger.info("Punkt tokenizer downloaded")
        
        # Create coordinator
        coordinator = BBNaijaAnalysisCoordinator(config=config)
        
        # Run analysis
        logger.info("Starting analysis...")
        result = coordinator.run_analysis(display_summary=not args.no_display)
        
        # Display eviction prediction
        if not args.no_display:
            eviction_prediction = coordinator.get_eviction_prediction(result)
            
            print("\n" + "🔮 " * 20)
            print(f"PREDICTION: {eviction_prediction[0]} is most likely to be evicted!")
            print(f"Confidence: {eviction_prediction[1]:.2f}% rating")
            print("🔮 " * 20 + "\n")
        
        logger.info("Analysis completed successfully!")
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\n❌ Error: {e}")
        print("Please ensure the data path exists and contains CSV files.\n")
        return 1
        
    except ValueError as e:
        logger.error(f"Value error: {e}")
        print(f"\n❌ Error: {e}\n")
        return 1
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Unexpected error occurred: {e}")
        print("Please check the logs for more details.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

