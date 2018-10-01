import requests, re
from bs4 import BeautifulSoup
import pandas as pd

# TODO need to remove print statements
# enclose getting source in try/except
# try/except for result-items?

sheet = pd.read_excel("springer_no_duplicates.xlsx", header=None)
l = pd.Series.tolist(sheet)
headers = l.pop(0)

home_url = "https://springer.com"
search_url_start = "https://www.springer.com/gp/search?query="
search_url_end = "&submit=Submit"

s = 0
for row in l:
    found = False
    # search_term = re.sub('[^ a-zA-Z0-9]', '', row[0])
    search_term = row[0].replace("&", "and")
    # search_term = row[0].replace("&", "%26")
    # print(search_term)
    search_url = search_url_start + search_term.replace(" ","+") + search_url_end
    # print(search_url)
    source = requests.get(search_url)
    soup = BeautifulSoup(source.content, 'lxml')
    for div_tag in soup.find_all("div", {"class":"result-item"}):
        if div_tag.small.text == "Journal":
            journal_url = home_url + div_tag.a.get('href')
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
                    print("ERROR: unable to get ISSN for ", row[0])
    if not found:
        print("could not find: ", row[0])

# had a timeout at scientometrics journal
print(s, len(l))

headers.append("URL")
df = pd.DataFrame.from_records(l, columns=headers)
df.to_excel("springer_journal_homepage_urls.xlsx", index=False)
