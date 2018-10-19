import pandas as pd

def determine_fresh_sheet(master_file):
    master_df = pd.read_excel(master_file, header=None)
    master_list = pd.Series.tolist(master_df)
    headers = master_list.pop(0)
    if headers[len(headers)-1] == "URL":
        return False
    return True

def calculate_remaining(spreadsheet_list, frequencies):
    remaining = 0
    for row in spreadsheet_list:
        if frequencies and (len(row) < 10 or str(row[9]) == "nan"):
            remaining += 1
        elif not frequencies and (len(row) < 9 or str(row[8]) == "nan"):
            remaining += 1
    return remaining
