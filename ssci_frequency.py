import requests
import re
from bs4 import BeautifulSoup

url = "http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=SS&mode=print&Page=1"
# url = "http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=H&mode=print&Page=1"
source = requests.get(url)
soup = BeautifulSoup(source.content, 'lxml')

# could tally up scraped journals and stop execution after this amount has been reached
# or stop execution if 0 journals are scraped on an iteration
total_journals = ''.join(filter(str.isdigit, soup.p.text))


frequency_and_ISSN = re.findall(r'</dt>\n(.+?)<', str(soup.dl))
frequencies = []
ISSNs = []
for journal in frequency_and_ISSN:
    info = journal.lstrip(" ").split(" ")
    # print(info)
    # sometimes frequency not listed, what to do if ISSN not listed???
    if len(info) == 3:
        frequencies.append(info[0])
        ISSNs.append(info[2])
    elif len(info) == 2 and info[0].find("ISSN") != -1: # assuming we don't have "ISSN: <blank>", could be other reasons why info is len 2
        frequencies.append("Not Listed")
        ISSNs.append(info[1])

print(len(frequencies), len(ISSNs))

journals = []
for dt_tag in soup.find_all('dt'):
    journals.append(dt_tag.string[dt_tag.string.find(" ")+1:])
print(len(journals))

# make dictionary out of the three lists with key = ISSN, value = [journal_name, frequency]
