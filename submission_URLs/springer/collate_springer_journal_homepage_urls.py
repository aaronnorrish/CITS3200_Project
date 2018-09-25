import pandas as pd
import math

sheet1 = pd.read_excel("springer_journal_homepage_urls.xlsx", header=None)
springer_urls = pd.Series.tolist(sheet1)
headers = springer_urls.pop(0)

sheet2 = pd.read_excel("springer_link_journal_homepage_urls.xlsx", header=None)
springer_link_urls = pd.Series.tolist(sheet2)
springer_link_urls.pop(0)

s = 0
for i in range(len(springer_urls)):
    try:
        if math.isnan(float(springer_urls[i][6])): # no url in the springer xlsx
            try:
                math.isnan(springer_link_urls[i][6])
            except:
                print(springer_urls[i][0])
                springer_urls[i][6] = springer_link_urls[i][6].replace("link.","")
                s+=1
    except:
        pass

print(s, len(springer_urls))

df = pd.DataFrame.from_records(springer_urls, columns=headers)
df.to_excel("collated_springer_journal_homepage_urls.xlsx", index=False)
