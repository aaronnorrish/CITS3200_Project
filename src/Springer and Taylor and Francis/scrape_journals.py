from journal_frequency import *
from taylor_and_francis import *
from springer import *
from helper_functions import *
from os.path import isfile
from sys import argv

# Main program which first tries to obtain the journal publishing frequencies as
# listed on the Clarivate website, then obtains the instructions for authors and
# homepages for journals published by Springer and Taylor and Francis. If journal
# frequencies were able to be obtained, the final output will be written to
# "master_URLs_frequencies.xlsx", otherwise "master_URLs.xlsx". This program will
# work if one of these files already exists; it will try to find any journal URLs
# that have not already been obtained. Once the program has started to search for
# journal URLs (the program will print "Begin scraping journal URLs" to the command
# line) execution may be stopped by pressing Control-C. The program will write
# the data it has found so far into an Excel file before terminating. This
# functionality has been built-in to allow the user to stop/re-run the program
# when convenient and so does not require the program to be executed in one go.
# Similarly, there is the option to pass command line arguments denoting the start
# and end positions of the journals in the spreadsheet for which the user would
# like the program to execute over. This allows the program to be run in chunks.
# This program requires that the A&HCI and SSCI master lists are stored as .xlsx
# files in the src directory, and are named "publist_ahci.xlsx" and "publist_ssci.xlsx"
# respectively. These files must contain six columns: [Journal Title], [Publisher],
# [ISSN], [E-ISSN], [Country], [Language] in that order.
if __name__ == '__main__':
    frequencies = False
    ifa_col = 8
    homepage_col = 9
    row_length = 10

    # check if an Excel file containing journal URLs (with the journal frequencies)
    # exists. If not, try to create a new spreadsheet containing the journal
    # frequencies.
    if not isfile("master_URLs_frequencies.xlsx"):
        get_journal_frequencies("http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=SS&mode=print&Page=1", "publist_ssci.xlsx", "ssci_frequencies.xlsx")
        get_journal_frequencies("http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=H&mode=print&Page=1", "publist_ahci.xlsx", "ahci_frequencies.xlsx")
        if isfile("ahci_frequencies.xlsx") and isfile("ssci_frequencies.xlsx"):
            merge_frequencies("ahci_frequencies.xlsx", "ssci_frequencies.xlsx", "master_URLs_frequencies.xlsx")
    # if such a file already exists, or it was successfully created initialise the
    # appropriate variables.
    if isfile("master_URLs_frequencies.xlsx"):
        frequencies = True
        ifa_col = 9
        homepage_col = 10
        row_length = 11
    # otherwise, if no Excel file containing just journal URLs (no frequencies)
    # exists, create a new spreadsheet
    elif not isfile("master_URLs.xlsx"):
        merge_without_frequencies("publist_ahci.xlsx", "publist_ssci.xlsx", "master_URLs.xlsx")

    # read the spreadsheet
    if frequencies:
        spreadsheet = pd.read_excel("master_URLs_frequencies.xlsx", header=None)
    else:
        spreadsheet = pd.read_excel("master_URLs.xlsx", header=None)

    spreadsheet_list = pd.Series.tolist(spreadsheet)
    headers = spreadsheet_list.pop(0)

    # determine what section of the journals the user would like the program to
    # be run on. By default, it will run over the whole spreadsheet. If a command
    # line argument is incorrect, print the errror to the command line and stop
    # execution.
    start_pos = 0
    end_pos = len(spreadsheet_list)
    error = False
    interrupt = False
    if len(argv) == 2:
        if int(argv[1]) >= 0 and int(argv[1]) < end_pos:
            start_pos = int(argv[1])
        else:
            error = True
            print("ERROR: the starting row index must be greater than or equal to zero and less than the total number of rows")
    elif len(argv) == 3:
        if int(argv[1]) >= 0 and int(argv[1]) < end_pos:
            start_pos = int(argv[1])
        else:
            error = True
            print("ERROR: the starting row index must be greater than or equal to zero and less than the total number of rows")
        if int(argv[2]) > 0 and int(argv[2]) <= end_pos:
            end_pos = int(argv[2])
        else:
            error = True
            print("ERROR: the ending row index must be greater than zero and less than or equal to the total number of rows")
    elif len(argv) > 3:
        error = True
        print("usage: python3 scrape_journals.py <starting_index> <ending_index>")

    if not error:
        # keep track of how many journal URLs have not yet been obtained
        previous_remaining = -1
        remaining = len(spreadsheet_list) + 1 # this can be any number != previous_remaining. This is so the below while loop executes at least twice.

        # keeps track whether at least one journal has been obtained
        obtained_journal = False

        print("Begin scraping journal URLs...")

        try:
            # keep iterating over the spreadsheet until the number of journals
            # whose URLs have not been obtained does not change
            while(previous_remaining != remaining):
                p, b_t,b_s,t,s = 0,0,0,0,0
                for i in range(start_pos, end_pos):
                    # if both the instructions for authors and journal homepage have
                    # been retrieved, continue to the next journal
                    if len(spreadsheet_list[i]) == row_length and str(spreadsheet_list[i][ifa_col]) != "nan" and str(spreadsheet_list[i][homepage_col]) != "nan":
                        continue

                    URL = (None, None)

                    # try to get the URL from the Taylor and Francis website
                    URL = taylor_and_francis(spreadsheet_list[i][0], str(spreadsheet_list[i][2]), str(spreadsheet_list[i][3]), 18.0)
                    if URL[0] is not None or URL[1] is not None:
                        obtained_journal = True
                        b_t+=1
                        # only change the journal's URLs if they have not been
                        # stored already
                        if len(spreadsheet_list[i]) == row_length:
                            if str(spreadsheet_list[i][ifa_col]) == "nan":
                                spreadsheet_list[i][ifa_col] = URL[0]
                            if str(spreadsheet_list[i][homepage_col]) == "nan":
                                spreadsheet_list[i][homepage_col] = URL[1]
                        elif len(spreadsheet_list[i]) == row_length-1:
                            if str(spreadsheet_list[i][ifa_col]) == "nan":
                                spreadsheet_list[i][ifa_col] = URL[0]
                            spreadsheet_list[i].append(URL[1])
                        else:
                            spreadsheet_list[i].append(URL[0])
                            spreadsheet_list[i].append(URL[1])

                    # if no journal was able to be obtained from the Taylor and
                    # Francis website, try to get the URL from the Springer website
                    if URL[0] is None and URL[1] is None:
                        URL = springer(spreadsheet_list[i][0], str(spreadsheet_list[i][2]), str(spreadsheet_list[i][3]), 18.0)
                        if URL[0] is not None or URL[1] is not None:
                            obtained_journal = True
                            b_s+=1
                            # only change the journal's URLs if they have not been
                            # stored already
                            if len(spreadsheet_list[i]) == row_length:
                                if str(spreadsheet_list[i][ifa_col]) == "nan":
                                    spreadsheet_list[i][ifa_col] = URL[0]
                                if str(spreadsheet_list[i][homepage_col]) == "nan":
                                    spreadsheet_list[i][homepage_col] = URL[1]
                            elif len(spreadsheet_list[i]) == row_length-1:
                                if str(spreadsheet_list[i][ifa_col]) == "nan":
                                    spreadsheet_list[i][ifa_col] = URL[0]
                                spreadsheet_list[i].append(URL[1])
                            else:
                                spreadsheet_list[i].append(URL[0])
                                spreadsheet_list[i].append(URL[1])

                previous_remaining = remaining
                remaining = calculate_remaining(spreadsheet_list, frequencies)

        except KeyboardInterrupt:
            interrupt = True
            print("\nInterrupt received, writing to file...")

        if not interrupt:
            print("Finished scraping journal URLs, writing to file...")

        # if at least one journal was able to be obtained, and the starting spreadsheet
        # was new, append the Instructions for Authors and Journal Homepage columns
        # to the spreadsheet.
        if obtained_journal:
            if not "Instructions for Authors" in headers:
                headers.append("Instructions for Authors")
                headers.append("Journal Homepage")

        df = pd.DataFrame.from_records(spreadsheet_list, columns=headers)
        if frequencies:
            df.to_excel("master_URLs_frequencies.xlsx", index=False)
        else:
            df.to_excel("master_URLs.xlsx", index=False)
