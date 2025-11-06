#!/usr/bin/env python3
"""
Sample Tweet Data Generator for BBNaija Sentiment Analysis

This script generates sample tweet CSV files for demonstration and testing
purposes following SOLID principles.
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple


class TweetTemplate:
    """
    Manages tweet templates for different sentiment categories.
    Single Responsibility: Template management only.
    """
    
    POSITIVE_TEMPLATES = [
        "I'm voting for {name}! They deserve to win! #BBNaija #Vote{name}",
        "{name} is the best housemate this season! Love them so much! 💕 #BBNaija",
        "Can't stop watching {name}! Such amazing energy! #BBNaija #Team{name}",
        "{name} just showed why they're a winner! 🔥 #BBNaija",
        "Nobody can beat {name}! They're playing the game perfectly! #BBNaija",
        "{name} is so genuine and authentic! We love you! #BBNaija #Vote{name}",
        "Team {name} all the way! Let's get them to the finals! 💪 #BBNaija",
        "{name} has the best strategy in the house! #BBNaija #Winner",
        "I'm so proud of {name}! They've grown so much! #BBNaija #Team{name}",
        "{name} is bringing the entertainment we need! Love it! #BBNaija",
        "Give {name} the grand prize already! They earned it! 👑 #BBNaija",
        "{name} is the most deserving housemate! No cap! #BBNaija #Vote{name}",
        "Everyone should vote for {name}! They're the real deal! #BBNaija",
        "{name} has my full support! Let's do this! 💯 #BBNaija #Team{name}",
        "The way {name} handled that situation was perfect! #BBNaija",
    ]
    
    NEGATIVE_TEMPLATES = [
        "I don't understand why {name} is still in the house #BBNaija",
        "{name} is not playing the game well at all #BBNaija",
        "{name} needs to step up their game or leave #BBNaija",
        "Not impressed with {name}'s behavior today #BBNaija",
        "{name} is being too fake for my liking #BBNaija",
        "I think {name} should be evicted this week #BBNaija",
        "{name} is not bringing anything to the show #BBNaija",
        "Why is {name} acting like this? So disappointing #BBNaija",
        "{name} is playing a weak game #BBNaija",
        "I'm not feeling {name} anymore #BBNaija",
        "{name} made a terrible decision today #BBNaija",
        "Can't relate to {name}'s strategy at all #BBNaija",
        "{name} is losing my vote with this attitude #BBNaija",
        "Not sure {name} deserves to be in the finals #BBNaija",
    ]
    
    NEUTRAL_TEMPLATES = [
        "{name} is competing in today's challenge #BBNaija",
        "Watching {name} on tonight's episode #BBNaija",
        "{name} had a conversation with another housemate #BBNaija",
        "Interesting to see how {name} approaches the game #BBNaija",
        "{name} is nominated this week #BBNaija",
        "Let's see what {name} does next #BBNaija",
        "{name} is in the diary room #BBNaija",
        "Curious about {name}'s next move #BBNaija",
        "{name} participated in tonight's task #BBNaija",
        "Following {name}'s journey in the house #BBNaija",
    ]
    
    @classmethod
    def get_templates_by_sentiment(cls, sentiment: str) -> List[str]:
        """
        Get tweet templates for a specific sentiment.
        
        Args:
            sentiment: 'positive', 'negative', or 'neutral'
            
        Returns:
            List of template strings
        """
        if sentiment == 'positive':
            return cls.POSITIVE_TEMPLATES
        elif sentiment == 'negative':
            return cls.NEGATIVE_TEMPLATES
        else:
            return cls.NEUTRAL_TEMPLATES


class SentimentDistributor:
    """
    Determines sentiment distribution for each housemate.
    Single Responsibility: Sentiment ratio management.
    """
    
    @staticmethod
    def get_distribution(housemate: str) -> Dict[str, float]:
        """
        Get sentiment distribution for a housemate.
        
        Args:
            housemate: Name of the housemate
            
        Returns:
            Dictionary with sentiment ratios
        """
        distributions = {
            'Laycon': {'positive': 0.75, 'neutral': 0.15, 'negative': 0.10},
            'Dorathy': {'positive': 0.65, 'neutral': 0.20, 'negative': 0.15},
            'Ozo': {'positive': 0.50, 'neutral': 0.25, 'negative': 0.25},
            'Nengi': {'positive': 0.60, 'neutral': 0.20, 'negative': 0.20},
            'Kiddwaya': {'positive': 0.40, 'neutral': 0.25, 'negative': 0.35},
        }
        return distributions.get(housemate, {'positive': 0.5, 'neutral': 0.3, 'negative': 0.2})


class TweetGenerator:
    """
    Generates individual tweets with proper formatting.
    Single Responsibility: Tweet creation.
    """
    
    def __init__(self):
        self.tweet_template = TweetTemplate()
        self.base_date = datetime(2024, 11, 1)
    
    def generate_tweet(self, housemate: str, sentiment: str, index: int) -> Tuple[str, str, str]:
        """
        Generate a single tweet.
        
        Args:
            housemate: Name of the housemate
            sentiment: Sentiment type (positive/negative/neutral)
            index: Tweet index for URL generation
            
        Returns:
            Tuple of (date, tweet_text, url)
        """
        # Get template
        templates = self.tweet_template.get_templates_by_sentiment(sentiment)
        template = random.choice(templates)
        tweet_text = template.format(name=housemate)
        
        # Generate date (spread over 5 days)
        days_offset = random.randint(0, 5)
        hours_offset = random.randint(0, 23)
        tweet_date = self.base_date + timedelta(days=days_offset, hours=hours_offset)
        date_str = tweet_date.strftime('%Y-%m-%d %H:%M:%S')
        
        # Generate URL
        tweet_id = 1234567890123456789 + index + random.randint(1000, 9999)
        url = f"https://twitter.com/user{index}/status/{tweet_id}"
        
        return date_str, tweet_text, url


class CSVWriter:
    """
    Handles CSV file writing operations.
    Single Responsibility: File I/O operations.
    """
    
    @staticmethod
    def write_csv(filepath: Path, tweets: List[Tuple[str, str, str]]) -> None:
        """
        Write tweets to CSV file.
        
        Args:
            filepath: Path to output file
            tweets: List of (date, tweet, url) tuples
        """
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['date', 'tweet', 'urls'])
            writer.writerows(tweets)


class SampleDataCoordinator:
    """
    Coordinates the sample data generation process.
    Single Responsibility: Orchestration of data generation workflow.
    """
    
    def __init__(self, output_dir: str = 'Scraped_tweets', tweets_per_housemate: int = 40):
        """
        Initialize the coordinator.
        
        Args:
            output_dir: Directory to save CSV files
            tweets_per_housemate: Number of tweets to generate per housemate
        """
        self.output_dir = Path(output_dir)
        self.tweets_per_housemate = tweets_per_housemate
        self.tweet_generator = TweetGenerator()
        self.csv_writer = CSVWriter()
        self.sentiment_distributor = SentimentDistributor()
        
    def generate_all_samples(self) -> None:
        """
        Generate sample data for all housemates.
        """
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        housemates = ['Laycon', 'Dorathy', 'Ozo', 'Nengi', 'Kiddwaya']
        
        print("=" * 60)
        print("Generating Sample BBNaija Tweet Data")
        print("=" * 60)
        
        for housemate in housemates:
            self._generate_housemate_data(housemate)
        
        print("\n" + "=" * 60)
        print("Sample data generation completed successfully!")
        print(f"Files saved to: {self.output_dir.absolute()}")
        print("=" * 60)
    
    def _generate_housemate_data(self, housemate: str) -> None:
        """
        Generate tweet data for a single housemate.
        
        Args:
            housemate: Name of the housemate
        """
        print(f"\nGenerating tweets for {housemate}...")
        
        # Get sentiment distribution
        distribution = self.sentiment_distributor.get_distribution(housemate)
        
        # Calculate tweet counts per sentiment
        positive_count = int(self.tweets_per_housemate * distribution['positive'])
        negative_count = int(self.tweets_per_housemate * distribution['negative'])
        neutral_count = self.tweets_per_housemate - positive_count - negative_count
        
        print(f"  Positive: {positive_count}, Neutral: {neutral_count}, Negative: {negative_count}")
        
        # Generate tweets
        tweets = []
        index = 0
        
        # Generate positive tweets
        for _ in range(positive_count):
            tweets.append(self.tweet_generator.generate_tweet(housemate, 'positive', index))
            index += 1
        
        # Generate negative tweets
        for _ in range(negative_count):
            tweets.append(self.tweet_generator.generate_tweet(housemate, 'negative', index))
            index += 1
        
        # Generate neutral tweets
        for _ in range(neutral_count):
            tweets.append(self.tweet_generator.generate_tweet(housemate, 'neutral', index))
            index += 1
        
        # Shuffle to mix sentiments
        random.shuffle(tweets)
        
        # Write to CSV
        filepath = self.output_dir / f"{housemate}.csv"
        self.csv_writer.write_csv(filepath, tweets)
        
        print(f"  ✓ Generated {len(tweets)} tweets -> {filepath}")


def main():
    """
    Main entry point for sample data generation.
    """
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create coordinator and generate samples
    coordinator = SampleDataCoordinator(
        output_dir='Scraped_tweets',
        tweets_per_housemate=40
    )
    
    coordinator.generate_all_samples()


if __name__ == "__main__":
    main()

