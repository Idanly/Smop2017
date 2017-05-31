import re
import time
import unicodedata
from functools import reduce
from threading import Thread

import certifi
import urllib3
from bs4 import BeautifulSoup


class TriviaQuestionCrawler:
    def __init__(self, num_pages=-1):
        self.num_pages = num_pages
        self.page_counter = 0
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        self.crawl_flag = False
        self.punct_pattern = re.compile('[,\.!?:"]')
        self.underscore_patten = re.compile('[_]{2,}')
        self.space_pattern = re.compile('[ ]{2,}')

    def start_crawling(self):
        self.crawling_thread = Thread(target=self.scrape_questions)
        self.crawl_flag = True
        self.target_file = open('questions.txt', 'ab')
        self.crawling_thread.start()

    def scrape_questions(self):
        while self.page_counter != self.num_pages and self.crawl_flag:
            curr_page_url = self.page_url()
            request = self.http.request('GET', curr_page_url)
            time.sleep(0.2)
            soup = BeautifulSoup(request.data, "lxml")
            self.parse_page_questions(soup)
            self.page_counter += 1
        self.target_file.close()

    def kill(self):
        self.crawl_flag = False

    def page_url(self):
        return "http://www.trivia-questions.net/page/" + str(self.page_counter + 1)

    def parse_page_questions(self, soup):
        quotes = soup.find_all("div", {'class': 'quote-content'})
        questions = [str(href.find('a').contents[0]).strip() for href in quotes]
        reduced = reduce(lambda x, y: x + '\n' + y, questions) + '\n'
        filtered = self.space_pattern.sub(' ', self.underscore_patten.sub('what', self.punct_pattern.sub('', reduced)))
        self.target_file.write(unicodedata.normalize('NFD', filtered).encode('ascii', 'ignore'))
        print("parsed page num " + str(self.page_counter))


if __name__ == "__main__":
    crawler = TriviaQuestionCrawler(1142)
    crawler.start_crawling()
