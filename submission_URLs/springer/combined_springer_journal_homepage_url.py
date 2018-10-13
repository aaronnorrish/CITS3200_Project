import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import urllib3

# Removes diacritics from a string.
#   @param string the string for which the diacritics are to be removed
def remove_diacritics(string):
    nfkd_form = unicodedata.normalize('NFKD', string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

# Finds the homepage URL for a journal on the Springer website. If no such page
# exists, return None.
#   @param journal_name the name of the journal to be searched
#   @param ISSN the ISSN of the journal to be searched
#   @param EISSN the EISSN of the journal to be searched
#   @param time_limit the time limit for the URL request
#   @returns the relative path to the journal homepage on the Springer website.
#       If no such page exists, return None.
def get_springer_homepage_url(journal_name, ISSN, EISSN, time_limit):
    springer_home_url = "https://springer.com"
    springer_search_url_start = "https://www.springer.com/gp/search?query="
    springer_search_url_end = "&submit=Submit"

    # relace any ampersands in the journal name with "and"; these are used as
    # special characters in the URL
    search_term = journal_name.replace("&", "and")
    springer_search_url = springer_search_url_start + search_term.replace(" ","+") + springer_search_url_end

    # get the HTML document for the result of this search
    source = requests.get(springer_search_url, timeout=time_limit)
    soup = BeautifulSoup(source.content, 'lxml')

    # iterate through all search results
    for div_tag in soup.find_all("div", {"class":"result-item"}):
        try:
            # only inspect results that are journals
            if div_tag.small.text == "Journal":
                # find the relative path to the current search result's homepage
                journal_homepage_relative_path = div_tag.a.get('href')

                # get the HTML document for this homepage
                journal_source = requests.get(springer_home_url + journal_homepage_relative_path, timeout=time_limit)
                journal_soup = BeautifulSoup(journal_source.content, 'lxml')

                # try to find the journal's ISSN on the journal's homepage
                try:
                    website_ISSN = journal_soup.find("span", {"wicketpath":"content_basic_productDescriptionContainer_productDescription_issnPrint_content"}).text

                    # compare the ISSN on the website with the ISSN in the master list
                    # if have a match then this is the journal we are looking for;
                    # return the relative path to this journal homepage
                    if(website_ISSN == ISSN):
                        return journal_homepage_relative_path
                # could not find an ISSN on the homepage, look for EISSN instead
                except AttributeError:
                    try:
                        website_EISSN = journal_soup.find("span", {"wicketpath":"content_basic_productDescriptionContainer_productDescription_issnElectronic_content"}).text
                        # compare the EISSN on the website with the EISSN in the master list
                        # if have a match then this is the journal we are looking for;
                        # return the relative path to this journal homepage
                        if(website_EISSN == EISSN):
                            return journal_homepage_relative_path
                    # could not find an EISSN on the homepage; inspect the next search result
                    except AttributeError:
                        continue
        # this search result is not a journal; inspect the next search result
        except AttributeError:
            continue
    # could not find the journal we were looking for; return None
    return None

# Finds the homepage URL for a journal on the SpringerLink website. If no such
# page exists, return None.
#   @param journal_name the name of the journal to be searched
#   @param ISSN the ISSN of the journal to be searched
#   @param time_limit the time limit for the URL request
#   @returns the relative path to the journal homepage on the SpringerLink
#       website. If no such page exists, return None.
def get_springer_link_homepage_url(journal_name, ISSN, time_limit):
    springer_link_search_url_start = "https://link.springer.com/search?query="
    springer_link_search_url_end = "&facet-content-type=%22Journal%22"
    springer_link_search_url = springer_link_search_url_start + ISSN + springer_link_search_url_end

    # get the HTML document for the result of this search
    source = requests.get(springer_link_search_url, timeout=time_limit)
    soup = BeautifulSoup(source.content, 'lxml')

    # iterate through all search results
    for journal in soup.findAll("li", {"class":"has-cover"}):
        try:
            # find the relative path to the current search result's homepage
            a_tag = journal.find("div", {"class":"text"}).find('a')
            journal_homepage_relative_path = a_tag.get('href')
            # find the journal name as listed on the website for this search result
            website_journal_name = a_tag.text.replace(",", "").lower()

            # compare the journal name on the website with the journal name
            # in the master list. If we have a match, return the relative path
            # to this journal's homepage
            if journal_name.lower().find(website_journal_name) != -1 or website_journal_name.find(journal_name.lower()) != -1:
                return journal_homepage_relative_path
            else:
                # try removing diacritics and special characters from the journal names, then compare
                j = remove_diacritics(journal_name.lower().replace("the ", "").replace(",","").replace("&", "and"))
                j = re.sub('[^A-Za-z0-9]+', '', j)
                website_journal_name = remove_diacritics(website_journal_name.lower().replace("the ", "").replace("&", "and"))
                website_journal_name = re.sub('[^A-Za-z0-9]+', '', website_journal_name)

                # if we have a match, return the relative path
                if(j == website_journal_name or j.find(website_journal_name) != -1 or website_journal_name.find(j) != -1):
                    return journal_homepage_relative_path

                # could not find a match; inspect the next search result
                else:
                    continue

        # could not find a URL for this search result's homepage; inspect the
        # next search result
        except AttributeError:
            continue

    # we did not find the journal we were looking for, return None
    return None

# Finds the full URL path to the instructions for authors page on the Springer
# website. If it does not exist, return None.
#   @param journal_homepage_URL the full URL path to the journal's homepage on
#       the Springer website
#   @param journal_name the name of the journal
#   @param time_limit the time limit for the URL request
#   @return the URL to the instructions for authors webpage on the Springer
#       website. If it does not exist, return None
def get_instructions_for_authors_url(journal_homepage_URL, journal_name, time_limit):
    # get the HTML document for the journal homepage
    source = requests.get(journal_homepage_URL, timeout=time_limit)
    soup = BeautifulSoup(source.content, 'lxml')

    # iterate through each list element
    for ul_tag in soup.find_all("ul", {"class":"listToOpenLayer"}):
        for li_tag in ul_tag.find_all("li", {"class":"listItemToOpenLayer"}):
            try:
                # extract the title for this list item
                title = li_tag.a.span.text.lower()

                # see if this list item is an instructions for authors item
                if title.find("instructions for authors")!=-1 or title.find("instructions to authors")!=-1 or title.find("author guidelines")!=-1 or title.find("guidelines for submitters")!=-1 or title.find("hinweise für autoren")!=-1:
                    # try to extract the instructions for authors URL from the list item
                    try:
                        guidelines_url = li_tag.find("div", {"class":"wideLayer portletLayer"}).find("div", {"class":"clearfix"}).a.get('href').replace("print_view=true&","")
                        # if this contains a URL, return the URL
                        if guidelines_url is not None:
                            return guidelines_url
                    # try a different method to extract the URL
                    except AttributeError:
                        try:
                            guidelines_url = li_tag.a.get('href')
                            # if this contains a URL, return the URL
                            if guidelines_url is not None:
                                return guidelines_url
                        # unable to extract a URL from this list item; inspect the next list item
                        except AttributeError:
                            print("unable to get instructions for authors link for: ", journal_name)
                            continue
            # the list item does not have a title; inspect the next list item
            except AttributeError:
                continue
    # unable to find a link to the instructions for authors webpage from this
    # journal's homepage; return None
    return None

if __name__ == '__main__':
    # sheet = pd.read_excel("publist_master_no_duplicates.xlsx", header=None)
    sheet = pd.read_excel("springer_no_duplicates.xlsx", header=None)
    l = pd.Series.tolist(sheet)
    headers = l.pop(0)

    springer_home_url = "https://springer.com"
    springer_link_home_url = "https://link.springer.com"

    h,i,f = 0,0,0
    for row in l:
        n_tries = 0
        journal_homepage_relative_path = None
        while(n_tries < 5):
            try:
                journal_homepage_relative_path = get_springer_homepage_url(row[0], row[2], row[3], 12.0 + n_tries * 12.0)
                break
            except(requests.exceptions.RequestException, urllib3.exceptions.HTTPError, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.RequestError, urllib3.exceptions.TimeoutError):
                n_tries += 1
        if journal_homepage_relative_path is None:
            n_tries = 0
            while(n_tries < 5):
                try:
                    journal_homepage_relative_path = get_springer_link_homepage_url(row[0], row[2], 12.0 + n_tries * 12.0)
                    break
                except(requests.exceptions.RequestException, urllib3.exceptions.HTTPError, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.RequestError, urllib3.exceptions.TimeoutError):
                    n_tries += 1
        if journal_homepage_relative_path is not None:
            h+=1 # count number of homepages obtained
            n_tries = 0
            while(n_tries < 5):
                try:
                    instructions_for_authors_URL = get_instructions_for_authors_url(springer_home_url + journal_homepage_relative_path, row[0], 12.0 + n_tries * 12.0)
                    break
                except(requests.exceptions.RequestException, urllib3.exceptions.HTTPError, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.RequestError, urllib3.exceptions.TimeoutError):
                    n_tries += 1
            if row[1].lower().find("springer") == -1:
                print(row[0])
            if instructions_for_authors_URL is not None:
                i+=1
                row.append(instructions_for_authors_URL)
            else:
                row.append(springer_home_url + journal_homepage_relative_path)
        else:
            f += 1
            print("unable to get:", row[0], row[2])

    print(h, i, len(l) - f, len(l))

    headers.append("URL")
    df = pd.DataFrame.from_records(l, columns=headers)
    df.to_excel("combined_springer_urls.xlsx", index=False)
    # df.to_excel("master_urls.xlsx", index=False)
