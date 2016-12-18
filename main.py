
from selenium import webdriver
from selenium import common

import scraperhelpers

url = 'https://pslinks.fiu.edu/psc/cslinks/EMPLOYEE/CAMP/Kkac/COMMUNITY_ACCESS.CLASS_SEARCH.GBL&FolderPath=PORTAL_ROOT_OBJECT.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder?&'

driver = webdriver.Chrome()
driver.get(url)
driver.get(url) #with cookies

already_seen = set()

def log_entry(class_num,
		  class_name,
		  section_name,
		  instructor,
		  capacity,
		  enrolled_num,
		  available_seats,
		  wait_list_capacity,
		  wait_list_total):
	 print ("%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
				class_num,
				class_name,
				section_name,
				instructor,
				capacity,
				enrolled_num,
				available_seats,
				wait_list_capacity,
				wait_list_total
				)).replace('\n', ' ')



def click_through_classes():
	 links = driver.find_elements_by_css_selector('a[id^="MTG_CLASS_NBR"]')
	 ids = [link.get_attribute('id') for link in links]

	 for i in ids:
		  class_num = driver.find_element_by_id(i).text
		  if class_num in already_seen:
				continue
		  already_seen.add(class_num)
		  num = i.split('$')[1]
		  section_name = driver.find_element_by_id('MTG_CLASSNAME$%s' % num).text
		  link = driver.find_element_by_id(i)
		  link.click()
		  scraperhelpers.wait_for_stale_link(link)
		  class_name = driver.find_element_by_id('DERIVED_CLSRCH_DESCR200').text
		  capacity = driver.find_element_by_id('SSR_CLS_DTL_WRK_ENRL_CAP').text
		  enrolled_num = driver.find_element_by_id('SSR_CLS_DTL_WRK_ENRL_TOT').text
		  available_seats = driver.find_element_by_id('SSR_CLS_DTL_WRK_AVAILABLE_SEATS').text
		  instructor = driver.find_element_by_id('MTG_INSTR$0').text
		  wait_list_capacity = driver.find_element_by_id('SSR_CLS_DTL_WRK_WAIT_CAP').text
		  wait_list_total = driver.find_element_by_id('SSR_CLS_DTL_WRK_WAIT_TOT').text
		  log_entry(class_num, class_name, section_name, instructor, capacity, enrolled_num, available_seats, wait_list_capacity, wait_list_total)
		  back_button = driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_BACK')
		  back_button.click()
		  scraperhelpers.wait_for_stale_link(back_button)


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
		  pass

	 click_through_classes()

	 try:
		  new_search_button = driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH')
		  new_search_button.click()
		  scraperhelpers.wait_for_stale_link(new_search_button)
	 except common.exceptions.NoSuchElementException:
		  pass

driver.close()
