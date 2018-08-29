#Import modules
#pandas
#numpy
#beautifulsoup4
#etc

# https://docs.google.com/document/d/170enUYwhoX5xjHld9fs92MUjpOHgRbCG6riMfFhiIG0/edit


def open_csv(csv):
    #opens merged masterlist
    #returns csv as a dataframe
    #can be xlsx
    return df

def tf_scraper(journal):
    #Opens https://www.tandofonline.com/
    #Search journal in website
    #Open Submission page via HTML anchor tag
    journal.submission_page = "submission page url"
    return     


def s_scraper(journal):
    #Opens https://www.springer.com/gp
    #Search journal in website
    #Open Submission page via HTML anchor tag
    #May habe to search with for a pdf file
    journal.submission_page = "submission page url"
    return     


def concatonate_URL(journal, target_publishers):
    if journal.name == "Wiley":
        #open https://onlinelibrary.wiley.com/page/journal/+ journal.e-issn +/homepage/forauthors.html
        journal.submission_page = "submission page url"
    # Repeat process for the rest of the 'green' websites specified in sheet 2. 
    if journal.name == "WALTER DE GRUYTER GMBH": #or another 'blue' website
        abrev_jname = abbreviate(journal.name)
        # open https://www.degruyter.com/view/j/+ abrev_jname+ #callForPapersHeader

    return

def abbreviate(name):
    # Create a list of several potential ways to abbreviate the journal name
    # Eg. European Analysis of The United States 
    # potential_abrevs = ["eaotus",euaotus, eaus, euaus]
    # for abrev potential_abrev
    #   open "www.example.com/" + abrev + "#submission_guidelines"
    #   if h1 tag == name
        abrev = name
        return abrev

def find_submission_page(df, target_publishers):
    #maybe limit number of instances in RAM
    for journal in df:
        if df.publisher == "Taylor and Francis":
            tf_scraper(journal)
        if df.publisher == "Springer":
            s_scraper(journal)
        if df.publisher in target_publishers:
            concatonate_URL(journal, target_publishers)
    return

def main():
    
    #Names of publishers that encompass about 65%
    target_publishers = ["Wiley", "Sage Publications INC","Elsevier",
    "CAMBRIDGE UNIV PRESS", "OXFORD UNIV PRESS", "WALTER DE GRUTYER GMBH", 
    "JOHNS HOPKINS UNIV PRESS", "UNIV CHICAGO PRESS", 
    "EMERALD GROUP PUBLISHING LTD","BRILL ACADEMIC PUBLISHERS",
    "JOHN BENJAMINS PUBLISHING CO","AMER PSYCHOLOGICAL ASSOC", "DUKE UNIV PRESS"]

    df = open_csv("masterlist.csv")
    find_submission_page(df, target_publishers)
    
