# coding: utf-8
# scrape the Nasa Mars News Site and collect the latest News Title and Paragraph Text
from bs4.element import AttributeValueWithCharsetSubstitution
import pymongo
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
from IPython.display import display




# -------------------- SCRAPING ---------------------------

# NASA Mars News
def nasa_mars_news():
    """
    Returns a list of news dictionaries
    """
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # setup splinter
    executable_path = {'executable_path': GeckoDriverManager().install()}
    # headless = True 
    browser = Browser('firefox', **executable_path, headless=True)

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # list of dictionaries of news
    news_list = []

    results = soup.find_all('div', class_='slide')

    for res in results:
        try:
            title = res.find('div', class_='content_title').text.strip()
            text = res.find('div', class_='rollover_description_inner').text.strip()
            
            news = {
                "title": title,
                "text": text
            }
            news_list.append(news)

        except AttributeError as err:
            print(err)

        browser.links.find_by_partial_text('Next')

    browser.quit()
    return news_list


# JPL Mars Space Images - Featured Image
def mars_space_featured_image():
    """
    Returns the link of Mars' feature image
    """
    url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    executable_path = {'executable_path': GeckoDriverManager().install()}

    browser = Browser('firefox', **executable_path, headless=True)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    featured_image_url = ""

    # ictures = soup.find_all('a', class_='fancybox-thumbs')
    picture = soup.find_all('img', class_='headerimage fade-in')


    for a in picture:
        # print(a.text) # FULL IMAGE
        pic_url = a['src']
        # print(pic_url)
        featured_image_url = url.replace('index.html', pic_url)

    print(featured_image_url)

    browser.quit()
    return featured_image_url


# Mars Facts
def mars_facts():
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    display(tables)

    df = tables[0]
    display(df.head())
    df.columns = ["Fact","Value"]
    df = df.set_index(["Fact"])
    html_table = df.to_html()
    html_table = html_table.replace("\n", "")
    # df.columns = df.columns.get_level_values(0)
    # display(df.columns)

    # html_table = df.to_html()
    # html_table = html_table.replace('\n', '')
    # print(html_table)
    return html_table

# Mars Hemispheres

def mars_hemispheres():
    """
    * obtain high resolution images for each of Mar’s hemispheres.
    * click each of the links to the hemispheres in order to find the image url to the full resolution image
    Returns a list of dictionaries:
    
    Example:
        hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "..."},
        {"title": "Cerberus Hemisphere", "img_url": "..."},
        {"title": "Schiaparelli Hemisphere", "img_url": "..."},
        {"title": "Syrtis Major Hemisphere", "img_url": "..."},
        ]
    """
    # main url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # images urls
    cerberus_hem_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    # https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg
    # /cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg
    schiaparelli_hem_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    syrtis_major_hem_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    valles_marineris_hem_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    
    url_list = [cerberus_hem_url,
                schiaparelli_hem_url,
                syrtis_major_hem_url,
                valles_marineris_hem_url]

    result_urls = []
    titles = []
    urls = []

    # find the descriptions first from the main url
    img_descriptions = requests.get(url)
    main_soup = BeautifulSoup(img_descriptions.text, 'html.parser')
    desc_results = main_soup.find_all('a', class_='itemLink product-item')

    executable_path = {'executable_path': GeckoDriverManager().install()}
    # headless = True 
    browser = Browser('firefox', **executable_path, headless=True)

    for desc in desc_results:
        try:
            alt = desc.find('img')
            desc = alt['alt'].strip('thumbnail')
            titles.append(desc)
        except AttributeError as err:
            print(err)

    # get the images urls
    for url in url_list:
        # response = requests.get(url)
        browser.visit(url)
        response = browser.html

        soup = BeautifulSoup(response, 'html.parser')
        results = soup.find_all('div', class_='wide-image-wrapper')

        for res in results:
            link = res.find('ul').a['href']
            print(link)
            urls.append(link)
    browser.quit()

    # place them in a list as dictionaries
    for title, url in zip(titles, urls):
        item = {"title": title, "img_url": url}
        result_urls.append(item)


    return result_urls

def scrape():
    mars_collection = {
        "nasa_news": nasa_mars_news(),
        "mars_space_img": mars_space_featured_image(),
        "mars_facts": mars_facts(),
        "mars_hemispheres": mars_hemispheres()
    }
    return mars_collection




# ------------------ Step 2 - MongoDB and Flask Application -------------------------

if __name__ in "__main__":
    # b res = nasa_mars_news()
    # print(res)
    # res = mars_space_featured_image()
    # print(res)
    # res = mars_facts()
    # print(res)
    res = mars_hemispheres()
    print(res)
    # print(res)
    # scrape()


