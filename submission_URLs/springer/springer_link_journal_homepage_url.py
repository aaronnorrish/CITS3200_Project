import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata

def remove_accents(string):
    nfkd_form = unicodedata.normalize('NFKD', string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


sheet = pd.read_excel("springer_no_duplicates.xlsx", header=None)
l = pd.Series.tolist(sheet)
headers = l.pop(0)

home_url = "https://link.springer.com"
search_url_start = "https://link.springer.com/search?query="
search_url_end = "&facet-content-type=%22Journal%22"

s = 0
for row in l:
    search_url = search_url_start + row[2] + search_url_end
    source = requests.get(search_url)
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
            row.append(home_url + journal_path)
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
                row.append(home_url + journal_path)
                s+=1
                break
            else:
                print("unable to match: ", soup.find("div", {"id":"issn"}), row[0], row[2])

                # e_issn = issn_tag.find("span", {"class":"eissn"}).split(" ")[0]
                # if print_issn == row[2]:
                #     row.append(home_url + journal_path)
                # elif e_issn == row[3]:
                #     row.append(home_url + journal_path)
                # except:
                #     print(journal_path, journal_name, row[2])

        # if journal name matches; break
        # a_tag = journal.find('a')
        # print(a_tag.get('href'), a_tag.text) # assumes that each list object only has one href tag
        # print()

    # print(row[0], row[2])
print(s, len(l), s/len(l))
headers.append("URL")
df = pd.DataFrame.from_records(l, columns=headers)
df.to_excel("springer_link_journal_homepage_urls.xlsx", index=False)
