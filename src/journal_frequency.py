import requests
from bs4 import BeautifulSoup
import pandas as pd
from sys import argv
import urllib3

# Scrapes the publishing frequency of all journals listed on the SSCI or A&HCI
# master list webpage and returns this information as a list of lists. Note that
# if a given journal does not have its publishing frequency listed, it is
# assigned a frequency value of "Not Listed" in the returned data structure.
# If there is an error parsing the HTML, this function will print an error
# statement to the command line and return None.
#   @param url the URL to the first webpage of the SSCI or A&HCI master page
#   @param time_limit the time limit for the URL request
#   @return journals_list, a list of lists containing all the journals from
#       the master list website where each element is of the form:
#           [ISSN, journal_name, frequency]
#       if there is a problem parsing the HTML, return None.
def scrape_frequencies(url, time_limit):

    source = requests.get(url, timeout=time_limit)
    soup = BeautifulSoup(source.content, 'lxml')

    # # if this page does not exist return None TODO
    # try:
    #     if soup.head.text.lower() == "404 not found" or soup.head.text.lower() == "not found":
    #         return None
    # except AttributeError:
    #     pass

    total_journals = int(''.join(filter(str.isdigit, soup.p.text)))

    frequencies, ISSNs, journals = [], [], []
    page = 1

    # retrieve all journals
    while(len(journals) < total_journals):
        if(page != 1): # prevents requesting the first page again
            source = requests.get(url, timeout=time_limit)
            soup = BeautifulSoup(source.content, 'lxml')

        # find all instances of the journal name containers
        journal_names = soup.dl.find_all("strong")

        # separate HTML into journal containers
        soup_stripped = str(soup.dl).replace("\n","").replace("<dl>","").replace("</dl>","")
        journals_HTML = soup_stripped.split("<dt>")

        # remove the empty string created from the split
        if journals_HTML[0] == "":
            journals_HTML.pop(0)

        # if the total number of journals does not equal the number of journal
        # names or if the number of journal names do not equal the number of
        # journals obtained from the HTML then something has gone wrong with
        # parsing the HTML
        if total_journals != len(journal_names) or len(journal_names) != len(journals_HTML):
            print("ERROR: UNABLE TO PARSE HTML")
            return None

        # find the journal publishing frequency and ISSN
        for journal in journals_HTML:
            # try to find the ISSN
            if journal.find("<br/>") != -1 and journal.find("<br/>", journal.find("<br/>")+len("<br/>")) != -1:
                ISSN = journal[journal.find("<br/>")+len("<br/>"):journal.find("<br/>", journal.find("<br/>")+len("<br/>"))]
                if ISSN[0:4].lower() == "issn":
                    ISSNs.append(ISSN[ISSN.find(" ")+1:].strip())
            else:
                ISSNs.append("none")

            # try to find the frequency
            if journal.find("</dt>") != -1 and journal.find("<br/>") != -1:
                frequencies.append(journal[journal.find("</dt>")+len("</dt>"):journal.find("<br/>")].strip())
            else:
                frequencies.append("Not Listed")

        # find the journal name
        for journal_name in journal_names:
            journals.append(journal_name.string[journal_name.string.find(" ")+1:])

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
                if journals_list[i][2] == "":
                    row.append("Not Listed")
                else:
                    row.append(journals_list[i][2])
                del journals_list[i]
                found = True
                break
            # attempt to match on journal name
            elif(journals_list[i][1].lower() == row[0].lower()):
                if journals_list[i][2] == "":
                    row.append("Not Listed")
                else:
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


# Retrieves and writes to a file the journal frequencies for a given master list.
#   @param url the URL to the first webpage of the SSCI or A&HCI master page
#   @param read_file the SSCI or A&HCI .xlsx master list to be read from
#   @param write_file the file to which the master list along with journal
def get_journal_frequencies(url, read_file, write_file):
    journals = None
    n_tries = 0
    # try to get the journal frequencies
    while(n_tries < 5):
        try:
            journals = scrape_frequencies(url, 24.0 + n_tries * 24.0)
            break
        except(requests.exceptions.RequestException, urllib3.exceptions.HTTPError, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.RequestError, urllib3.exceptions.TimeoutError, ValueError):
            n_tries += 1
    # if the journal frequencies were able to be obtained, write them to a file
    if journals != None:
        write_frequencies(journals, read_file, write_file)


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
        get_journal_frequencies("http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=SS&mode=print&Page=1", "publist_ssci.xlsx", "ssci_frequencies.xlsx")
        get_journal_frequencies("http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=H&mode=print&Page=1", "publist_ahci.xlsx", "ahci_frequencies.xlsx")
    elif(len(argv) == 7):
        get_journal_frequencies(argv[1], argv[2], argv[3])
        get_journal_frequencies(argv[4], argv[5], argv[6])
    else:
        print("usage: python3 journal_frequency.py <ssci_url> <read_ssci_journals.xlsx> <write_ssci_journals.xlsx> <ahci_url> <read_ahci_journals.xlsx> <write_ahci_journals.xlsx>")
