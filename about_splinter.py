from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup
# from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def scrape_qoutes_use_splinter():
    # setup splinter
    executable_path = {'executable_path': GeckoDriverManager().install()}
    # headless = True 
    browser = Browser('firefox', **executable_path, headless=True)

    url = "http://quotes.toscrape.com"
    browser.visit(url)

    for x in range(1, 6):
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        quotes = soup.find_all('span', class_='text')

        for q in quotes:
            print(q.text)

        browser.links.find_by_partial_text('Next')

    browser.quit()


def scrape_qoutes_use_selenium():
    opts = webdriver.FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=opts, executable_path=GeckoDriverManager().install())

    url = "http://quotes.toscrape.com"
    # browser.visit(url)

    for x in range(1, 6):
        driver.get(url)
        html = driver.page_source
        
        soup = BeautifulSoup(html, 'html.parser')

        quotes = soup.find_all('span', class_='text')

        for q in quotes:
            print(q.text)

    driver.quit()

if __name__ in "__main__":
    # scrape_qoutes_use_Browser()
    scrape_qoutes_use_Driver()