from selenium import webdriver
from selenium import common
from collections import deque

import threading
import scraperhelpers
import code

url = 'https://pslinks.fiu.edu/psc/cslinks/EMPLOYEE/CAMP/Kkac/COMMUNITY_ACCESS.CLASS_SEARCH.GBL&FolderPath=PORTAL_ROOT_OBJECT.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder?&'
already_seen = set()

FILE_NAME = "output.csv"
file_lock = threading.Lock()
output_file = open(FILE_NAME, 'w')
output_file.write("Class Number, Class Name, Section Name, Instructor, Capacity, Enrolled, Available Seats, Wait List Capacity, Wait List Total")

def log_entry(class_num,
        class_name,
        section_name,
        instructor,
        capacity,
        enrolled_num,
        available_seats,
        wait_list_capacity,
        wait_list_total):
    file_lock.acquire()
    try:
        output_file.write(("%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
        class_num,
        class_name,
        section_name,
        instructor,
        capacity,
        enrolled_num,
        available_seats,
        wait_list_capacity,
        wait_list_total,
        )).encode('utf8').replace('\n', ' ') + '\n')
    except UnicodeEncodeError:
        print "goddammit with this"
    file_lock.release()

def click_through_classes(driver):
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

def search_by_class_number(number, driver):
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

    try:
        error_message = driver.find_element_by_id('DERIVED_CLSMSG_ERROR_TEXT')
        if error_message and 'maximum limit' in error_message.text:
            print "too many in %s " % padded_number
    except common.exceptions.NoSuchElementException:
        click_through_classes(driver)

    try:
        new_search_button = driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH')
        new_search_button.click()
        scraperhelpers.wait_for_stale_link(new_search_button)
    except common.exceptions.NoSuchElementException:
        pass

# lock acquisition specifically for getting length of stack
stack_lock = threading.Lock()
stack = deque(range(1000, 8000))

def spawn_driver():
    driver = webdriver.Chrome()
    driver.get(url)
    driver.get(url) # with cookies
    stack_lock.acquire()
    while len(stack) > 0:
        stack_lock.release()
        number = stack.pop()
        search_by_class_number(number, driver)
        stack_lock.acquire()
    driver.close()

for num in range(10):
    t = threading.Thread(target=spawn_driver)
    t.start()
