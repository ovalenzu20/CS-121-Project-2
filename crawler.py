import logging
import re
from urllib.parse import urlparse, urljoin, parse_qs
from corpus import Corpus
import lxml
import urllib.request
import http.client
import os
import urllib.request
from collections import defaultdict

from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier):
        self.frontier = frontier
        self.corpus = Corpus()
        self.maxValidOutLinks = ["", float("-inf")]
        self.numberOfLinksCrawled = 0
        self.TRAP_PARAMS = {"action=download","action=login","action=edit"}
        self.domainCounts = defaultdict(int)
        self.domainAndOutputLinks = defaultdict(int)
        self.trapUrls = []

    #Assumption: all links are processed -- we have to check if they're traps and if valid
    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            
            url_data = self.fetch_url(url)
            print(url_data["url"])
            outputLinks = self.extract_next_links(url_data)
            self.domainAndOutputLinks[url_data["url"]] = len(outputLinks)
            
            validOutputLinks = 0
            
            for next_link in outputLinks:
                if self.corpus.get_file_name(next_link) is not None:
                    if self.is_valid(next_link):
                        validOutputLinks += 1
                        self.frontier.add_url(next_link)
                        
            if validOutputLinks > self.maxValidOutLinks[1]:
                self.maxValidOutLinks[0] = url_data["url"]
                self.maxValidOutLinks[1] = validOutputLinks
            
            validOutputLinks = 0
                        
                        

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
        
        beautifulSoup = BeautifulSoup(url_data["content"], "lxml")
        aTags = beautifulSoup.find_all("a")
                
        try:
            baseURL = url_data["url"]
            
            for link in aTags:
                relativeURL = link.attrs["href"]
                absoluteURL = urljoin(baseURL, relativeURL)
                outputLinks.append(absoluteURL)
                self.numberOfLinksCrawled += 1
                
        except KeyError:
            pass
        
        return outputLinks


    def is_trap(self, parsed):
        if parsed[:6] == "mailto":
            return True

        #Return false if we receive some parameters that know are bad
        if parsed.query in self.TRAP_PARAMS:
            return True
        
        #If the URL has been accessed more than 13 times return false
        domainName = parsed.netloc + parsed.path
        self.domainCounts[domainName] += 1
        if self.domainCounts[domainName] > 13:
            return True

        if parsed.scheme not in set(["http", "https"]):
            return True
    
        return False
    
    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        parsed = urlparse(url)
#         print(parsed.netloc)
        if self.is_trap(parsed):
            self.trapUrls.append(parsed.netloc + parsed.path)
            return False

        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower()) #and urllib.request.urlopen(url).getcode() == 200

        except TypeError:
            print("TypeError for ", parsed)
            return False
        
        
        
    def printDomains(self):
        pass
#         print(f"Max Output Links: {self.maxOutLinks[0], self.maxOutLinks[1]}")
#         
#         for d,c in self.domainCounts.items():
#             print(f"Domain: {d}, {c}")
#             
#         print("-----------------------------")
#         
#         for trap in self.trapUrls:
#             print(trap)
# 
#         for d, c in self.domainAndOutputLinks.items():
#             print(f"Domain: {d}, OutputLinksCount: {c}")
        
#         print(self.maxValidOutLinks)
        
