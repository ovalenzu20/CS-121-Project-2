import logging
import re
from urllib.parse import urlparse
from corpus import Corpus
import lxml
<<<<<<< HEAD
import urllib.request
=======
import http.client
import os
import urllib.request


>>>>>>> c4432a8b40840d8c0736bd6103eebc75cc5e8ff6

logger = logging.getLogger(__name__)

class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier):
        self.frontier = frontier
        self.corpus = Corpus()

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        print(len(self.frontier))
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
#             self.is_valid(url)
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            
            url_data = self.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.corpus.get_file_name(next_link) is not None:
                    if self.is_valid(next_link):
                        self.frontier.add_url(next_link)

    def fetch_url(self, url):
        """
        This method, using the given url, should find the corresponding file in the corpus and return a dictionary
        containing the url, content of the file in binary format and the content size in bytes
        :param url: the url to be fetched
        :return: a dictionary containing the url, content and the size of the content. If the url does not
        exist in the corpus, a dictionary with content set to None and size set to 0 can be returned.
        """
        url_data = {
            "url": url,
            "content": None,
            "size": 0
        }
        fileAddr = self.corpus.get_file_name(url)
        if fileAddr != None:
            f = open(fileAddr)
            str = f.read()
            url_data["content"] = str.encode('utf-8')
            url_data["size"] = os.path.getsize(fileAddr)
        return url_data

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        outputLinks = []
        print("outptLinks: ", outputLinks)
        print("url_data: ", url_data["content"])
        return outputLinks

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        print(urllib.request.urlopen(url).getcode())
    
        
        parsed = urlparse(url)
<<<<<<< HEAD
        
=======
>>>>>>> c4432a8b40840d8c0736bd6103eebc75cc5e8ff6
        if parsed.scheme not in set(["http", "https"]):
            return False
        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
<<<<<<< HEAD
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower()) and urllib.request.urlopen(url).getcode() == 200
=======
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())\
                   and urllib.request.urlopen(url).getcode() == 200
>>>>>>> c4432a8b40840d8c0736bd6103eebc75cc5e8ff6

        except TypeError:
            print("TypeError for ", parsed)
            return False

<<<<<<< HEAD
=======

>>>>>>> c4432a8b40840d8c0736bd6103eebc75cc5e8ff6
