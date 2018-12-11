from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

browser = webdriver.Chrome()
target = '0001166559'


def find_page(target_CIK):
    browser.get('https://www.sec.gov/edgar/searchedgar/companysearch.html')
    search_bar = browser.find_element_by_id('cik')
    search_bar.send_keys(target_CIK)
    find_link = browser.find_element_by_id('cik_find')
    find_link.click()
    type_bar = browser.find_element_by_name('type')
    type_bar.send_keys('13F')
    type_bar.send_keys(Keys.ENTER)
    documents_link = browser.find_element_by_id('documentsbutton')
    documents_link.click()








find_page(target)

