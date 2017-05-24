import org.jsoup.Connection.Response;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * Created by t8331602 on 19/05/2017.
 */
public class QuerySearch
{

    public static void main(String[] args)
    {
        String search = "What is the best time to fly abroad";


        String[] searchWords = search.split(" ");

        ArrayList<String> ecosiaHrefs = fetchEcosiaHrefs(searchWords, 2);
        ArrayList<String> bingHrefs = fetchBingHrefs(searchWords, 2);
        ArrayList<String> yahooHrefs = fetchYahooHrefs(searchWords, 2);
        ArrayList<String> askHrefs = fetchAskHrefs(searchWords, 2);
        ArrayList<String> searchHrefs = fetchSearchHrefs(searchWords, 2);

        System.out.println(searchHrefs);

        HashSet<String> allHrefs = new HashSet<>();

        System.out.println(allHrefs.addAll(ecosiaHrefs));
        System.out.println(allHrefs.addAll(bingHrefs));
        System.out.println(allHrefs.addAll(yahooHrefs));
        System.out.println(allHrefs.addAll(askHrefs));
        System.out.println(allHrefs.addAll(searchHrefs));
        System.out.println(allHrefs.size());

        ArrayList<String> paragraphs = fetchParagraphsFromHrefs(allHrefs);

        for (String p : paragraphs)
        {
            System.out.println(p);
        }

        System.out.println("Finished");
    }


    /**
     * Returns paragraphs from a list of hyperlinks.
     *
     * @param hrefs A list of hrefs (hyperlinks).
     * @return An ArrayList<String> of all paragraphs selected from the links.
     */
    public static ArrayList<String> fetchParagraphsFromHrefs(Iterable<String> hrefs)
    {
        ArrayList<String> allParagraphs = new ArrayList<>();

        for (String href : hrefs)
        {
            Document doc;

            try
            {
                doc = Jsoup.connect(href).timeout(3000).get();
                Elements paragraphs = doc.select("p");
                for (Element p : paragraphs)
                {
                    allParagraphs.add(p.text());
                }
            }
            catch (IOException | IllegalArgumentException e)
            {
                e.printStackTrace();
            }
        }

        return allParagraphs;
    }


    /**
     * Creates alternative searches by replacing each word with its 5 most relevant queries.
     *
     * @param searchWords The original search query.
     * @param maxSynonyms The maximum amount of relevant synonyms taken for each word.
     * @return An ArrayList of all alternative searches.
     */
    public static ArrayList<String[]> alternativeSearches(String[] searchWords, int maxSynonyms)
    {
        ArrayList<ArrayList<String>> searchSynonyms = new ArrayList<>();
        for (int i = 0; i < searchWords.length; i++)
        {
            String word = searchWords[i];
            ArrayList<String> wordSynonyms = findThesaurusSynonyms(word);
            System.out.println(wordSynonyms);
            searchSynonyms.add(wordSynonyms);
        }

        ArrayList<String[]> alteredSearches = new ArrayList<>();

        for (int i = 0; i < searchWords.length; i++)
        {
            ArrayList<String> currSynonyms = searchSynonyms.get(i);
            for (int j = 0; j < Math.min(currSynonyms.size(), maxSynonyms); j++)
            {
                String[] alteredSearch = searchWords.clone();
                alteredSearch[i] = currSynonyms.get(j);
                alteredSearches.add(alteredSearch);
            }
        }

        return alteredSearches;
    }






    /**
     * Returns hrefs from ecosia.
     *
     * @param searchWords The words of the query.
     * @return An ArrayList<String> of hrefs.
     */
    public static ArrayList<String> fetchEcosiaHrefs(String[] searchWords, int numOfPages)
    {
        String query = String.join("+", searchWords);

        String toEcosia = "&q=" + query;

        String start = "https://www.ecosia.org/search?p=";

        ArrayList<String> hrefs = new ArrayList<>();

        for (int i = 0; i < numOfPages; i++)
        {
            String pNum = String.valueOf(i); // This is what makes ecosia go over the pages
            String currPageURL = start + pNum + toEcosia;

            Document doc;

            try
            {
                doc = Jsoup.connect(currPageURL).timeout(0).get();
                Elements links = doc.select("div[class='result js-result card-mobile']");
                for (Element link : links)
                {
                    Elements currTitle = link.select("a[class='result-title js-result-title']");
                    String url = currTitle.attr("abs:href");
                    hrefs.add(url);
                }
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }

        return hrefs;
    }

    public static ArrayList<String> fetchBingHrefs(String[] searchWords, int numOfPages)
    {
        ArrayList<String> hrefs = new ArrayList<>();

        String query = "q=" + String.join("+", searchWords);
        String start = "http://www.bing.com/search?";
        String cont = "&qs=AS&sc=8-27&sp=1&first=";
        String end = "&FORM=PORE";

        for (int i = 0; i < numOfPages; i++)
        {
            String firstNum = String.valueOf(1 + i * 50);
            String currPageURL = start + query + cont + firstNum + end;

            Document doc;
            try
            {
                doc = Jsoup.connect(currPageURL).timeout(0).get();
                Elements links = doc.select("ol#b_results").select("li[class=b_algo]");
                for (Element link : links)
                {
                    String href = link.select("[href]").attr("href");
                    hrefs.add(href);
                }
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }

        return hrefs;
    }

    /**
     * Fetches hyperlinks from yahoo.com.
     *
     * @param searchWords Words of the query
     * @param numOfPages  Num of pages to crawl
     * @return ArrayList<String> of all hrefs collected.
     */
    public static ArrayList<String> fetchYahooHrefs(String[] searchWords, int numOfPages)
    {
        ArrayList<String> hrefs = new ArrayList<>();
        String baseURL = "https://search.yahoo" +
                ".com/search?p=when+was+marilyn+monroe+born&pz=10&ei=UTF-8&fr=yfp-t-s&fr2=rs-top&bct=0&fp=1" +
                "&b=11&pz=10&bct=0&xargs=0";
        String start = "https://search.yahoo.com/search?";
        String query = "p=" + String.join("+", searchWords);
        String cont = "&pz=10&ei=UTF-8&fr=yfp-t-s&fr2=rs-top&bct=0&fp=1&b=";
        String end = "&pz=10&bct=0&xargs=0";

        for (int i = 0; i < numOfPages; i++)
        {
            String bNum = String.valueOf(1 + i * 10);
            String currPageURL = start + query + cont + bNum + end;
            Document doc;
            try
            {
                doc = Jsoup.connect(currPageURL).timeout(0).get();
                Elements links = doc.select("h3[class=title]");
                for (Element link : links)
                {
                    String href = link.select("[href]").attr("href");
                    hrefs.add(href);
                }
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }

        return hrefs;
    }

    /**
     * Fetches hyperlinks from ask.com.
     *
     * @param searchWords Words of the query
     * @param numOfPages  Num of pages to crawl
     * @return ArrayList<String> of all hrefs collected.
     */
    public static ArrayList<String> fetchAskHrefs(String[] searchWords, int numOfPages)
    {
        ArrayList<String> hrefs = new ArrayList<>();
        String baseURL = "http://www.ask.com/web?q=when+was+marilyn+monroe+born&o=0&qo=pagination&qsrc=998" +
                "&page=2";
        String start = "http://www.ask.com/web?";
        String query = "q=" + String.join("+", searchWords);
        String end = "&o=0&qo=pagination&qsrc=998&page=";

        for (int i = 0; i < numOfPages; i++)
        {
            String pageNum = String.valueOf(1 + i);
            String currPageURL = start + query + end + pageNum;
            Document doc;
            try
            {
                doc = Jsoup.connect(currPageURL).timeout(0).get();
                Elements links = doc.select("div[class=PartialSearchResults-item-title]");
                for (Element link : links)
                {
                    String href = link.select("[href]").attr("href");
                    hrefs.add(href);
                }
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }

        return hrefs;
    }


    /**
     * Fetches hyperlinks from search.com.
     *
     * @param searchWords Words of the query
     * @param numOfPages  Num of pages to crawl
     * @return ArrayList<String> of all hrefs collected.
     */
    public static ArrayList<String> fetchSearchHrefs(String[] searchWords, int numOfPages)
    {
        ArrayList<String> hrefs = new ArrayList<>();
        String baseURL = "https://www.search.com/web?q=when+was+marilyn+monroe+born&qo=homeSearchBox&qsrc=1&ot=organic&page=3&sd=1";
        String start = "https://www.search.com/web?";
        String query = "q=" + String.join("+", searchWords);
        String cont = "&qo=homeSearchBox&qsrc=1&ot=organic&page=";
        String end = "&sd=1";

        for (int i = 0; i < numOfPages; i++)
        {
            String pageNum = String.valueOf(1 + i);
            String currPageURL = start + query + cont + pageNum + end;
            Document doc;
            try
            {
                doc = Jsoup.connect(currPageURL).timeout(0).get();
                Elements links = doc.select("p[class=web-result-url]");
                for (Element link : links)
                {
                    String href = link.text();
                    if (href.contains("http")) hrefs.add(href);
                    else hrefs.add("http://" + href);
                }
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }

        return hrefs;
    }



    /**
     * Returns the synonyms of a word from thesaurus.com
     *
     * @param word A given word
     * @return ArrayList of all synonyms found from thesaurus, ordered by relevance.
     */
    public static ArrayList<String> findThesaurusSynonyms(String word)
    {
        String url = "http://www.thesaurus.com/browse/" + word + "?s=t";

        Document doc;
        ArrayList<String> synonyms;
        synonyms = new ArrayList<String>();

        try
        {
            doc = Jsoup.connect(url).timeout(0).get();
            Elements links = doc.select("div[class=relevancy-list]").select("a[href]");
            for (Element link : links)
            {
                Elements currSyn = link.select("span[class=text]");
                String syn = currSyn.text();
                synonyms.add(syn);
            }
        }
        catch (IOException e)
        {
            System.out.println("Word " + word + " has no thesaurus synonyms");
            //e.printStackTrace();
        }

        return synonyms;
    }
}
