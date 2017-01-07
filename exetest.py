from selenium import webdriver
from selenium import common
from collections import deque
from time import gmtime, strftime, sleep
import re
import sys

import threading
import scraperhelpers
import code

FILE_NAME = 'exetest.txt'
output_file = open(FILE_NAME, 'w')
output_file.write("Expecting 'search for classes'\n")

url = 'https://mymdcsprodpub.oracleoutsourcing.com/psp/PMYM1J/CUSTOMER/CAMP/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?FolderPath=PORTAL_ROOT_OBJECT.CO_EMPLOYEE_SELF_SERVICE.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder'
driver = webdriver.Chrome()
driver.get(url)

try:
	search_iframe = driver.find_element_by_id('ptifrmtgtframe')
	driver.switch_to_frame(search_iframe)
except common.exceptions.NoSuchElementException:
	pass



header_title = driver.find_element_by_id('DERIVED_CLSRCH_SS_TRANSACT_TITLE')
output_file.write(header_title.text.encode('utf-8'))