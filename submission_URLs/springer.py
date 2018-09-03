import requests, re
from bs4 import BeautifulSoup
import pandas as pd

sheet = pd.read_excel("springer.xlsx", header=None)
l = pd.Series.tolist(sheet)
headers = l.pop(0)

search_url_start = "https://link.springer.com/search?query="
search_url_end = "&facet-content-type=%22Journal%22"

s = 0
for row in l:
    search_url = search_url_start + row[2] + search_url_end
    source = requests.get(search_url)
    soup = BeautifulSoup(source.content, 'lxml')

    journals = soup.findAll("li", {"class":"has-cover"})
    if len(journals) != 1:
        print(row[0], row[2], len(journals))
    for journal in journals:
        # for link in :
        a_tag = journal.find("div", {"class":"text"}).find('a') # assumes each entry has text div
        journal_path = a_tag.get('href')
        journal_name = a_tag.text.replace(",", "").lower()
        if row[0].lower().find(journal_name) != -1 or journal_name.find(row[0].lower()) != -1:
            s += 1
            break
        else:
            journal_name = journal_name.replace("and", "&").replace(":", "-")
            if row[0].lower().find(journal_name) != -1 or journal_name.find(row[0].lower()) != -1:
                s += 1
                break
            else:
                print(journal_path, journal_name, row[2])

        # if journal name matches; break
        # a_tag = journal.find('a')
        # print(a_tag.get('href'), a_tag.text) # assumes that each list object only has one href tag
        # print()

    # print(row[0], row[2])
print(s, len(l), s/len(l))
