import openpyxl as xl
import pprint as pp
import urllib3
from bs4 import BeautifulSoup
import requests

#Load xlsx file into Python
wb = xl.load_workbook('output.xlsx') #Open Input workbook
journals = wb['journal_sheet'] #Open journals worksheet
urls = wb["url_sheet"]
num_rows = len(tuple(journals.rows))
print("Program Starting")

#journal_sheet column map
#Col 0/A = journal name
#Col 1/B = Publisher
#Col 2/C = ISSN
#Col 3/D = EISSN
#Col 4/E = Country
#Col 5/F = Language
#Col 6/G = Category
#Col 7/H = Submission Guidelines URL

def get_url(row, source):
    #Alias varibles for readability
    
    journal = row[0]
    publisher = row[1]
    issn = row[2]
    eissn = row[3]
    target = row[8]
    
    #Check for each attribute in URL and replace with appropriate variable
    
    if "J_U_NAME" in source:
        #replace J_U_NAME with lowercase journal name and replace space with an underscore
        temp_name = journal.value.lower().replace(" ","_")
        target = source.replace("J_U_NAME", temp_name)
        source = target
    if "JNAME" in source:
        #Replace JNAME with lowercase journal name and replace space with hyphen
        temp_name = journal.value.lower().replace(" ", "-") 
        target = source.replace("JNAME",temp_name)
        source = target
    if "EISSN" in source:
        #Replace EISSN with actual EISSN, replacing space with hyphen
        temp_name = eissn.value.replace("-","")
        target = source.replace("EISSN", temp_name)
        source = target
    if "E_H_SSN" in source:
        #Replace EISSN with actual EISSN, keeping hyphens
        temp_name = eissn.value
        target = source.replace("E_H_SSN", temp_name)
        source = target
    if "ISSN" in source:
        #Replace ISSN with actual ISSN, replacing space with hyphen
        temp_name = issn.value.replace("-","")
        target = source.replace("ISSN", temp_name)
        source = target
    if "I_H_SSN" in source:
        #Replace ISSN with actual ISSN, keeping hyphens
        temp_name = issn.value
        target = source.replace("I_H_SSN", temp_name)
        source = target
    return target

#Iterate over all rows, find homepage
#TAKES VERY VERY LONG
home_page_url = "https://www.researchgate.net/journal/I_H_SSN_J_U_NAME"
limit = 0 #recomended for testing

for row in journals.iter_rows(max_col=9, min_row=2, max_row=num_rows):
    if limit == 5:
        break
    #try:
        
    page = requests.get(get_url(row, home_page_url))
    soup = BeautifulSoup(page.text,'html.parser')
    for link in soup.find_all("a", {"class": "nova-e-link nova-e-link--color-blue nova-e-link--theme-bare"}):
        print(link.get('href'))
        row[8].value = link.get('href')
        limit +=1
        
   # except:
    #    continue
        

wb.save('output.xlsx')