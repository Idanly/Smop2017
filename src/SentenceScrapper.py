import re
import time
from multiprocessing import Pool
from threading import Thread, Lock
import os

import certifi
import urllib3
from bs4 import BeautifulSoup

from RelevancyFinder import RelevancyFinder
from RelevantSentencesScrapper import RelevantSentencesScrapper

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), timeout=3.0)

class SearchEngineLinkExtractor:
    def __init__(self, search_words, num_pages=-1):
        self.search_words = search_words
        self.num_pages = num_pages
        self.page_counter = 0

        self.q = "+".join(self.search_words)

    def __iter__(self):
        return self.next_href()

    def next_href(self):
        while self.page_counter != self.num_pages:
            curr_page_url = self.page_url()
            request = http.request('GET', curr_page_url)
            time.sleep(0.15)
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
        self.url_set = set()
        self.url_list = list()
        self.search_query = search_query

        self.kill_flag = False
        self.thread_list = list()
        self.start_extraction()

    def extract_links(self, link_extractor):
        for links_list in link_extractor:
            for url in links_list:
                if url not in self.url_set:
                    if self.kill_flag:
                        print(link_extractor.__class__.__name__ + " was killed")
                        return
                    self.url_set.add(url)
                    self.url_list.append(url)

    def start_extraction(self):
        self.url_list = list()
        self.url_set = set()
        self.kill_flag = False
        search_words = self.search_query.split(" ")
        ecosia_extractor = EcosiaLinkExtractor(search_words, 2)
        ecosia_thread = Thread(target=self.extract_links, args=(ecosia_extractor,))
        bing_extractor = BingLinkExtractor(search_words, 2)
        bing_thread = Thread(target=self.extract_links, args=(bing_extractor,))
        yahoo_extractor = YahooLinkExtractor(search_words, 2)
        yahoo_thread = Thread(target=self.extract_links, args=(yahoo_extractor,))
        ask_extractor = AskLinkExtractor(search_words, 2)
        ask_thread = Thread(target=self.extract_links, args=(ask_extractor,))
        self.thread_list = [ecosia_thread, bing_thread, yahoo_thread, ask_thread]
        # Google extractor doesn't work atm
        ecosia_thread.start()
        bing_thread.start()
        yahoo_thread.start()
        ask_thread.start()

    def __iter__(self):
        while (not self.finished()) or self.url_list:
            try:
                yield self.url_list.pop(0)
            except IndexError:
                yield ""

    def finished(self):
        return all(not thread.isAlive() for thread in self.thread_list)


class ParagraphScrapper:
    results_lock = Lock()
    paragraph_lock = Lock()

    def __init__(self, search_query):
        self.paragraph_list = list()
        self.search_query = search_query
        self.link_extractor = SearchEngineScrapper(search_query=search_query)
        self.kill_flag = False
        self.results = list()
        self.extraction_thread = Thread(target=self.start_extraction)
        self.results_thread = Thread(target=self.get_results)
        self.extraction_thread.start()
        self.results_thread.start()

    def start_extraction(self):
        pool = Pool(processes=6)
        for url in self.link_extractor:
            if self.kill_flag:
                pool.terminate()
                return
            if url is not "":
                with ParagraphScrapper.results_lock:
                    self.results.append(pool.apply_async(func=ParagraphScrapper.extract_paragraphs, args=(url,)))
            else:
                time.sleep(0.15)

    def get_results(self):
        while True:
            if self.finished():
                return
            with ParagraphScrapper.results_lock:
                copy_results = self.results.copy()
                self.results.clear()
            unfinished = list()
            for res in copy_results:
                if res.ready():
                    with ParagraphScrapper.paragraph_lock:
                        self.paragraph_list.extend(res.get())
                else:
                    unfinished.append(res)
            with ParagraphScrapper.results_lock:
                self.results.extend(unfinished)
            time.sleep(0.2)

    @staticmethod
    def extract_paragraphs(url):
        try:
            request = http.request('GET', url)
            soup = BeautifulSoup(request.data, "lxml")
            paragraphs = soup.find_all("p")
            return [p.text for p in paragraphs]
        except Exception as e:
            print("error from extract paragraphs: " + str(e))

    def flush_paragraphs(self):
        with self.paragraph_lock:
            curr_paragraphs = self.paragraph_list.copy()
            self.paragraph_list.clear()
        return curr_paragraphs

    def has_n_paragraphs(self, n):
        return len(self.paragraph_list) >= n

    def kill(self):
        self.kill_flag = True

    def finished(self):
        return self.kill_flag or not(self.extraction_thread.is_alive() or self.results)

    def get_paragraphs(self):
        return self.paragraph_list.copy()


class SentenceScrapper:
    def __init__(self, query):
        self.query = query
        self.scrapper = ParagraphScrapper(search_query=self.query)
        self.pattern = re.compile('[.][A-Z]')
        self.dash_pattern = re.compile('[-]')
        self.space_pattern = re.compile('\s+')
        self.forbidden_pattern = re.compile('http|\?')  # We don't want a sentence with a link or a question
        self.sentences_returned = list()

    def __iter__(self):
        while (not self.scrapper.finished()) or self.scrapper.has_n_paragraphs(1):
            flushed = self.scrapper.flush_paragraphs()
            if not flushed:
                time.sleep(0.2)
            for p in flushed:
                try:
                    p = self.space_pattern.sub(' ', self.dash_pattern.sub(' ', p)).strip()
                except TypeError as e:
                    continue
                sentences = p.split('. ')
                for s in sentences:
                    if re.search(self.forbidden_pattern, s):
                        continue
                    if re.search(self.pattern,
                                 s):  # There is a sentence starting right after a period (with no space)
                        more_split = s.split('.')
                        for t in more_split:
                            self.sentences_returned.append(t)
                            yield t
                    else:
                        self.sentences_returned.append(s)
                        yield s

    def kill(self):
        self.scrapper.kill()

    def get_sentences_returned(self):
        return self.sentences_returned


if __name__ == "__main__":
    query_to_pass = "when was marilyn monroe born"

    relevancy_finder = RelevancyFinder()
    time1 = time.time()
    query_important_words = relevancy_finder.important_query_words(query=query_to_pass)
    query_important_joined = ' '.join(query_important_words)
    print("Time to filter query: " + str(time.time() - time1))
    time2 = time.time()
    sentence_scrapper = SentenceScrapper(query=query_important_joined)
    print("Time to init sentence scrapper: " + str(time.time() - time2))
    time3 = time.time()
    rel_scrapper = RelevantSentencesScrapper(s_scrapper=sentence_scrapper, search_words=query_important_words,
                                             max_sentences=100)
    rel_sentences = list(rel_scrapper)
    print("Time to scrape relevant sentences: " + str(time.time() - time3))
    sentence_scrapper.kill()

    print("relevant sentences:")
    for sent in rel_sentences:
        print(sent)

    # all_sentences = sentence_scrapper.get_sentences_returned()
    """
    rel_sentences_ordered = relevancy_finder.find_most_relevant_sentence(query=query_to_pass,
                                                                         all_sentences=None,
                                                                         rel_sentences=rel_sentences)
    print("relevant sentences ordered:")
    for sent in rel_sentences_ordered:
        print(sent)
    """