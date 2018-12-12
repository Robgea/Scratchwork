from bs4 import BeautifulSoup
import requests
import csv

# target CIK
target = '0001166559'


def find_page(target):
    # go right to a search that just shows 13F filings 
    search_return = requests.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + target +'&type=13F&dateb=&owner=exclude&output=xml&count=100')
    
    #parse the page
    soup = BeautifulSoup(search_return.content, "html5lib")
    results = soup.find_all('filing')
    
    # find the first result
    result = results[0]
    #get the link
    result_link = result.find('filinghref')
    page_link = result_link.text

    #return the link
    return page_link

def find_xml(url):
    # go to the filings page
    filing_page = requests.get(url)

    # parse the page
    soup_2 = BeautifulSoup(filing_page.content, "html5lib")
    
    # find the text report
    report_links = soup_2.find_all('a')
    for link in report_links:
        if link.text[-4:] == ('.txt'):
            return(link.get('href'))

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

    #parse the info tables
    
    info = soup_3.find_all('infoTable')

    #create the TSV, name it after the organization and the period of the report.

    csvFile = open(org_name.text + '_' + report_period.text +'.tsv', 'w', newline='')
    csvWriter = csv.writer(csvFile, delimiter='\t', lineterminator='\n\n')
    
    #set up the table

    csvWriter.writerow([org_name.text])
    csvWriter.writerow([report_period.text])
    csvWriter.writerow(' ')
    csvWriter.writerow(['Name of Issuer', 'Sole Stock', 'Shared Stock', 'No Vote Stock', 'Total Value'])

    for stock in info:
        issuer = stock.find('nameOfIssuer')
        value = stock.find('value')
        sole_shares = stock.find('Sole')
        shared_shares = stock.find('Shared')
        novote_shares = stock.find('None')
        csvWriter.writerow([issuer.text, sole_shares.text, shared_shares.text, novote_shares.text, value.text])

    
    csvFile.close()    










parse_xml(find_xml(find_page(target)))
