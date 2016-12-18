
from selenium import webdriver
from selenium import common

import scraperhelpers

url = 'https://pslinks.fiu.edu/psc/cslinks/EMPLOYEE/CAMP/Kkac/COMMUNITY_ACCESS.CLASS_SEARCH.GBL&FolderPath=PORTAL_ROOT_OBJECT.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder?&'

def click_through_classes():
	 links = driver.find_elements_by_css_selector('a[id^="MTG_CLASS_NBR"]')
	 ids = [link.get_attribute('id') for link in links]
	 print ids

driver = webdriver.Chrome()
driver.get(url)
driver.get(url) #with cookies

for number in range(1000):
	 padded_number = '%03d' % number

	 course_number_select = driver.find_element_by_id('SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$4')
	 for option in course_number_select.find_elements_by_tag_name('option'):
		  if option.get_attribute('value') == 'C':
				option.click()
				break

	 course_number_input = driver.find_element_by_id('SSR_CLSRCH_WRK_CATALOG_NBR$4')
	 course_number_input.clear()
	 course_number_input.send_keys(padded_number)
	 submit_button = driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH')
	 submit_button.click()

	 scraperhelpers.wait_for_stale_link(submit_button)

	 try:
		  ok_button = driver.find_element_by_id('#ICSave')
		  ok_button.click()
		  scraperhelpers.wait_for_stale_link(ok_button)
	 except common.exceptions.NoSuchElementException:
		  print('g2g')

	 for course in driver.find_elements_by_class_name('PAGROUPBOXLABELLEVEL1'):
		  print course.text

	 click_through_classes()

	 try:
		  new_search_button = driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH')
		  new_search_button.click()
		  scraperhelpers.wait_for_stale_link(new_search_button)
	 except common.exceptions.NoSuchElementException:
		  print('no results found for %d' % number)

driver.close()
