import atexit
import logging
import os
import lxml
from crawler import Crawler
from frontier import Frontier

if __name__ == "__main__":
    print("hello")
    # Configures basic logging
    logging.basicConfig(format='%(asctime)s (%(name)s) %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)

    # Instantiates frontier and loads the last state if exists
    frontier = Frontier()
    frontier.load_frontier()
    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    atexit.register(frontier.save_frontier)

    # Instantiates a crawler object and starts crawling
    crawler = Crawler(frontier)
    crawler.start_crawling()
    crawler.is_valid("https://google.com")
    print("goodbye")
