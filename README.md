# CITS3200_Project

## Installation Guide
To download this program, you may simply click the green "Clone or download" button on the repository homepage and either download the repo as a ZIP file or clone it using the GitHub Desktop app. Alternatively, if you have git installed on your computer, you may clone from the command line:
```
$ git clone https://github.com/aaronnorrish/CITS3200_Project.git
```

This program requires Python3 and the following Python modules:
  * sys
  * os.path
  * re
  * unicodedata
  * BeautifulSoup
  * lxml
  * requests
  * pandas
  * xlrd
  * openpyxl
  * urllib3

[Here is a link to install Python3](https://www.python.org/downloads/).

The sys, os.path, re and unicodedata modules belong to the Python Standard Library (and so do not require installation if Python is already installed), however the other modules will require installing. [See this link for more information on how to install Python packages.](https://packaging.python.org/tutorials/installing-packages/#ensure-you-can-run-python-from-the-command-line)

A link to the installation guide for each of these other packages have been provided below, however, on MacOS with pip3 installed, these packages may simply be installed by entering the following into the command line:

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
```
pip3 install --user beautifulsoup4
```
* [lxml](https://lxml.de/installation.html)
```
pip3 install --user lxml
```
* [requests](http://docs.python-requests.org/en/master/user/install/)
```
pip3 install --user requests
```
* [pandas](https://pandas.pydata.org/pandas-docs/stable/install.html)
```
pip3 install --user --upgrade pandas
```
* [xlrd](https://xlrd.readthedocs.io/en/latest/installation.html)
```
pip3 install --user xlrd
```
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
```
pip3 install --user openpyxl
```
* [urllib3](https://urllib3.readthedocs.io/en/latest/)
```
pip3 install --user urllib3
```

## User Guide
This program consists of six Python files which are stored in the src folder. The master file is scrape_journals.py which can be run from the command line in one of two ways:

#### Option 1 - No Command Line Arguments


```
python3 scrape_journals.py
```


#### Option 2 - One Command Line Argument


```
python3 scrape_journals.py <start_position>
```


Where `start_position` denotes the position of the first journal in the spreadsheet from which the program should start execution from. Note that 0 is taken to be the index of the first journal listed in the spreadsheet.


#### Option 3 - Two Command Line Arguments


```
python3 scrape_journals.py <start_position> <end_position>
```



Where `end_position` is the index of the last journal the program should try to obtain the URLs for.


### scrape_journals.py
This is the master file which runs the program. It requires that the A&HCI and SSCI master lists Excel files are stored in the src directory and are named `publist_ahci.xlsx` and `publist_ssci.xlsx` respectively. By default, these files are stored in src, however, should new lists be released, these will require updating. The A&HCI and SSCI files are typically given in PDF and so require being converted into .xlsx format. There are many websites that perform this task for free such as [this one](https://smallpdf.com/pdf-to-excel). The converted Excel files must contain a header with the following or similarly titled fields:
  * Journal Title
  * Publisher
  * ISSN
  * E-ISSN
  * Country
  * Language


in that order. In some cases, the conversion process adds empty columns in between these columns of the Excel file. Any such columns need to be removed.

This program first tries to obtain the journal publishing frequencies as listed on the Clarivate website and writes them to `ahci_frequencies.xlsx` and `ssci_frequencies.xlsx` respectively before merging them into `master_URLs_frequencies.xlsx` should the frequencies been retrieved. The URLs to the first webpage of the [SSCI Master List](http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=SS&mode=print&Page=1) and [A&HCI Master List](http://mjl.clarivate.com/cgi-bin/jrnlst/jlresults.cgi?PC=H&mode=print&Page=1) are hard coded into this program as they are unreachable by a webcrawler. These URLs were obtained by clicking on the "Format for print A-Z" button on the Master Journal List website for each master list and selecting the link to the first 500 journals. Should the URLs provided be changed at any point, navigate to each of these pages and replace the URLs given as arguments to the get_journal_frequencies function on lines 41 and 42.

Due to the inherent risks involved in parsing HTML (such as the possibility of the HTML format being changed), this program has been designed to be robust and so executes whether or not these frequencies were able to be obtained. If they were not able to be obtained, the program will write the journal URLs to `master_URLs.xlsx`. The program will first try to retrieve the journal's homepage and instructions for authors from the Taylor and Francis website, then the Springer website and will append the results to `master_URLs_frequencies.xlsx` or `master_URLs.xlsx` depending on what the case may be.

Because of the large amount of time it takes for this program to execute over the total list of journals, a functionality has been built-in to allow the user to terminate execution (by pressing Control-C) once the program has started to search for journal URLs (the program will notify the user printing "Begin scraping journal URLs" to the command line). In such a case, the program will write the data it has found so far into an Excel file before terminating. Note that each time execution is resumed by re-running the program, the program will first try to obtain the journal frequencies if they have not already been. In addition to this, there is the option to pass command line arguments denoting the start and end positions of the journals in the spreadsheet for which the user would like the program to execute over. This allows the program to be run in chunks for convenience. By default, the program executes over the whole spreadsheet.

To counter any possible occurrences such as the Internet connection being dropped, or the Taylor and Francis or Springer websites being briefly unresponsive, the program will execute over the spreadsheet at least twice. On each resulting iteration, the program will try to obtain the URLs for journals that were not obtained in the previous iteration. Once the number of such journals has not changed, the program will terminate.
