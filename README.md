# Crypto Sentiment Analyzer

A web application that performs sentiment analysis on cryptocurrency-related news and forums. This project allows users to select a cryptocurrency (e.g., Bitcoin, Ethereum) and a news site (e.g., BBC, Telegraph) to analyze the sentiments of articles and comments related to that cryptocurrency. The results are displayed in a pie chart showing positive, negative, and neutral sentiments.

## Features

- Scrape and analyze cryptocurrency news headlines and forum discussions.
- Perform sentiment analysis (positive, negative, neutral) using TextBlob.
- Visualize the sentiment distribution using a pie chart.
- Supports multiple cryptocurrencies (Bitcoin, Ethereum) and sites (BBC, Telegraph).
- Easy-to-use web interface with dropdowns for selecting cryptocurrency and news site.

## Technologies Used

- **Python**: Backend logic and web scraping (requests, BeautifulSoup).
- **Flask**: Web framework for building the app.
- **TextBlob**: Sentiment analysis tool.
- **Bootstrap**: Frontend framework for responsive UI design.
- **Chart.js**: JavaScript library for rendering the sentiment analysis pie chart.


## Setup and Installation

### Prerequisites

Make sure you have the following installed on your system:

- **Python 3.7+**
- **Flask**
- **requests**
- **BeautifulSoup**
- **TextBlob**
- **Chart.js**

### Installation Steps

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/Crypto-Sentiment-Analyzer.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd CryptoSentimentAnalyzer
    ```

3. **Set up a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate   # For Windows: venv\Scripts\activate
    ```

4. **Install required packages**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Flask app**:

    ```bash
    python app.py
    ```

6. **Access the application** by opening a web browser and going to:

    ```
    http://127.0.0.1:5000/
    ```

## Usage

1. Select a cryptocurrency (Bitcoin or Ethereum) from the dropdown menu.
2. Select a news site (BBC or Telegraph) from the dropdown menu.
3. Click the "Start Analysis" button.
4. The app will display the sentiment analysis results in a pie chart.
5. Click "Show Comments" to view the individual comments and their associated sentiments.

