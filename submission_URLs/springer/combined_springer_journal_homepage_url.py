import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

# TODO need to remove print statements
# enclose getting source in try/except
# try/except for result-items?

def remove_accents(string):
    nfkd_form = unicodedata.normalize('NFKD', string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

sheet = pd.read_excel("springer_no_duplicates.xlsx", header=None)
l = pd.Series.tolist(sheet)
headers = l.pop(0)

springer_home_url = "https://springer.com"
springer_search_url_start = "https://www.springer.com/gp/search?query="
springer_search_url_end = "&submit=Submit"

springer_link_home_url = "https://link.springer.com"
springer_link_search_url_start = "https://link.springer.com/search?query="
springer_link_search_url_end = "&facet-content-type=%22Journal%22"

s = 0
for row in l:
    # have functions for springer and springer link ?
    found = False
    # search_term = re.sub('[^ a-zA-Z0-9]', '', row[0])
    search_term = row[0].replace("&", "and")
    # search_term = row[0].replace("&", "%26")
    # print(search_term)
    springer_search_url = springer_search_url_start + search_term.replace(" ","+") + springer_search_url_end
    # print(search_url)
    source = requests.get(springer_search_url)
    soup = BeautifulSoup(source.content, 'lxml')
    for div_tag in soup.find_all("div", {"class":"result-item"}):
        if div_tag.small.text == "Journal":
            journal_url = springer_home_url + div_tag.a.get('href')
            journal_source = requests.get(journal_url)
            journal_soup = BeautifulSoup(journal_source.content, 'lxml')
            try:
                ISSN = journal_soup.find("span", {"wicketpath":"content_basic_productDescriptionContainer_productDescription_issnPrint_content"}).text
                if(ISSN == row[2]):
                    # print(row[0])
                    row.append(journal_url)
                    s+=1
                    found = True
                    break
            except AttributeError:
                try:
                    ISSN = journal_soup.find("span", {"wicketpath":"content_basic_productDescriptionContainer_productDescription_issnElectronic_content"}).text
                    if(ISSN == row[3]):
                        # print(row[0])
                        row.append(journal_url)
                        s+=1
                        found = True
                        break
                except AttributeError:
                    continue
                    # print("ERROR: unable to get ISSN for ", row[0])
    if not found:
        # print("could not find: ", row[0])
        springer_link_search_url = springer_link_search_url_start + row[2] + springer_link_search_url_end
        source = requests.get(springer_link_search_url)
        soup = BeautifulSoup(source.content, 'lxml')

        journals = soup.findAll("li", {"class":"has-cover"})
        if len(journals) == 0:
            print("no seach results: ", row[0], row[2])
        for journal in journals:
            # for link in :
            a_tag = journal.find("div", {"class":"text"}).find('a') # assumes each entry has text div
            journal_path = a_tag.get('href')
            journal_name = a_tag.text.replace(",", "").lower()
            if row[0].lower().find(journal_name) != -1 or journal_name.find(row[0].lower()) != -1:
                row.append(springer_home_url + journal_path)
                s += 1
                break
            else: # the search is done on the ISSN so could just do it anyway
                # try:
                # need to open up link to check this
                # print_issn = issn_tag.find("span", {"class":"pissn"}).split(" ")[0]
                j = remove_accents(row[0].lower().replace("the ", "").replace(",","").replace("&", "and"))
                j = re.sub('[^A-Za-z0-9]+', '', j)
                journal_name = remove_accents(journal_name.lower().replace("the ", "").replace("&", "and"))
                journal_name = re.sub('[^A-Za-z0-9]+', '', journal_name)
                if(j == journal_name or j.find(journal_name) != -1 or journal_name.find(j) != -1):
                    row.append(springer_home_url + journal_path)
                    s+=1
                    break
                else:
                    print("unable to match: ", soup.find("div", {"id":"issn"}), row[0], row[2])


# had a timeout at scientometrics journal
print(s, len(l))

headers.append("URL")
df = pd.DataFrame.from_records(l, columns=headers)
df.to_excel("combined_springer_journal_homepage_urls.xlsx", index=False)
