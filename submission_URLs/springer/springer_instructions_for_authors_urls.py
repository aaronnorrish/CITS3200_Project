import requests, re
from bs4 import BeautifulSoup
import pandas as pd

sheet = pd.read_excel("collated_springer_journal_homepage_urls.xlsx", header=None)
l = pd.Series.tolist(sheet)
headers = l.pop(0)

f,s,a = 0,0,0
for row in l:
    url = row[6]
    try: # need to change this, is supposed to check whether row[6] is NaN not if can get webpage
        source = requests.get(url)
        soup = BeautifulSoup(source.content, 'lxml')
    except:
        print("no url inputted: ", row[0])
        continue
    try:
        found_url = False
        for ul_tag in soup.find_all("ul", {"class":"listToOpenLayer"}):
            for li_tag in ul_tag.find_all("li", {"class":"listItemToOpenLayer"}):
                # need to make this not case sensitive
                title = li_tag.a.span.text.lower()
                if title.find("instructions for authors")!=-1 or title.find("instructions to authors")!=-1 or title.find("author guidelines")!=-1 or title.find("guidelines for submitters")!=-1 or title.find("hinweise für autoren")!=-1:
                    # then this is the correct list element
                    # sometimes the link is to a PDF
                    # this line may be a problem if there is more than one of these div tags or a tags
                    try:
                        guidelines_url = li_tag.find("div", {"class":"wideLayer portletLayer"}).find("div", {"class":"clearfix"}).a.get('href').replace("print_view=true&","")
                        if guidelines_url is not None:
                            row.append(guidelines_url)
                            s+=1
                            found_url = True
                            break
                    except:
                        try:
                            print("trying a tag for: ", row[0])
                            guidelines_url = li_tag.a.get('href')
                            print(guidelines_url)
                            if guidelines_url is not None:
                                row.append(guidelines_url)
                                a+=1
                                found_url = True
                                break
                        except:
                            print("unable to get instructions for authors link for: ", row[0])
            if found_url:
                break
    except:
        # executing for EPJ Data Science -> "http://www.epjdatascience.com/authors/instructions", European Transport Research Review
        # need to investigate how the HTML is structured
        print("no ifa tag: ", row[0])
        f+=1
        continue

print(f, s, a, len(l))
for row in l:
    if len(row) == 9:
        print(row)
headers.append("Instructions for Authors URL")
df = pd.DataFrame.from_records(l, columns=headers)
df.to_excel("springer_instructions_for_authors_urls.xlsx", index=False)
