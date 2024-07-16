from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin
from newspaper import Article

def fetch_articles(url, keyword):
    options = Options()
    options.add_argument('--headless')  # Ensure headless mode is enabled
    options.add_argument('--disable-gpu')  # Required for headless mode in some environments
    options.add_argument('--ignore-certificate-errors')  # Ignore SSL errors
    # Path to the portable Slimjet executable
    options.binary_location = "C:/Users/natec/Desktop/news/Slimjet/slimjet.exe"
    # Path to the ChromeDriver executable
    service = Service(executable_path="C:/Users/natec/Desktop/news/chromedriver_win32/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = soup.find_all('a', href=True)
        articles = []
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)  # Ensure the URL is absolute
            if keyword in full_url and full_url not in articles:
                articles.append(full_url)
        return articles
    except Exception as e:
        print(f"Error fetching articles from {url}: {e}")
        return []
    finally:
        driver.quit()

def print_article_details(url):
    article = Article(url)
    try:
        article.download()
        article.parse()
        # Print only the article text, limiting to the first 500 characters
        print(f"Text: {article.text[:500]}...\n")
    except Exception as e:
        print(f"Error processing article {url}: {e}")

def main():
    parser = argparse.ArgumentParser(description="CLI NEWS")
    parser.add_argument('url', type=str, help="URL of the news site")
    parser.add_argument('keyword', type=str, help="Keyword to filter articles")
    args = parser.parse_args()

    articles = fetch_articles(args.url, args.keyword)
    print(f"Found {len(articles)} articles.\n")
    for idx, article_url in enumerate(articles[:5], start=1):  # Limit to 5 articles for brevity
        print(f"{idx}. {article_url}")
        print_article_details(article_url)

if __name__ == "__main__":
    main()
