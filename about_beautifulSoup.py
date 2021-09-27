from bs4 import BeautifulSoup as bs
import requests


def basic_bs():
    # an html string
    html_string = """
    <html>
    <head>
    <title>
    A simple HTML Document
    </title>
    <body>
    <p>This is a very simple html document</p>
    <p>It has two tiny paragraphs</p>
    </body>
    </html>
    """

    # create the object
    soup = bs(html_string, "html.parser")

    # the type() method will return the type of

    # the prettyfy() method will return things in a more pretty way (just like in mongo pretty)

    type(soup)
    print(soup.prettify())


    # now we can extract things
    print(soup.title)

    print(soup.title.text)

    print(soup.title.text.strip())


    # same with body:
    print(soup.body)
    print(soup.body.text)
    print(soup.body.p.text)


    # find stuff with BeautifulSoup
    print(soup.body.find_all('p'))
    print(soup.body.find_all('p')[0])
    print(soup.body.find_all('p')[1])


def using_requests():
    # using requests
    import requests

    url = "https://cristinasewell.github.io/html_and_css/index.html"
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    # print(soup.prettify())

    # results are returned as an iterable list
    results = soup.find_all('head')

    for res in results:
        try:
            title = res.find("title").text
            print(title)
        
        except AttributeError as err:
            print(err)


def using_lxml_parser():
    """
    Before using this we should create the db in mongo and the colelction?
    """

    import pymongo
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    # define the database collection
    db = client.craigslist_db

    # url of the pages that we will scrape
    url = "https://newjersey.craigslist.org/search/sss?sort=rel&query=guitar"
    response = requests.get(url)

    # create a BeautifulSoup object with lxml parser
    soup = bs(response.text, 'lxml')

    results = soup.find_all('li', class_='result-row')

    for res in results:
        try:
            title = res.find('a', class_='result-title').text
            price = res.a.span.text
            link = res.a['href']

            if (title and price and link):
                post = {
                    'title': title,
                    'price': price,
                    'url': link
                }
                db.item.insert_one(post)
        except AttributeError as err:
            print(err)


if __name__ in "__main__":
   #  basic_bs()
   #  using_requests()
    using_lxml_parser()