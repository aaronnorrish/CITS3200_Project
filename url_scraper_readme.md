### url_scraper.py readme

This program takes in a given xlsx file and finds the appropriate submission guidelines url
and home page url for a given journal by scraping the web. This program takes along time to run
as it needs to scrape many pages aswell as wait for arbitrary amounts of time to avoid IP blocking.
for this reason, its ideal to run this program is small batches.
This program may only be run at UWA as the university has special IP privilleges that allow it to 
scrape researchgate websites with out being blocked.

#Installation

1. Install [Python3](https://www.python.org/downloads/). Python is installed by default on OSX systems. 
2. Install [pip](https://pypi.org/project/pip/)
3. Install fhe following packages:
  * openpyxl
  ```
  pip install openpyxl
  ``` 
  * pprint
  ```
  pip install pprint
  ```
  * urllib3
  ```
  pip install urllib3
  ```
  * BeautifulSoup
  ```
  pip install bs4
  ```
  * requests
  ```
  pip install requests
  ```
  * numpy
  ```
  pip install numpy
  ```
  * selenium
  ```
  pip install selenium
  ```
  
4. Install [Chromedriver](http://chromedriver.chromium.org/downloads) and place .exe in same location that url_scraper.py is running from
5. Install [Geckodriver](https://github.com/mozilla/geckodriver/releases) and place .exe in same location that url_scraper.py is running from
6. Open the command prompt and run the program with the following command:
```
python3 url_scraper.py
```
