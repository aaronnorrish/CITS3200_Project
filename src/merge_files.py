import pandas as pd

def merge_without_frequencies(ahci_file, ssci_file, master_file):
    # starting files have no appended information
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

    for ssci_row in ssci_list:
        found = False
        for ahci_row in ahci_list:
            if str(ssci_row[2]) == str(ahci_row[2]):
                ahci_row.append("Yes")
                found = True
                break
        if not found:
            ssci_row.append("No")
            ssci_row.append("Yes")
            ahci_list.append(ssci_row)

    for ahci_row in ahci_list:
        if len(ahci_row) == 7:
            ahci_row.append("No")

    df = pd.DataFrame.from_records(ahci_list, columns=headers)
    df.to_excel(master_file, index=False)

def merge_frequencies(ahci_file, ssci_file, master_file):
    # starting files have no appended information
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

    # find journals contained in both master lists
    for ssci_row in ssci_list:
        found = False
        for ahci_row in ahci_list:
            if str(ssci_row[2]) == str(ahci_row[2]):
                frequency = row[7]
                ahci_row[7] = "Yes"
                ahci_row.append(frequency)
                found = True
                break
        if not found:
            frequency = ssci_row[6]
            ssci_row[6] = "No"
            ssci_row.append("Yes")
            ssci_row.append(frequency)
            ahci_list.append(ssci_row)

    for ahci_row in ahci_list:
        if len(ahci_row) == 8:
            frequency = ahci_row[7]
            ahci_row[7] = "No"
            ahci_row.append(frequency)
    df = pd.DataFrame.from_records(ahci_list, columns=headers)
    df.to_excel(master_file, index=False)
