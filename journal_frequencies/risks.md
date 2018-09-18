# Risks
Format of PDF/Excel spreadsheet being changed
  * will have to specify in documentation what format the input spreadsheet must be in
  * alternatively could build in functionality for command line input for which column the ISSN is in, the number of columns, etc. However this is most likely overkill
  * need to ensure that the two empty columns are in the spreadsheet otherwise

URL of webpage being changed
  * as this URL is unreachable using a webcrawler it must either be hardcoded
  * this can be solved by adding the option to pass URL to the program from the command line
  * will need to specify in the documentation how the required URL may be reached by a human

Format of webpage's HTML being changed
  * this is a harder problem to deal with, the only practical solution to this is to specify in the documentation what information is required from the webpage to match the online information to that in the Excel master list
