from journal_frequency import *
from taylor_and_francis import *
from springer import *
from merge_files import *
from helper_functions import *
from os.path import isfile


if __name__ == '__main__':
    fresh_spreadsheet = True
    master = False
    frequencies = False
    found_file = False
    if isfile("master_URLs_frequencies.xlsx"):
        frequencies = True
        master = True
        found_file = True
    # maybe move this below
    elif isfile("master_URLs.xlsx"):
        # fresh_spreadsheet = determine_fresh_sheet("publist_master.xlsx")
        frequencies = False
        master = True
        found_file = True
    # think more about this
    elif not isfile("master_frequencies.xlsx"):
        get_journal_frequencies("http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=SS&mode=print&Page=1", "ssci.xlsx", "ssci_frequencies.xlsx")
        get_journal_frequencies("http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=H&mode=print&Page=1", "ahci.xlsx", "ahci_frequencies.xlsx")
        if isfile("ahci_frequencies.xlsx") and isfile("ssci_frequencies.xlsx"):
            merge_frequencies("ahci_frequencies.xlsx", "ssci_frequencies.xlsx", "master_frequencies.xlsx")
            # cols = 9
            frequencies = True
            found_file = True
    elif isfile("master_frequencies.xlsx"):
        frequencies = True
        found_file = True
    # if master frequencies exists
    # elif isfile("master_frequencies.xlsx"):
    if not found_file and not isfile("publist_master.xlsx"):
        merge_without_frequencies("ahci.xlsx", "ssci.xlsx", "publist_master.xlsx")
        # cols = 8
        frequencies = False


    # need to consider starting with a fresh spreadsheet v previously calculated
    # len 6 if no frequencies, 7 w/ frequencies, 8 w URLs

    if frequencies:
        if not master:
            spreadsheet = pd.read_excel("master_frequencies.xlsx", header=None)
        else:
            spreadsheet = pd.read_excel("master_URLs_frequencies.xlsx", header=None)
    else:
        if not master:
            spreadsheet = pd.read_excel("publist_master.xlsx", header=None)
        else:
            spreadsheet = pd.read_excel("master_URLs.xlsx", header=None)

    spreadsheet_list = pd.Series.tolist(spreadsheet)
    headers = spreadsheet_list.pop(0)
    if not master:
        headers.append("URL")


    previous_remaining = -1
    remaining = len(spreadsheet_list) + 1 # calc remaining

    while(previous_remaining != remaining):
        p, b_t,b_s,t,s = 0,0,0,0,0
        for i in range(len(spreadsheet_list)):
            if frequencies and len(spreadsheet_list[i]) == 10 and spreadsheet_list[i][9] != "nan":
                continue
            elif not frequencies and len(spreadsheet_list[i]) == 9 and spreadsheet_list[i][8] != "nan":
                continue

            URL = None
            if(spreadsheet_list[i][1].lower().find("taylor & francis") != -1 or spreadsheet_list[i][1].lower().find("taylor and francis") != -1):
                t+=1
                URL = taylor_and_francis(spreadsheet_list[i][0], str(spreadsheet_list[i][2]), str(spreadsheet_list[i][3]), 18.0)
                if URL is not None:
                    b_t+=1
                    spreadsheet_list[i].append(URL)
                # else:
                #     print(spreadsheet_list[i][0], spreadsheet_list[i][1])

            elif(spreadsheet_list[i][1].lower().find("springer") != -1):
                s+=1
                URL = springer(spreadsheet_list[i][0], str(spreadsheet_list[i][2]), str(spreadsheet_list[i][3]), 18.0)
                # print(URL)
                if URL is not None:
                    b_s+=1
                    spreadsheet_list[i].append(URL)
                # else:
                #     print(spreadsheet_list[i][0], spreadsheet_list[i][1])
        previous_remaining = remaining
        remaining = calculate_remaining(spreadsheet_list, frequencies)
        print(previous_remaining, remaining)

    # TODO if internet cuts out no URLs will be added so df will only have 6 rows -> wont write
    # previous remaining calc not working

    df = pd.DataFrame.from_records(spreadsheet_list, columns=headers)
    if frequencies:
        df.to_excel("master_URLs_frequencies.xlsx", index=False)
    else:
        df.to_excel("master_URLs.xlsx", index=False)
