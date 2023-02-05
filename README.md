# GSMArena Scraper
Scrape news elements from news explorer page from GSMArena.
* Supports multithreading for faster scraping of pages
* Returns a simple dictionary for easy integration with your project
* Uses semaphores to run only given # of requests at a time

```python
NUMBER_OF_PAGES = 1 # No of pages to be scraped
s = Semaphore(5) # No of concurrent requests to be sent
```
