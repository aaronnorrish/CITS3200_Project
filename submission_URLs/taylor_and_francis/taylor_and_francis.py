import requests, re
from bs4 import BeautifulSoup
import pandas as pd
import sys
import unicodedata

def remove_accents(string):
    nfkd_form = unicodedata.normalize('NFKD', string)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

sheet = pd.read_excel("taylor_and_francis_no_duplicates.xlsx", header=None)
l = pd.Series.tolist(sheet)
headers = l.pop(0)


home_url = "https://www.tandfonline.com"
search_url_start = "https://www.tandfonline.com/action/doSearch?AllField="
instructions_url_start = "/action/authorSubmission?journalCode="
instructions_url_end = "&page=instructions"
# url = "https://www.tandfonline.com/action/doSearch?AllField=1747-7603"

s,t,w, = 0,0,0
for i in range(len(l)):
    try:
        search_url = search_url_start + l[i][2]
        source = requests.get(search_url)
        soup = BeautifulSoup(source.content, 'lxml')
        found = False
        try:
            ol_tag = soup.find("ol", {"class":"search-results"})
            for li_tag in ol_tag.find_all("li"):
                relative_path = li_tag.find("div", {"class":"publication-meta"}).span.a.get('href')
                journal_url = home_url + relative_path
                journal_source = requests.get(journal_url)
                journal_soup = BeautifulSoup(journal_source.content, 'lxml')
                journal_name = journal_soup.find("div", {"class":"journalMetaTitle page-heading"}).a.span.text
                if(l[i][0].lower() == journal_name.lower()):
                    found = True
                    s += 1
                    break
                else:
                    j = remove_accents(l[i][0].lower().replace("the ", "").replace(",","").replace("&", "and"))
                    journal_name = remove_accents(journal_name.lower().replace("the ", "").replace(",","").replace("&", "and"))
                    if(j == journal_name or j.find(journal_name) != -1 or journal_name.find(j) != -1):
                        found = True
                        # print(l[i][0].lower(), journal_name.lower())
                        t += 1
                        break
                    else:
                        j = re.sub('[^A-Za-z0-9]+', '', j)
                        journal_name = re.sub('[^A-Za-z0-9]+', '', journal_name)
                        # j = j.replace("&", "and").replace("-", "").replace(":", "").replace("'", "").replace(" ", "").replace("/", "").replace('-', '')
                        # journal_name = journal_name.replace("&", "and").replace("-", "").replace(":", "").replace("'", "").replace(" ", "").replace("/", "").replace('-', '')
                        # j = j.replace("&", "and").strip(["-", ":", "'", " ", "/", '-'])
                        # journal_name = journal_name.replace("&", "and").strip(["-", ":", "'", " ", "/", '-'])
                        if(j == journal_name or j.find(journal_name) != -1 or journal_name.find(j) != -1):
                            found = True
                            # print(l[i][0].lower(), journal_name.lower())
                            w += 1
                            break
                        else:
                            print(j, journal_name)
            if found:
                code = re.search('/toc/(.+?)/current', relative_path).group(1)
                #try: testing if the submission page exists - need a try here
                # if so l[i].append(instructions_url)
                # else l[i].append(journal_url)
                instructions_url = home_url + instructions_url_start + code + instructions_url_end
                instructions_source = requests.get(instructions_url)
                instructions_soup = BeautifulSoup(instructions_source.content, 'lxml')
                if instructions_soup.head.title.text != "Error":
                    l[i].append(instructions_url)
                    print("success")
                else:
                    print("failure:", l[i][0])
                    l[i].append(journal_url)
                print(relative_path, code)
        except ConnectionResetError:
            i-=1
        except AttributeError:
            try:
                print(l[i][0], l[i][2])
                search_url = search_url_start + l[i][3]
                source = requests.get(search_url)
                soup = BeautifulSoup(source.content, 'lxml')
                found = False
                ol_tag = soup.find("ol", {"class":"search-results"})
                for li_tag in ol_tag.find_all("li"):
                    relative_path = li_tag.find("div", {"class":"publication-meta"}).span.a.get('href')
                    journal_url = home_url + relative_path
                    journal_source = requests.get(journal_url)
                    journal_soup = BeautifulSoup(journal_source.content, 'lxml')
                    journal_name = journal_soup.find("div", {"class":"journalMetaTitle page-heading"}).a.span.text
                    if(l[i][0].lower() == journal_name.lower()):
                        found = True
                        s += 1
                        break
                    else:
                        j = remove_accents(l[i][0].lower().replace("the ", "").replace(",","").replace("&", "and"))
                        journal_name = remove_accents(journal_name.lower().replace("the ", "").replace(",","").replace("&", "and"))
                        if(j == journal_name or j.find(journal_name) != -1 or journal_name.find(j) != -1):
                            found = True
                            # print(l[i][0].lower(), journal_name.lower())
                            t += 1
                            break
                        else:
                            j = re.sub('[^A-Za-z0-9]+', '', j)
                            journal_name = re.sub('[^A-Za-z0-9]+', '', journal_name)
                            # j = j.replace("&", "and").replace("-", "").replace(":", "").replace("'", "").replace(" ", "").replace("/", "").replace('-', '')
                            # journal_name = journal_name.replace("&", "and").replace("-", "").replace(":", "").replace("'", "").replace(" ", "").replace("/", "").replace('-', '')
                            # j = j.replace("&", "and").strip(["-", ":", "'", " ", "/", '-'])
                            # journal_name = journal_name.replace("&", "and").strip(["-", ":", "'", " ", "/", '-'])
                            if(j == journal_name or j.find(journal_name) != -1 or journal_name.find(j) != -1):
                                found = True
                                # print(l[i][0].lower(), journal_name.lower())
                                w += 1
                                break
                            else:
                                print(j, journal_name)
                if found:
                    code = re.search('/toc/(.+?)/current', relative_path).group(1)
                    #try: testing if the submission page exists - need a try here
                    # if so l[i].append(instructions_url)
                    # else l[i].append(journal_url)
                    instructions_url = home_url + instructions_url_start + code + instructions_url_end
                    instructions_source = requests.get(instructions_url)
                    instructions_soup = BeautifulSoup(instructions_source.content, 'lxml')
                    if instructions_soup.head.title.text != "Error":
                        l[i].append(instructions_url)
                        print("success")
                    else:
                        l[i].append(journal_url)
                        print("failure:", l[i][0])
                    print(relative_path, code)
            except:
                print(l[i][0], l[i][2])
        except:
            print("exception: ", sys.exc_info())
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("error ", sys.exc_info())
        i-=1 # not working

print(s, t, w, len(l), (s+t+w)/len(l))

headers.append("Homepage URL")
df = pd.DataFrame.from_records(l, columns=headers)
df.to_excel("taylor_and_francis_journal_homepage_urls.xlsx", index=False)

# if we match journal, extract code then add to submissions url:
# https://www.tandfonline.com/action/authorSubmission?journalCode=rdsp20&page=instructions
