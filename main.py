
from selenium import webdriver

import scraperhelpers

url = 'https://pslinks.fiu.edu/psc/cslinks/EMPLOYEE/CAMP/Kkac/COMMUNITY_ACCESS.CLASS_SEARCH.GBL&FolderPath=PORTAL_ROOT_OBJECT.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder?&'



driver = webdriver.Chrome()
driver.get(url)
driver.get(url) #with cookies


subjectDropDown = driver.find_element_by_xpath('//*[@id="SSR_CLSRCH_WRK_ACAD_ORG$2"]')
for option in subjectDropDown.find_elements_by_tag_name('option'):
	if not option.text.isspace():
		option.click()
		submitButton = driver.find_element_by_xpath('//*[@id="CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"]')
		submitButton.click()

		scraperhelpers.wait_for_stale_link(submitButton)

		for course in driver.find_elements_by_class_name('PAGROUPBOXLABELLEVEL1'):
			print course.text


		break #for now

driver.close()
