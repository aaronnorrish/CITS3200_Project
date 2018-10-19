import pandas as pd

def determine_fresh_sheet(master_file):
    master_df = pd.read_excel(master_file, header=None)
    master_list = pd.Series.tolist(master_df)
    headers = master_list.pop(0)
    if headers[len(headers)-1] == "URL":
        return False
    return True

# Calculates the remaining number of journals whose instructions for authors
# webpage have not yet been obtained.
#   @param spreadsheet_list a spreadsheet represented as a list
#   @param frequencies a boolean denoting whether the spreadsheet includes
#       journal frequencies (True) or not (False)
#   @return the number of journals whose instructions for authors webpage
#       have not yet been obtained.
def calculate_remaining(spreadsheet_list, frequencies):
    remaining = 0
    for row in spreadsheet_list:
        if frequencies and (len(row) < 11 or str(row[10]) == "nan"):
            remaining += 1
        elif not frequencies and (len(row) < 10 or str(row[9]) == "nan"):
            remaining += 1
    return remaining

# Merges the A&HCI and SSCI excel files into a single excel file. This should
#   only be used if the A&HCI and SSCI files do not have the journal frequency
#   information appended to them.
#   @param ahci_file the path to the A&HCI excel file
#   @param ssci_file the path to the SSCI excel file
#   @param master_file the desired path for the merged list.
def merge_without_frequencies(ahci_file, ssci_file, master_file):
    ahci_df = pd.read_excel(ahci_file, header=None)
    ahci_list = pd.Series.tolist(ahci_df)
    headers = ahci_list.pop(0)
    headers.append("A&HCI")
    headers.append("SSCI")

    # all journals belong to A&HCI
    for row in ahci_list:
        row.append("Yes")

    ssci_df = pd.read_excel(ssci_file, header=None)
    ssci_list = pd.Series.tolist(ssci_df)
    ssci_list.pop(0)

    # add journals from SSCI list
    for ssci_row in ssci_list:
        found = False
        # see if this journal occurs in the A&HCI list
        for ahci_row in ahci_list:
            # if so append "Yes" - belongs to the SSCI as well
            if str(ssci_row[2]) == str(ahci_row[2]):
                ahci_row.append("Yes")
                found = True
                break
        # otherwise append this journal as a new row
        if not found:
            ssci_row.append("No")
            ssci_row.append("Yes")
            ahci_list.append(ssci_row)

    # find each journal that only occurs in the A&HCI and append "No" - does not
    # belong to the SSCI
    for ahci_row in ahci_list:
        if len(ahci_row) == 7:
            ahci_row.append("No")

    df = pd.DataFrame.from_records(ahci_list, columns=headers)
    df.to_excel(master_file, index=False)

# Merges the A&HCI and SSCI excel files (that contain a journal frequency column)
#   into a single excel file. This should only be used if the A&HCI and SSCI files
#   have the journal frequency information appended to them.
#   @param ahci_file the path to the A&HCI excel file
#   @param ssci_file the path to the SSCI excel file
#   @param master_file the desired path for the merged list.
def merge_frequencies(ahci_file, ssci_file, master_file):
    ahci_df = pd.read_excel(ahci_file, header=None)
    ahci_list = pd.Series.tolist(ahci_df)
    headers = ahci_list.pop(0)
    headers[6] = "A&HCI"
    headers.append("SSCI")
    headers.append("Frequency")

    # all journals belong to A&HCI
    for row in ahci_list:
        frequency = row[6]
        row[6] = "Yes"
        row.append(frequency)

    ssci_df = pd.read_excel(ssci_file, header=None)
    ssci_list = pd.Series.tolist(ssci_df)
    ssci_list.pop(0)

    # add journals from SSCI list
    for ssci_row in ssci_list:
        found = False
        # see if this journal occurs in the A&HCI list
        for ahci_row in ahci_list:
            # if so, add that it belongs to the SSCI as well
            if str(ssci_row[2]) == str(ahci_row[2]):
                frequency = row[7]
                ahci_row[7] = "Yes"
                ahci_row.append(frequency)
                found = True
                break
        # otherwise append this journal as a new row
        if not found:
            frequency = ssci_row[6]
            ssci_row[6] = "No"
            ssci_row.append("Yes")
            ssci_row.append(frequency)
            ahci_list.append(ssci_row)

    # find each journal that only occurs in the A&HCI and indicate that it only
    # belongs to the A&HCI list
    for ahci_row in ahci_list:
        if len(ahci_row) == 8:
            frequency = ahci_row[7]
            ahci_row[7] = "No"
            ahci_row.append(frequency)

    df = pd.DataFrame.from_records(ahci_list, columns=headers)
    df.to_excel(master_file, index=False)
