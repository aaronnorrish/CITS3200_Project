import requests, re
from bs4 import BeautifulSoup
import pandas as pd
from sys import argv

# Scrapes the publishing frequency of all journals listed on the SSCI or A&HCI
# master list webpage and returns this information as a dictionary. Note that
# if a given journal does not have its publishing frequency listed, it is
# assigned a frequency value of "Not Listed" in the returned dictionary.
#   @param url the URL to the first webpage of the SSCI or A&HCI master page
#   @return journals_dictionary, a dictionary containing all the journals from
#       the master list website where key = ISSN, value = (journal_name, frequency)
def scrape_frequencies(url):
    source = requests.get(url)
    soup = BeautifulSoup(source.content, 'lxml')

    # could tally up scraped journals and stop execution after this amount has been reached
    # or stop execution if 0 journals are scraped on an iteration
    total_journals = int(''.join(filter(str.isdigit, soup.p.text)))
    # print(total_journals) # for testing

    frequencies, ISSNs, journals = [], [], []
    page = 1
    missing = [] # for testing, can be removed later

    while(len(journals) < total_journals):
        if(page != 1): # prevents requesting the first page again
            source = requests.get(url)
            soup = BeautifulSoup(source.content, 'lxml')
        frequency_and_ISSN = re.findall(r'</dt>\n(.+?)<', str(soup.dl))
        for journal in frequency_and_ISSN:
            info = journal.lstrip(" ").split(" ")
            # print(info)
            # sometimes frequency not listed, what to do if ISSN not listed???
            if len(info) == 3:
                frequencies.append(info[0])
                ISSNs.append(info[2])
            elif len(info) == 2 and info[0].find("ISSN") != -1: # assuming we don't have "ISSN: <blank>", could be other reasons why info is len 2
                frequencies.append("Not Listed") # 14 have not listed
                missing.append(info[1])
                ISSNs.append(info[1])
                # could just not add to lists, depends whether this is useful information - probably not
        # print(len(frequencies), len(ISSNs)) # for testing

        for dt_tag in soup.find_all('dt'):
            journals.append(dt_tag.string[dt_tag.string.find(" ")+1:])
        # print(len(journals))

        page += 1
        url = url[:-1] + str(page)

    # following print statements are for testing
    # print(missing)
    # print(len(journals), len(frequencies), len(ISSNs))
    # print(len(set(journals)))

    # make dictionary out of the three lists with key = ISSN, value = (journal_name, frequency)
    journals_dictionary = dict(zip(ISSNs, zip(journals, frequencies)))
    # print(journals_dictionary)
    # print(len(journals_dictionary)) # for some reason this is missing one entry for SSCI
    return journals_dictionary

def write_frequencies(journals_dictionary, read_file, write_file):
    # read xlsx file into lists so the publishing frequencies can be added and wrote
    # to another xlsx file
    sheet = pd.read_excel(read_file, header=None)
    l = pd.Series.tolist(sheet)
    headers = l.pop(0)
    headers.append("Frequency")

    # n = 0
    for row in l:
        if row[2] in journals_dictionary:
            # n += 1
            if journals_dictionary[row[2]][1] != "Not Listed":
                row.append(journals_dictionary[row[2]][1])
            else:
                row.append("Not Listed")
            # print(journals_dictionary[row[2]][0], row[0], journals_dictionary[row[2]][0].lower() == row[0].lower())
        else:
            row.append("Not Listed")
            # print(row[2] in missing)
    df = pd.DataFrame.from_records(l, columns=headers)
    # print(df)
    df.to_excel(write_file, index=False)
    # print(n) #3201/3250 by ISSN, string
    # print(len(l))
    # print(l)

if __name__ == '__main__':
    if(len(argv) == 1):
        ssci_journals = scrape_frequencies("http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=SS&mode=print&Page=1")
        write_frequencies(ssci_journals, "publist_ssci.xlsx", "ssci_frequencies.xlsx")
        ahci_journals = scrape_frequencies("http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=H&mode=print&Page=1")
        write_frequencies(ahci_journals, "publist_ahci.xlsx", "ahci_frequencies.xlsx")
    elif(len(argv) == 7):
        ssci_journals = scrape_frequencies(argv[1])
        write_frequencies(ssci_journals, argv[2], argv[3])
        ahci_journals = scrape_frequencies(argv[4])
        write_frequencies(ahci_journals, argv[5], argv[6])
    else:
        print("usage: python3 journal_frequency.py <ssci_url> <read_ssci_journals.xlsx> <write_ssci_journals.xlsx> <ahci_url> <read_ahci_journals.xlsx> <write_ahci_journals.xlsx>")
