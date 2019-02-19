import threading
from queue import Queue
from spider import Spider
from general import *

PROJECT_NAME = 'toto'
HOMEPAGE = 'http://www.singaporepools.com.sg/en/product/Pages/toto_results.aspx?'
DATA_FILE_NAME = PROJECT_NAME + '/toto.txt'
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
LINKS_FILE = PROJECT_NAME + '/querylinks.html'
NUMBER_OF_THREADS = 8
queue = Queue()

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    queued_links = generate_urls(PROJECT_NAME, HOMEPAGE, LINKS_FILE)
    Spider(PROJECT_NAME, HOMEPAGE, DATA_FILE_NAME)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        for link in queued_links:
            queue.put(link)
        queue.join()

create_workers()
create_jobs()
