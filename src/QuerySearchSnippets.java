import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Map;

/**
 * Created by t8331602 on 22/05/2017.
 */
public class QuerySearchSnippets
{
    /**
     * Do not search google repeatedly - ip will get blocked.
     *
     * @param searchWords The words of the query.
     * @return An entry with key = ArrayList of titles, value = ArrayList of snippets.
     */
    public static Map.Entry<ArrayList<String>, ArrayList<String>> fetchGoogleTitlesAndSnippets(String[]
                                                                                                       searchWords,
                                                                                               int numResults)
    {
        String toGoogle = String.join("+", searchWords);

        toGoogle = "q=" + toGoogle;

        String url = "http://www.google.com/search?" + toGoogle + "&num=" + String.valueOf(numResults);

        Document doc;
        ArrayList<String> titles, snippets;
        titles = new ArrayList<>();
        snippets = new ArrayList<>();

        try
        {
            doc = Jsoup.connect(url).timeout(0).get();
            Elements links = doc.select("div.rc");
            for (Element link : links)
            {
                Elements currTitle = link.select("h3[class=r]");
                String title = currTitle.text();
                titles.add(title);

                Elements currSnippet = link.select("span[class=st]");
                String snippet = currSnippet.text();
                snippets.add(snippet);
            }
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }

        return new Map.Entry<ArrayList<String>, ArrayList<String>>()
        {
            @Override
            public ArrayList<String> getKey()
            {
                return titles;
            }

            @Override
            public ArrayList<String> getValue()
            {
                return snippets;
            }

            @Override
            public ArrayList<String> setValue(ArrayList<String> value)
            {
                return null;
            }
        };

    }

    /**
     * Returns titles and snippets from ecosia.
     *
     * @param searchWords The words of the query.
     * @return An entry with key = ArrayList of titles, value = ArrayList of snippets.
     */
    public static Map.Entry<ArrayList<String>, ArrayList<String>> fetchEcosiaTitlesAndSnippets(String[]
                                                                                                       searchWords,
                                                                                               int numOfPages)
    {
        String query = String.join("+", searchWords);

        String toEcosia = "&q=" + query;

        String start = "https://www.ecosia.org/search?p=";

        ArrayList<String> titles = new ArrayList<>();
        ArrayList<String> snippets = new ArrayList<>();

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
                    String title = currTitle.text();
                    titles.add(title);

                    Elements currSnippet = link.select("p[class=result-snippet]");
                    String snippet = currSnippet.text();
                    snippets.add(snippet);
                }
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }

        return new Map.Entry<ArrayList<String>, ArrayList<String>>()
        {
            @Override
            public ArrayList<String> getKey()
            {
                return titles;
            }

            @Override
            public ArrayList<String> getValue()
            {
                return snippets;
            }

            @Override
            public ArrayList<String> setValue(ArrayList<String> value)
            {
                return null;
            }
        };

    }


    /**
     * Fetches titles and snippets from dogpile (fortunately dogpile does not block your ip).
     *
     * @param searchWords The words of the query.
     * @param numOfPages  Number of pages of results to scrape.
     * @return An entry with key = ArrayList of titles, value = ArrayList of snippets.
     */
    public static Map.Entry<ArrayList<String>, ArrayList<String>> fetchDogpileTitlesAndSnippets(String[]
                                                                                                        searchWords,
                                                                                                int numOfPages)
    {
        String start = "http://www.dogpile.com/search/web?qsi=";

        String query = String.join("+", searchWords);
        String toDogpile = "&q=" + query;

        String end = "&fcoid=4&fcop=results-bottom&om_nextpage=True&fpid=2";

        ArrayList<String> titles = new ArrayList<>();
        ArrayList<String> snippets = new ArrayList<>();

        for (int i = 0; i < numOfPages; i++)
        {
            String qsiNum = String.valueOf(1 + 15 * i); // This is what makes dogpile go over the pages
            String currPageURL = start + qsiNum + toDogpile + end;

            Document doc;

            try
            {
                doc = Jsoup.connect(currPageURL).timeout(0).get();
                Elements links = doc.select("div#webResults");
                for (Element link : links)
                {
                    Elements titleElement = link.select("a[class=resultTitle]");
                    String title = titleElement.text();
                    titles.add(title);

                    Elements snippetElement = link.select("div[class=resultDescription]");
                    String snippet = snippetElement.text();
                    snippets.add(snippet);
                }
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }

        return new Map.Entry<ArrayList<String>, ArrayList<String>>()
        {
            @Override
            public ArrayList<String> getKey()
            {
                return titles;
            }

            @Override
            public ArrayList<String> getValue()
            {
                return snippets;
            }

            @Override
            public ArrayList<String> setValue(ArrayList<String> value)
            {
                return null;
            }
        };
    }
}
