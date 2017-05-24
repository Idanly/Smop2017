import time
from threading import Thread

import certifi
import urllib3
from bs4 import BeautifulSoup


class SearchEngineLinkExtractor:
    def __init__(self, search_words, num_pages=-1):
        self.search_words = search_words
        self.num_pages = num_pages
        self.page_counter = 0
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=3.0)
        self.q = "+".join(self.search_words)

    def __iter__(self):
        return self.next_href()

    def next_href(self):
        while self.page_counter != self.num_pages:
            curr_page_url = self.page_url()
            request = self.http.request('GET', curr_page_url)
            time.sleep(0.3)
            soup = BeautifulSoup(request.data, "lxml")
            page_hrefs = self.parse_page_hrefs(soup)
            yield page_hrefs
            self.page_counter += 1

    def page_url(self):
        # To be implemented by inheriting classes
        return None

    def parse_page_hrefs(self, soup):
        # To be implemented by inheriting classes
        return None


class EcosiaLinkExtractor(SearchEngineLinkExtractor):
    def page_url(self):
        to_ecosia = "&q=" + self.q
        start = "https://www.ecosia.org/search?p="
        return start + str(self.page_counter) + to_ecosia

    def parse_page_hrefs(self, soup):
        results_hrefs = [title["href"] for title in
                         soup.findAll("a", class_="result-title js-result-title") if title is not None]
        return results_hrefs


class BingLinkExtractor(SearchEngineLinkExtractor):
    def page_url(self):
        start = "http://www.bing.com/search?q="
        cont = "&qs=AS&sc=8-27&sp=1&first="
        end = "&FORM=PORE"
        return start + self.q + cont + str(1 + self.page_counter * 50) + end

    def parse_page_hrefs(self, soup):
        results_titles = [result.find("a") for result in soup.findAll("li", class_="b_algo")]
        results_hrefs = [title["href"] for title in results_titles if title is not None]
        return results_hrefs


class YahooLinkExtractor(SearchEngineLinkExtractor):
    def page_url(self):
        start = "https://search.yahoo.com/search?p="
        cont = "&pz=10&ei=UTF-8&fr=yfp-t-s&fr2=rs-top&bct=0&fp=1&b="
        end = "&pz=10&bct=0&xargs=0"
        return start + self.q + cont + str(1 + self.page_counter * 10) + end

    def parse_page_hrefs(self, soup):
        results_titles = [result.find("a") for result in soup.findAll("h3", class_="title")]
        results_hrefs = [title['href'] for title in results_titles if title is not None]
        return results_hrefs


class AskLinkExtractor(SearchEngineLinkExtractor):
    def page_url(self):
        start = "http://www.ask.com/web?q="
        cont = "&o=0&qo=pagination&qsrc=998&page="
        end = ""
        return start + self.q + cont + str(1 + self.page_counter) + end

    def parse_page_hrefs(self, soup):
        results_titles = [result.find("a") for result in soup.findAll("div", class_="PartialSearchResults-item-title")]
        results_hrefs = [title['href'] for title in results_titles if title is not None]
        return results_hrefs


class GoogleLinkExtractor(SearchEngineLinkExtractor):
    """
    Google link extractor - DOES NOT WORK
    For some reason the openend page of this url is not the same page viewed in the browser
    """
    def page_url(self):
        start = "https://www.google.co.il/?gfe_rd=cr&ei=Pz8kWY_AE5Pd8AeOh67QBw#q="
        cont = "&start="
        end = "&num=20"
        return start + self.q + cont + str(self.page_counter * 10) + end

    def parse_page_hrefs(self, soup):
        results_titles = [result.find('a') for result in soup.findAll('h3', {'class': 'r'})]
        results_hrefs = [title['href'] for title in results_titles if title is not None]
        return results_hrefs


class SearchEngineScrapper:

    def __init__(self, search_query):
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=3.0)
        self.url_set = set()
        self.paragraph_list = list()
        self.search_query = search_query
        self.start_extraction()
        self.thread_list = list()
        self.kill_flag = False

    def extract_paragraphs(self, link_extractor):
        for links_list in link_extractor:
            for url in links_list:
                if url not in self.url_set:
                    if self.kill_flag:
                        return
                    self.url_set.add(url)
                    try:
                        request = self.http.request('GET', url)
                        time.sleep(0.3)
                        soup = BeautifulSoup(request.data, "lxml")
                        paragraphs = soup.find_all("p")
                        self.paragraph_list.extend([p.text for p in paragraphs])
                    except Exception as e:
                        print("error from extract paragraphs: " + str(e))

    def start_extraction(self):
        self.paragraph_list = list()
        self.url_set = set()
        self.kill_flag = False
        search_words = self.search_query.split(" ")
        ecosia_extractor = EcosiaLinkExtractor(search_words, 1)
        ecosia_thread = Thread(target=self.extract_paragraphs, args=(ecosia_extractor,))
        bing_extractor = BingLinkExtractor(search_words, 1)
        bing_thread = Thread(target=self.extract_paragraphs, args=(bing_extractor,))
        yahoo_extractor = YahooLinkExtractor(search_words, 1)
        yahoo_thread = Thread(target=self.extract_paragraphs, args=(yahoo_extractor,))
        ask_extractor = AskLinkExtractor(search_words, 1)
        ask_thread = Thread(target=self.extract_paragraphs, args=(ask_extractor,))
        self.thread_list = [ecosia_thread, bing_thread, yahoo_thread, ask_thread]
        # Google extractor doesn't work atm
        ecosia_thread.start()
        bing_thread.start()
        yahoo_thread.start()
        ask_thread.start()

    def has_n_paragraphs(self, n):
        return len(self.paragraph_list) >= n

    def finished(self):
        return all(not thread.isAlive() for thread in self.thread_list)

    def kill(self):
        self.kill_flag = True

    def get_paragraphs(self):
        return self.paragraph_list.copy()


class Paragraph_Scrapper:
    def __init__(self, query):
        self.query = query

    def get_n_paragraphs(self, n):
        scrapper = SearchEngineScrapper(search_query=self.query)
        while not scrapper.has_n_paragraphs(n) or not scrapper.finished():
            time.sleep(0.5)
        scrapper.kill()
        return scrapper.get_paragraphs()


if __name__ == "__main__":
    query_to_pass = "what is the depth of the mediterranean sea"
    pretime = time.time()
    p_scrapper = Paragraph_Scrapper(query_to_pass)
    paragraphs = p_scrapper.get_n_paragraphs(300)
    posttime = time.time()
    print("time diff: " + str(posttime - pretime))
    print(paragraphs)
