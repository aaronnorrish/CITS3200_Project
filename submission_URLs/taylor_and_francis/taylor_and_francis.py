import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import sys
import unicodedata
import urllib3

# Removes diacritics from a string.
#   @param string the string for which the diacritics are to be removed
#   @return the input string with all diacritics removed
def remove_diacritics(string):
    nfkd_form = unicodedata.normalize('NFKD', string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

# Finds the relative path to a journal homepage on the Taylor and Francis
# website. If no such page is found, return None.
#   @param journal the name of the journal to be searched
#   @param search_term either the ISSN or the EISSN of the journal to searched
#   @param time_limit the time limit for the URL request
#   @return the relative path to the journal homepage on the Taylor and Francis
#            website. Return None if no such page can be found.
def get_taylor_and_francis_homepage_url(journal, search_term, time_limit):
    home_url = "https://www.tandfonline.com"

    search_url_start = "https://www.tandfonline.com/action/doSearch?AllField="
    search_url = search_url_start + search_term

    # get the HTML document for the result of this search
    source = requests.get(search_url, timeout=time_limit)
    soup = BeautifulSoup(source.content, 'lxml')

    try:
        # find element containing all search results
        ol_tag = soup.find("ol", {"class":"search-results"})

        # iterate through each search result
        for li_tag in ol_tag.find_all("li"):
            # find the relative path to the current search result's (could be a journal, book, etc.) homepage
            relative_path = li_tag.find("div", {"class":"publication-meta"}).span.a.get('href')
            journal_url = home_url + relative_path

            # get the HTML for this homepage
            journal_source = requests.get(journal_url, timeout=time_limit)
            journal_soup = BeautifulSoup(journal_source.content, 'lxml')

            # compare the journal name on the website to the journal name in the master list
            # if we have a match, return the relative path to this journal homepage
            journal_name = journal_soup.find("div", {"class":"journalMetaTitle page-heading"}).a.span.text
            if(journal.lower() == journal_name.lower()):
                return relative_path
            else:
                # try removing diacritics from the journal names, then compare
                j = remove_diacritics(journal.lower().replace("the ", "").replace(",","").replace("&", "and"))
                journal_name = remove_diacritics(journal_name.lower().replace("the ", "").replace(",","").replace("&", "and"))
                if(j == journal_name or j.find(journal_name) != -1 or journal_name.find(j) != -1):
                    return relative_path
                else:
                    # try removing any special characters, then compare
                    j = re.sub('[^A-Za-z0-9]+', '', j)
                    journal_name = re.sub('[^A-Za-z0-9]+', '', journal_name)
                    if(j == journal_name or j.find(journal_name) != -1 or journal_name.find(j) != -1):
                        return relative_path
                    # we cannot match the journal names; inspect the next search result
                    else:
                        continue
    except AttributeError:
        # we were not able to generate any search results, return None
        return None
    # we did not find the journal we were looking for, return None
    return None

# Finds the full URL path to the instructions for authors page, or if it does
# not exist, the homepage for a journal on the Taylor and Francis website.
#   @param relative_path the relative path to the journal's homepage
#   @param time_limit the time limit for the URL request
#   @return the path to the instructions for authors webpage, or failing that,
#       the homepage for the journal on the Taylor and Francis
def get_taylor_and_francis_instructions_for_authors_url(relative_path, time_limit):
    home_url = "https://www.tandfonline.com"
    instructions_url_start = "/action/authorSubmission?journalCode="
    instructions_url_end = "&page=instructions"

    # extract the journal code from the relative path
    code = re.search('/toc/(.+?)/current', relative_path).group(1)
    instructions_url = home_url + instructions_url_start + code + instructions_url_end

    # check that the URL leads to an instructions for authors page
    instructions_source = requests.get(instructions_url, timeout=time_limit)
    instructions_soup = BeautifulSoup(instructions_source.content, 'lxml')

    try:
        # if the instructions for authors page exists return the URL for this page
        if instructions_soup.head.title.text != "Error":
            return instructions_url
        # otherwise return the URL for the journal homepage
        else:
            return home_url + relative_path
    except AttributeError:
        return home_url + relative_path

if __name__ == '__main__':
    sheet = pd.read_excel("taylor_and_francis_no_duplicates.xlsx", header=None)
    l = pd.Series.tolist(sheet)
    headers = l.pop(0)

    s = 0
    for i in range(len(l)):
        n_tries = 0
        journal_homepage_relative_path = None
        journal_page = None
        while(n_tries < 5):
            try:
                journal_homepage_relative_path = get_taylor_and_francis_homepage_url(l[i][0], l[i][2], 24.0 + n_tries * 24.0)
                if journal_homepage_relative_path is None:
                    journal_homepage_relative_path = get_taylor_and_francis_homepage_url(l[i][0], l[i][3], 24.0 + n_tries * 24.0) # maybe separate instead of nest -> could cause a problem
                break
            except(requests.exceptions.RequestException, urllib3.exceptions.HTTPError, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.RequestError, urllib3.exceptions.TimeoutError):
                n_tries += 1

        if journal_homepage_relative_path is not None:
            n_tries = 0
            while(n_tries < 5):
                try:
                    journal_page = get_taylor_and_francis_instructions_for_authors_url(journal_homepage_relative_path, 24.0 + n_tries * 24.0)
                    break
                except(requests.exceptions.RequestException, urllib3.exceptions.HTTPError, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.RequestError, urllib3.exceptions.TimeoutError):
                    n_tries += 1

        if journal_page is not None:
            s+=1
            l[i].append(journal_page)

    print(s, len(l), s/len(l))

    headers.append("Homepage URL")
    df = pd.DataFrame.from_records(l, columns=headers)
    df.to_excel("taylor_and_francis_journal_homepage_urls.xlsx", index=False)
