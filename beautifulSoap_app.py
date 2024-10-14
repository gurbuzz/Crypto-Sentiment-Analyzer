from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import logging

app = Flask(__name__)

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO)

# URL'leri dinamik olarak oluşturmak için sabitler
URLS = {
    'telegraph': {
        'bitcoin': 'https://www.telegraph.co.uk/bitcoin',
        'ethereum': 'https://www.telegraph.co.uk/ethereum'
    },
    'bbc': {
        'bitcoin': 'https://www.bbc.com/news/topics/c734j90em14t',
        'ethereum': 'https://www.bbc.com/news/topics/c734j90em14t'  # Örnek URL, gerçek URL ile güncelle
    },
    'cointelegraph': {
        'bitcoin': 'https://cointelegraph.com/tags/bitcoin',
        'ethereum': 'https://cointelegraph.com/tags/ethereum'
    }
}

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize variables
    total_comments = 0
    positive_comments = 0
    negative_comments = 0
    neutral_comments = 0
    results = []

    if request.method == 'POST':
        # Formdan gelen seçimleri al
        crypto = request.form.get('crypto')
        site = request.form.get('site')

        # crypto veya site boş mu kontrol et
        if not crypto or not site:
            return "Please select both the site and cryptocurrency.", 400

        # Seçilen site ve kripto paraya göre URL oluştur
        try:
            url = URLS[site][crypto]
        except KeyError as e:
            logging.error(f"KeyError: {str(e)} - Site: {site}, Crypto: {crypto}")
            return "Invalid site or cryptocurrency selection.", 400

        # HTTP isteği için headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            'Referer': 'https://www.google.com/',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }

        try:
            # HTTP isteği
            response = requests.get(url, headers=headers)
            logging.info(f"Page status: {response.status_code}")
            if response.status_code != 200:
                logging.error(f"Page could not be loaded: {response.status_code}")
                return f"Page could not be loaded: {response.status_code}", 500

            # HTML içeriği parse etme
            soup = BeautifulSoup(response.content, 'html.parser')

            # Telegraph için scraping işlemi
            if site == 'telegraph':
                articles = soup.find_all('a', class_='list-headline__link')
                for article in articles:
                    title = article.find('span', class_='u-heading-6 list-headline__text')
                    if title:
                        results.append({'headline': title.text.strip()})

            # BBC için scraping işlemi
            elif site == 'bbc':
                articles = soup.find_all('div', class_='sc-ae29827d-6')
                for article in articles:
                    title = article.find('h2', class_='sc-1207bea1-3')
                    if title:
                        results.append({'headline': title.text.strip()})

            # Cointelegraph için scraping işlemi
            elif site == 'cointelegraph':
                articles = soup.find_all('div', class_='post-card-inline__content')
                for article in articles:
                    title = article.find('a', class_='post-card-inline__title-link')
                    if title:
                        results.append({'headline': title.text.strip()})

            # Duygu analizi ve sonuçları hesaplama
            total_comments = len(results)
            for result in results:
                analysis = TextBlob(result['headline'])
                sentiment = analysis.sentiment.polarity
                if sentiment > 0:
                    sentiment_label = 'Positive'
                    positive_comments += 1
                elif sentiment < 0:
                    sentiment_label = 'Negative'
                    negative_comments += 1
                else:
                    sentiment_label = 'Neutral'
                    neutral_comments += 1
                result['sentiment'] = sentiment_label

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return "An error occurred", 500

    # Render the template with results
    return render_template('index.html', results=results, total_comments=total_comments,
                           positive_comments=positive_comments, negative_comments=negative_comments,
                           neutral_comments=neutral_comments)

if __name__ == '__main__':
    app.run(debug=True)
