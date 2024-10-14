from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob
import logging

app = Flask(__name__)

# Loglama yapılandırması
logging.basicConfig(level=logging.DEBUG)

# URL'leri dinamik olarak oluşturmak için sabitler
URLS = {
    'telegraph': {
        'bitcoin': 'https://www.telegraph.co.uk/bitcoin',
        'ethereum': 'https://www.telegraph.co.uk/ethereum'
    },
    'bbc': {
        'bitcoin': 'https://www.bbc.com/news/topics/c734j90em14t',
        'ethereum': 'https://www.bbc.com/news/topics/c734j90em14t'
    },
    'cointelegraph': {
        'bitcoin': 'https://cointelegraph.com/tags/bitcoin',
        'ethereum': 'https://cointelegraph.com/tags/ethereum'
    }
}

# Selenium ayarları
chrome_options = Options()
chrome_options.add_argument("--headless")  # Headless modda çalıştırma

@app.route('/', methods=['GET', 'POST'])
def index():
    total_comments = 0
    positive_comments = 0
    negative_comments = 0
    neutral_comments = 0
    results = []

    if request.method == 'POST':
        crypto = request.form.get('crypto')
        site = request.form.get('site')

        if not crypto or not site:
            logging.error("Site veya kripto para seçilmedi.")
            return "Please select both the site and cryptocurrency.", 400

        try:
            url = URLS[site][crypto]
            logging.info(f"Seçilen URL: {url}")
        except KeyError as e:
            logging.error(f"KeyError: {str(e)} - Site: {site}, Crypto: {crypto}")
            return "Invalid site or cryptocurrency selection.", 400

        try:
            # WebDriver'ı başlat
            logging.info("Chrome WebDriver başlatılıyor.")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            logging.info(f"{url} sayfası yükleniyor...")

            # Telegraph için scraping işlemi
            if site == 'telegraph':
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-headline__text')))
                articles = driver.find_elements(By.CLASS_NAME, 'list-headline__link')
                for article in articles:
                    title = article.find_element(By.CLASS_NAME, 'list-headline__text').text
                    logging.debug(f"Başlık bulundu: {title}")
                    if title:
                        results.append({'headline': title})

            # BBC için scraping işlemi
            elif site == 'bbc':
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sc-ae29827d-6')))
                articles = driver.find_elements(By.CLASS_NAME, 'sc-ae29827d-6')
                for article in articles:
                    title = article.find_element(By.CLASS_NAME, 'sc-1207bea1-3').text
                    logging.debug(f"Başlık bulundu: {title}")
                    if title:
                        results.append({'headline': title})

            # Cointelegraph için scraping işlemi
            elif site == 'cointelegraph':
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-card-inline__title-link')))
                articles = driver.find_elements(By.CLASS_NAME, 'post-card-inline__content')
                for article in articles:
                    title = article.find_element(By.CLASS_NAME, 'post-card-inline__title-link').text
                    logging.debug(f"Başlık bulundu: {title}")
                    if title:
                        results.append({'headline': title})

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
            logging.error(f"Bir hata oluştu: {str(e)}")
            return "An error occurred", 500
        finally:
            driver.quit()

    return render_template('index.html', results=results, total_comments=total_comments,
                           positive_comments=positive_comments, negative_comments=negative_comments,
                           neutral_comments=neutral_comments)

if __name__ == '__main__':
    app.run(debug=True)
