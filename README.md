# BBNaija Sentiment Analysis System

A professional sentiment analysis system for predicting Big Brother Nigeria evictions based on viewer tweets using VADER sentiment analysis.

## 🎯 Overview

This project analyzes tweets about BBNaija housemates to predict which housemate is most likely to be evicted based on viewer sentiment. The system is built following **SOLID principles** with a modular, maintainable architecture.

## ✨ Features

- **Sentiment Analysis**: Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) for social media text analysis
- **Data Visualization**: Generates pie charts and bar charts showing ratings
- **Eviction Prediction**: Predicts most likely housemate to be evicted based on sentiment
- **Modular Architecture**: Clean separation of concerns following SOLID principles
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Error Handling**: Robust error handling throughout the system
- **Type Hints**: Full type annotations for better code quality

## 🏗️ Architecture

The project follows SOLID principles with a clean modular structure:

```
BBNaija/
├── src/
│   ├── models/          # Data models
│   │   └── tweet_data.py
│   ├── data/            # Data loading and cleaning
│   │   ├── data_loader.py
│   │   └── data_cleaner.py
│   ├── analysis/        # Sentiment analysis and rating calculation
│   │   ├── sentiment_analyzer.py
│   │   └── rating_calculator.py
│   ├── visualization/   # Chart creation
│   │   └── chart_visualizer.py
│   ├── services/        # Workflow coordination
│   │   └── analysis_coordinator.py
│   ├── utils/           # Utility functions
│   │   └── file_utils.py
│   └── config.py        # Configuration management
├── Scrapers/            # Tweet scraping scripts
├── Scraped_tweets/      # CSV files with tweet data
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/francisatoyebi/BBNaija.git
cd BBNaija
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data (if not done automatically):**
```python
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
```

## 📝 Sample Data

The repository includes **sample scraped tweet data** in the `Scraped_tweets/` directory for immediate testing:

- **Laycon.csv** - 40 tweets (75% positive sentiment)
- **Dorathy.csv** - 40 tweets (65% positive sentiment)
- **Ozo.csv** - 40 tweets (50% positive sentiment)
- **Nengi.csv** - 40 tweets (60% positive sentiment)
- **Kiddwaya.csv** - 40 tweets (40% positive sentiment)

You can run the analysis immediately with these sample files without needing to scrape your own data!

> 📖 **For more details** about the sample data, see [`Scraped_tweets/README.md`](Scraped_tweets/README.md)

### Regenerating Sample Data

If you need to regenerate the sample data:

```bash
python3 generate_sample_data.py
```

## 🚀 Usage

### Basic Usage

Run the analysis with default settings (uses sample data):

```bash
python main.py
```

### Custom Paths

Specify custom data and output paths:

```bash
python main.py --data-path /path/to/tweets/ --output-path /path/to/output/
```

### Command-Line Options

```bash
python main.py --help
```

Options:
- `--data-path PATH`: Path to directory containing tweet CSV files
- `--output-path PATH`: Path to save output charts
- `--no-display`: Don't display results summary
- `--verbose` or `-v`: Enable verbose logging

### Example

```bash
python main.py --data-path Scraped_tweets/ --output-path results/ --verbose
```

## 📊 Data Format

Tweet CSV files should contain the following columns:
- `date`: Tweet date/timestamp
- `tweet`: Tweet text content
- `urls`: Associated URLs

Example:
```csv
date,tweet,urls
2023-01-01,I love this housemate!,[https://twitter.com/...]
2023-01-01,Not a fan of this person,[https://twitter.com/...]
```

## 🔧 Configuration

The system can be configured via the `Config` class in `src/config.py`:

- Chart DPI (resolution)
- Chart sizes and styling
- Required CSV columns
- File paths

## 📈 Output

The system generates:

1. **Pie Chart**: Donut chart showing percentage ratings (`bbnaija_pie.png`)
2. **Bar Chart**: Bar chart comparing housemate ratings (`bbnaija_bar.png`)
3. **Console Summary**: Detailed text summary with statistics
4. **Eviction Prediction**: Prediction of most likely evicted housemate

## 🧪 Testing

Run tests (if implemented):

```bash
pytest tests/ -v --cov=src
```

## 👤 Author

**Francis Atoyebi**

## 🙏 Acknowledgments

- NLTK for VADER sentiment analysis
- BBNaija community for inspiration
- All contributors to this project

## 📚 References

- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Clean Code in Python](https://realpython.com/python-clean-code/)

---

**Note**: This is a fun educational project for sentiment analysis. Predictions are based on tweet sentiment and may not reflect actual eviction results.
