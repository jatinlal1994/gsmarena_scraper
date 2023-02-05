"""Module to fetch news from multiple pages of GSMArena simultaneously"""
from threading import Thread, Semaphore
from requests import get
from lxml import html

NUMBER_OF_PAGES = 1
s = Semaphore(5)

def parse_page(page_no: int, news_titles: list) -> None:
    """Parse news page present at below URL"""
    s.acquire()
    content = get(f"https://www.gsmarena.com/news.php3?iPage={page_no}", timeout=5).text
    data = html.fromstring(content)
    news_list = zip(
        [title.text_content() for title in data.cssselect("#news .floating-title h3")], # Title of news elements
        [description.text_content() for description in data.cssselect(".floating-title .news-item p")], # Short description of news elements
        [image.get("src") for image in data.cssselect(".news-item-media-wrap img")], # Images of news elements
        [link.get("src") for link in data.cssselect(".news-item-media-wrap a")], # Links present in news elements
        [published_on.text_content() for published_on in data.cssselect(".meta-line .meta-item-time")], # Date of publication of news
    )
    s.release()
    news_titles.extend([{
        "title": news[0],
        "description": news[1],
        "image": news[2],
        "link": news[3],
        "published_on": news[4]
    } for news in news_list])

def parse_gsmarena_news() -> list:
    """Run multiple threads to get new simultaneously"""
    threads = [None] * (NUMBER_OF_PAGES + 1)
    news_titles = []

    for page_no in range(1, NUMBER_OF_PAGES+1):
        threads[page_no] = Thread(target=parse_page, args=[page_no, news_titles])
        threads[page_no].start()

    for page_no in range(1, NUMBER_OF_PAGES+1):
        threads[page_no].join()

    return news_titles
