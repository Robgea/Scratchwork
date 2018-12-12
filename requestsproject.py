from bs4 import BeautifulSoup
import requests
#from lxml import etree

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
    report_page = requests.get('https://www.sec.gov/' + txt_link)
    
    soup_3 = BeautifulSoup(report_page.content, "html5lib")

    tables = soup_3.find_all('infoTable')
    for table in tables:
      print(table.text)


parse_xml(find_xml(find_page(target)))
