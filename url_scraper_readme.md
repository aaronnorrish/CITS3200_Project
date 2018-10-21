### url_scraper.py readme

This program takes in a given xlsx file and finds the appropriate submission guidelines url
and home page url for a given journal by scraping the web. This program takes along time to run
as it needs to scrape many pages aswell as wait for arbitrary amounts of time to avoid IP blocking.
for this reason, its ideal to run this program is small batches.
This program may only be run at UWA as the university has special IP privilleges that allow it to 
scrape researchgate websites with out being blocked.

#Installation

1. Install Python
2. Install Pip
3. Install The Following packages:
  #openpyxl
  ``` 
  pip install openpyxl
  '''
  #pprint
  '''
  pip install pprint
  '''
  #urllib3
  '''
  pip install urllib3
  '''
  #BeautifulSoup
  '''
  pip install bs4
  '''
  #requests
  '''
  pip install requests
  '''
  #numpy
  '''
  pip install numpy
  '''
  #selenium
  '''
  pip install selenium
  '''
  
4. Install Chromedriver and place .exe in same location that url_scraper.py is running from
5. Install Gecko driver and place .exe in same location that url_scraper.py is running from
6. Run program
