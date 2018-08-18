# CITS3200_Project

[Sprint 1](https://docs.google.com/document/d/1tTihT0tXBC_Wv4KGTl56_YIdyBtyK2or0R0NVLBpva8/edit?usp=sharing)

## Usage
### journal_frequency.py
This program can be run from the command line in one of two ways:
#### Option 1 - No Command Line Arguments
```
python3 journal_frequency.py
```

This method requires that the SSCI and A&HCI master list Excel files are stored in the current directory and are named `publist_ssci.xlsx` and `publist_ahci.xlsx` respectively. You do not have to worry about this if you just simply clone the repo and run the program from the command line; these files will have the correct names and will be in the correct directory.
#### Option 2 - With Command Line Arguments
```
python3 journal_frequency.py <ssci_url> <read_ssci_journals.xlsx> <write_ssci_journals.xlsx> <ahci_url> <read_ahci_journals.xlsx> <write_ahci_journals.xlsx>
```

This method requires the user to pass the URL to the first webpage of the [SSCI Master List](http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=SS&mode=print&Page=1) and [A&HCI Master List](http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=H&mode=print&Page=1), as well as the paths to the Excel files:   
  * containing the SSCI and A&HCI Master Lists (two separate files)
  * which the user would like the updated data to be written to (also two separate files)

as command line arguments.

#### Requirements
This program requires Python3 and the following Python modules:
  * sys
  * re
  * BeautifulSoup
  * lxml
  * requests
  * pandas
  * xlrd
  * openpyxl

The sys and re modules belong to the Python Standard Library, however the other modules will require installing. [See this link for more information on how to install Python packages.](https://packaging.python.org/tutorials/installing-packages/#ensure-you-can-run-python-from-the-command-line)

On Apple computers with pip3 installed, these other packages may simply be installed by entering the following into the command line:
* BeautifulSoup
```
pip3 install --user beautifulsoup4
```
* lxml
```
pip3 install --user lxml
```
* requests
```
pip3 install --user requests
```
* pandas
```
pip3 install --user --upgrade pandas
```
* xlrd
```
pip3 install --user xlrd
```
* openpyxl
```
pip3 install --user openpyxl
```
