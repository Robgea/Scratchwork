from bs4 import BeautifulSoup
import requests
import csv


#function to find the page containing the 13F filings.
def find_page(target):
    # go right to a search that just shows 13F filings 
    search_return = requests.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + target +'&type=13F&dateb=&owner=exclude&output=xml&count=100')
    
    #parse the page
    soup = BeautifulSoup(search_return.content, "html5lib")
    results = soup.find_all('filing')
    
    # if no filings then we skip the page and print the error.
    if len(results) == 0:
        print('No luck finding a 13F report for ' + target +'.  Continuing on to next CIK.')

    else: 
        # find the first result
        result = results[0]
        #get the link
        result_link = result.find('filinghref')
        page_link = result_link.text

        #pass the link onto the next step
        find_xml(page_link)


#function to find the report
def find_xml(url):
    # go to the filings page
    filing_page = requests.get(url)

    # parse the page
    soup_2 = BeautifulSoup(filing_page.content, "html5lib")
    
    # find the text report, and pass it on to the parser
    report_links = soup_2.find_all('a')
    for link in report_links:
        if link.text[-4:] == ('.txt'):
            parse_xml(link.get('href'))


#function to parse the report.
def parse_xml(txt_link):
    #the XML
    
    report_page = requests.get('https://www.sec.gov/' + txt_link)
    
    #parse the page
    
    soup_3 = BeautifulSoup(report_page.content, "xml")

    #get the organization name
    
    org_name = soup_3.find('name')
    print(org_name.text)

    #get the date the filing is reporting through.
    
    report_period = soup_3.find('periodOfReport')
    print(report_period.text)

    #Get the CIK from the report, this is for the error catcher below.
    report_cik = soup_3.find('cik')


    #parse the info tables
    
    info = soup_3.find_all('infoTable')

    #create the TSV, name it after the organization and the period of the report. Try and except are for if there's an invalid name.
    
    try:
        csvFile = open(org_name.text + '_' + report_period.text +'.tsv', 'w', newline='')
        csvWriter = csv.writer(csvFile, delimiter='\t', lineterminator='\n\n')
        
        #set up the table

        csvWriter.writerow(['Name of Organization: ', org_name.text])
        csvWriter.writerow(['Period of Report ', report_period.text])
        csvWriter.writerow(' ')
        csvWriter.writerow(['Name of Issuer', 'Sole Stock', 'Shared Stock', 'No Vote Stock', 'Total Value'])

        #looping through the info in the XML and printing it to the table

        for stock in info:
            issuer = stock.find('nameOfIssuer')
            value = stock.find('value')
            sole_shares = stock.find('Sole')
            shared_shares = stock.find('Shared')
            novote_shares = stock.find('None')
            csvWriter.writerow([issuer.text, sole_shares.text, shared_shares.text, novote_shares.text, value.text])

        csvFile.close()   
    
    except:
          print('Hit an error with the report for CIK: ' + report_cik.text + ' for group ' + org_name.text + ' this is probably becauase of an invalid character in the name. Sorry.')
    
  


# function to start the process and generate a list of CIKs to lookup. 

def initiator():
    
    #empty list to put CIKs into
    starting_list = []
    
    #greeting message
    print("Hello! This is Rob Glass's CIK lookup. \n\n  ")
    
    new_CIK = ''

    # while loop to take inputs
    while new_CIK != 'Start' :
        new_CIK = input('Please add a CIK, if you are finished adding CIKs input "Start": ')
        if new_CIK == 'Start':
          break
        elif (len(new_CIK) != 10):
            print('Sorry, that looks like an invalid CIK. Please recheck your CIK and try again.')
        elif new_CIK.isdigit() == False:
            print('Sorry, a CIK can only have numbers please try again.')
        else:
            starting_list.append(new_CIK)


    #for loop that runs the program for every CIK
    for CIK in starting_list:
        find_page(CIK)

    print('All done!')




initiator()



