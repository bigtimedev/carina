
from selenium import webdriver

url = 'https://pslinks.fiu.edu/psc/cslinks/EMPLOYEE/CAMP/Kkac/COMMUNITY_ACCESS.CLASS_SEARCH.GBL&FolderPath=PORTAL_ROOT_OBJECT.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder?&'
driver = webdriver.Chrome()
driver.get(url)
driver.get(url) #with cookies

subjectDropDown = driver.find_element_by_xpath('//*[@id="SSR_CLSRCH_WRK_ACAD_ORG$2"]')
for option in subjectDropDown.find_elements_by_tag_name('option'):
	print option.text