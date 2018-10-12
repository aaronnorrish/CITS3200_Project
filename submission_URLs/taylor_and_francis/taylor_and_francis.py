import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import sys
import unicodedata
import urllib3


def remove_accents(string):
    nfkd_form = unicodedata.normalize('NFKD', string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def get_taylor_and_francis_homepage(journal, search_term, time_limit):
    home_url = "https://www.tandfonline.com"
    search_url_start = "https://www.tandfonline.com/action/doSearch?AllField="

    search_url = search_url_start + search_term
    source = requests.get(search_url, timeout=time_limit)
    soup = BeautifulSoup(source.content, 'lxml')
    found = False
    try:
        ol_tag = soup.find("ol", {"class":"search-results"})
        for li_tag in ol_tag.find_all("li"):
            relative_path = li_tag.find("div", {"class":"publication-meta"}).span.a.get('href')
            journal_url = home_url + relative_path
            journal_source = requests.get(journal_url, timeout=time_limit)
            journal_soup = BeautifulSoup(journal_source.content, 'lxml')
            journal_name = journal_soup.find("div", {"class":"journalMetaTitle page-heading"}).a.span.text
            if(journal.lower() == journal_name.lower()):
                return relative_path
            else:
                j = remove_accents(journal.lower().replace("the ", "").replace(",","").replace("&", "and"))
                journal_name = remove_accents(journal_name.lower().replace("the ", "").replace(",","").replace("&", "and"))
                if(j == journal_name or j.find(journal_name) != -1 or journal_name.find(j) != -1):
                    return relative_path
                else:
                    j = re.sub('[^A-Za-z0-9]+', '', j)
                    journal_name = re.sub('[^A-Za-z0-9]+', '', journal_name)
                    if(j == journal_name or j.find(journal_name) != -1 or journal_name.find(j) != -1):
                        return relative_path
                    else:
                        continue
    except AttributeError:
        return None
    return None

def get_taylor_and_francis_instructions_for_authors(relative_path, time_limit):
    home_url = "https://www.tandfonline.com"
    instructions_url_start = "/action/authorSubmission?journalCode="
    instructions_url_end = "&page=instructions"

    code = re.search('/toc/(.+?)/current', relative_path).group(1)
    instructions_url = home_url + instructions_url_start + code + instructions_url_end
    instructions_source = requests.get(instructions_url, timeout=time_limit)
    instructions_soup = BeautifulSoup(instructions_source.content, 'lxml')
    if instructions_soup.head.title.text != "Error":
        return instructions_url
    else:
        return home_url + relative_path

if __name__ == '__main__':
    sheet = pd.read_excel("taylor_and_francis_no_duplicates.xlsx", header=None)
    l = pd.Series.tolist(sheet)
    headers = l.pop(0)

    s,t,w, = 0,0,0
    for i in range(len(l)):
        t +=1
        exception = True
        n_tries = 0
        while(exception and n_tries < 5):
            try:
                journal_homepage_relative_path = get_taylor_and_francis_homepage(l[i][0], l[i][2], 12.0 + n_tries * 12.0)
                if journal_homepage_relative_path is None:
                    journal_homepage_relative_path = get_taylor_and_francis_homepage(l[i][0], l[i][3], 12.0 + n_tries * 12.0) # maybe separate instead of nest -> could cause a problem
                exception = False
            except(requests.exceptions.RequestException, urllib3.exceptions.HTTPError, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.RequestError, urllib3.exceptions.TimeoutError):
                # pass
                n_tries += 1
                exception = True
        if journal_homepage_relative_path is not None:
            exception = True
            n_tries = 0
            while(exception and n_tries < 5):
                try:
                    journal_page = get_taylor_and_francis_instructions_for_authors(journal_homepage_relative_path, 12.0 + n_tries * 12.0)
                    exception = False
                except(requests.exceptions.RequestException, urllib3.exceptions.HTTPError, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.RequestError, urllib3.exceptions.TimeoutError):
                    # pass
                    n_tries += 1
                    exception = True
        if journal_page is not None:
            s+=1
            print(s, t, s/t)
            l[i].append(journal_page)

    print(s, t, w, len(l), (s+t+w)/len(l))

    headers.append("Homepage URL")
    df = pd.DataFrame.from_records(l, columns=headers)
    df.to_excel("taylor_and_francis_journal_homepage_urls.xlsx", index=False)
