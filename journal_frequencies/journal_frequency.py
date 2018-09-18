import requests, re
from bs4 import BeautifulSoup
import pandas as pd
from sys import argv

# Scrapes the publishing frequency of all journals listed on the SSCI or A&HCI
# master list webpage and returns this information as a list of lists. Note that
# if a given journal does not have its publishing frequency listed, it is
# assigned a frequency value of "Not Listed" in the returned data structure.
#   @param url the URL to the first webpage of the SSCI or A&HCI master page
#   @return journals_list, a list of lists containing all the journals from
#       the master list website where each element is of the form:
#           [ISSN, journal_name, frequency]
def scrape_frequencies(url):
    source = requests.get(url)
    soup = BeautifulSoup(source.content, 'lxml')

    total_journals = int(''.join(filter(str.isdigit, soup.p.text)))

    frequencies, ISSNs, journals = [], [], []
    page = 1

    while(len(journals) < total_journals):
        if(page != 1): # prevents requesting the first page again
            source = requests.get(url)
            soup = BeautifulSoup(source.content, 'lxml')

        # find all instances of journal publishing frequency and ISSN containers
        frequency_and_ISSN = re.findall(r'</dt>\n(.+?)<', str(soup.dl))

        # find the journal publishing frequency and ISSN
        for journal in frequency_and_ISSN:
            info = journal.lstrip(" ").split(" ")
            if len(info) == 3:
                frequencies.append(info[0])
                ISSNs.append(info[2])
            elif len(info) == 2 and info[0].find("ISSN") != -1:
                frequencies.append("Not Listed")
                ISSNs.append(info[1])

        # find the journal name
        for dt_tag in soup.find_all('dt'):
            journals.append(dt_tag.string[dt_tag.string.find(" ")+1:])

        page += 1
        url = url[:-1] + str(page)

    # make list of lists out of the three lists with each list = [ISSN, journal_name, frequency]
    journals_list = []
    for i in range(len(ISSNs)):
        journals_list.append([ISSNs[i], journals[i], frequencies[i]])
    return journals_list

# Reads all the journals from the .xlsx SSCI or A&HCI master list and matches
# them to the journals scraped from the respective master list webpage in order
# to obtain their publishing frequency. The results are written to another .xlsx
# file. Note that if a journal from the .xlsx list does not match a journal from
# the website, or the journal does not have a frequency listed on the website,
# then the journal is assigned a frequency value of "Not Listed".
#   @return journals_list, a list of lists containing all the journals from
#       the master list website where each element is of the form:
#           [ISSN, journal_name, frequency]
#   @param read_file the SSCI or A&HCI .xlsx master list to be read from
#   @param write_file the file to which the master list along with journal
#       publishing frequencies should be written to
def write_frequencies(journals_list, read_file, write_file):
    # read xlsx file into a list so the publishing frequencies can be added and
    # later written to another xlsx file
    sheet = pd.read_excel(read_file, header=None)
    l = pd.Series.tolist(sheet)
    headers = l.pop(0)
    headers.append("Frequency")

    # loop through each journal from the master list
    for row in l:
        found = False
        # iterate through each journal remaining in journals_list
        for i in range(len(journals_list)):
            # attempt to match on ISSN
            if row[2] == journals_list[i][0]:
                row.append(journals_list[i][2])
                del journals_list[i]
                found = True
                break
            # attempt to match on journal name
            elif(journals_list[i][1].lower() == row[0].lower()):
                row.append(journals_list[i][2])
                del journals_list[i]
                found = True
                break
        # if no match was found, then the journal must not exist on the website
        if not found:
            row.append("Not Listed")

    # create a pandas dataframe from the existing excel file with the journal
    # publishing frequencies added to it
    df = pd.DataFrame.from_records(l, columns=headers)

    # write dataframe to excel file
    df.to_excel(write_file, index=False)

# This program may be run with or without command line arguments. If run without
#  command line arguments, the SSCI and A&HCI Excel master lists must be stored
#  in the current directory and named publist_ssci.xlsx and publist_ahci.xlsx
#  respectively. Note this method assumes that the user wants the new data to
#  written to new Excel files (ssci_frequencies.xlsx and ahci_frequencies.xlsx).
#  If run with command line arguments, then 6 pieces of information are required,
#  in the following order:
#   1. URL to the first webpage of the SSCI master list,
#   2. the SSCI Excel master list,
#   3. the Excel file for the updated SSCI information to be written to,
#   4. URL to the first webpage of the A&HCI master list,
#   5. the A&HCI Excel master list, and
#   6. the Excel file for the updated A&HCI information to be written to.
#  If the number of command line arguments provided is not 0 or 6, then a message
#  detailing the proper usage of the program will be printed to the command line.
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