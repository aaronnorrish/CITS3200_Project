import pandas as pd
from os.path import isfile

# This is a program that merges the output Excel files produced by scrape_journals.py
# and url_scraper.py into a single Excel file.
if __name__ == '__main__':
    ifa_col = 8
    homepage_col = 9
    # check if the file produced by scrape_journals.py contains the journal
    # frequencies. If so, its columns will be in a different position.
    if isfile("master_URLs_frequencies.xlsx"):
        spreadsheet = pd.read_excel("master_URLs_frequencies.xlsx", header=None)
        frequencies = True
        ifa_col = 9
        homepage_col = 10
    elif isfile("master_URLs.xlsx"):
        spreadsheet = pd.read_excel("master_URLs.xlsx", header=None)

    spreadsheet_list = pd.Series.tolist(spreadsheet)
    headers = spreadsheet_list.pop(0)

    # open the file produced by url_scraper.py
    spreadsheet2 = pd.read_excel("../ResearchGate/journals.xlsx", header=None)
    spreadsheet_list2 = pd.Series.tolist(spreadsheet2)
    spreadsheet_list2.pop(0)

    # for each row in spreadsheet2 see if the corresponding row in spreadsheet
    # has URL information. If not, add this information.
    for row in spreadsheet_list2:
        for journal in spreadsheet_list:
            if journal[3] == row[3]:
                # if it is a Springer or Taylor and Francis journal only use the
                # URLs from spreadsheet_list2 if it is not listed in spreadsheet_list
                if row[3].lower().find("springer") != -1 or row[3].lower().find("taylor & francis") != -1 or row[3][1].lower().find("taylor and francis") != -1:
                    if str(journal[ifa_col]) == "nan" and str(row[7]) != "nan":
                        journal[ifa_col] = row[7]
                    if str(journal[homepage_col]) == "nan" and str(row[8]) != "nan":
                        journal[homepage_col] = row[8]
                        break
                # otherwise if the URL exists in spreadsheet_list2, add it to
                # spreadsheet_list
                else:
                    if str(row[7]) != "nan":
                        journal[ifa_col] = row[7]
                    if str(row[8]) != "nan":
                        journal[homepage_col] = row[8]
                        break

    df = pd.DataFrame.from_records(spreadsheet_list, columns=headers)
    df.to_excel("journal_URLs.xlsx", index=False)
