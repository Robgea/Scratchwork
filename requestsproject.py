from bs4 import BeautifulSoup
import requests

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
    filing_page = requests.get(url)
    soup_2 = BeautifulSoup(filing_page.content, "html5lib")
    report_links = soup_2.find_all('a')
    for link in report_links:
      print(link)



find_xml(find_page(target))
