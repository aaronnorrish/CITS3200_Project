import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

# TODO need to remove print statements
# enclose getting source in try/except
# try/except for result-items?
# have functions for springer and springer link ?
# add a timeout? retry
# need a try for .find code

def remove_accents(string):
    nfkd_form = unicodedata.normalize('NFKD', string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def get_springer_homepage_url(journal_name, ISSN, EISSN):
    springer_home_url = "https://springer.com"
    springer_search_url_start = "https://www.springer.com/gp/search?query="
    springer_search_url_end = "&submit=Submit"

    # search_term = re.sub('[^ a-zA-Z0-9]', '', journal_name)
    search_term = journal_name.replace("&", "and")
    # search_term = journal_name.replace("&", "%26")
    # print(search_term)
    springer_search_url = springer_search_url_start + search_term.replace(" ","+") + springer_search_url_end
    # print(search_url)
    source = requests.get(springer_search_url)
    soup = BeautifulSoup(source.content, 'lxml')
    for div_tag in soup.find_all("div", {"class":"result-item"}):
        if div_tag.small.text == "Journal":
            journal_homepage_relative_path = div_tag.a.get('href')
            journal_source = requests.get(springer_home_url + journal_homepage_relative_path)
            journal_soup = BeautifulSoup(journal_source.content, 'lxml')
            try:
                website_ISSN = journal_soup.find("span", {"wicketpath":"content_basic_productDescriptionContainer_productDescription_issnPrint_content"}).text
                if(website_ISSN == ISSN):
                    return journal_homepage_relative_path
                    # print(journal_name)
                    # row.append(journal_homepage_relative_path)
                    # s+=1
                    # break
            except AttributeError:
                try:
                    website_EISSN = journal_soup.find("span", {"wicketpath":"content_basic_productDescriptionContainer_productDescription_issnElectronic_content"}).text
                    if(website_EISSN == ISSN):
                        return journal_homepage_relative_path
                        # print(journal_name)
                        # row.append(journal_homepage_relative_path)
                        # s+=1
                        # break
                except AttributeError:
                    continue
                    # print("ERROR: unable to get ISSN for ", journal_name)
    return None

def get_springer_link_homepage_url(journal_name, ISSN):
    springer_link_search_url_start = "https://link.springer.com/search?query="
    springer_link_search_url_end = "&facet-content-type=%22Journal%22"

    springer_link_search_url = springer_link_search_url_start + ISSN + springer_link_search_url_end
    source = requests.get(springer_link_search_url)
    soup = BeautifulSoup(source.content, 'lxml')

    journals = soup.findAll("li", {"class":"has-cover"})
    if len(journals) == 0:
        print("no seach results: ", journal_name, ISSN)
    for journal in journals:
        # for link in :
        a_tag = journal.find("div", {"class":"text"}).find('a') # assumes each entry has text div
        journal_homepage_relative_path = a_tag.get('href')
        website_journal_name = a_tag.text.replace(",", "").lower()
        if journal_name.lower().find(website_journal_name) != -1 or website_journal_name.find(journal_name.lower()) != -1:
            # row.append(springer_home_url + journal_homepage_relative_path)
            return journal_homepage_relative_path
            # s += 1
            # break
        else: # the search is done on the ISSN so could just do it anyway
            # try:
            # need to open up link to check this
            # print_issn = issn_tag.find("span", {"class":"pissn"}).split(" ")[0]
            j = remove_accents(journal_name.lower().replace("the ", "").replace(",","").replace("&", "and"))
            j = re.sub('[^A-Za-z0-9]+', '', j)
            website_journal_name = remove_accents(website_journal_name.lower().replace("the ", "").replace("&", "and"))
            website_journal_name = re.sub('[^A-Za-z0-9]+', '', website_journal_name)
            if(j == website_journal_name or j.find(website_journal_name) != -1 or website_journal_name.find(j) != -1):
                return journal_homepage_relative_path
                # row.append(springer_home_url + journal_homepage_relative_path)
                # s+=1
                # break
            else:
                print("unable to match: ", soup.find("div", {"id":"issn"}), journal_name, ISSN)
    return None

if __name__ == '__main__':
    sheet = pd.read_excel("springer_no_duplicates.xlsx", header=None)
    l = pd.Series.tolist(sheet)
    headers = l.pop(0)

    springer_home_url = "https://springer.com"
    springer_link_home_url = "https://link.springer.com"


    s,f = 0,0
    for row in l:
        journal_homepage_relative_path = get_springer_homepage_url(row[0], row[2], row[3])
        if journal_homepage_relative_path is None:
            print("unable to get from springer:", row[0], row[2])
            journal_homepage_relative_path = get_springer_link_homepage_url(row[0], row[2])
        if journal_homepage_relative_path is None:
            f += 1
            print("unable to get:", row[0], row[2])
        else:
            s += 1
            row.append(springer_home_url + journal_homepage_relative_path)
        # if journal_homepage_relative_path is not None:
        #     instructions_for_authors_URL = get_instructions_for_authors(springer_home_url + journal_homepage_relative_path)
        #     if instructions_for_authors_URL is not None:
        #         row.append(instructions_for_authors_URL)
        #     else:
        #         row.append(springer_home_url + journal_homepage_relative_path)

    print(s, len(l) - f, len(l))

    headers.append("URL")
    df = pd.DataFrame.from_records(l, columns=headers)
    df.to_excel("combined_springer_journal_homepage_urls.xlsx", index=False)
