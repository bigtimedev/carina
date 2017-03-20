# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium import common
from collections import deque
from time import gmtime, strftime

import threading
import scraperhelpers
import code
import re
import sys
import os

url = 'https://pslinks.fiu.edu/psc/cslinks/EMPLOYEE/CAMP/Kkac/COMMUNITY_ACCESS.CLASS_SEARCH.GBL&FolderPath=PORTAL_ROOT_OBJECT.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder?&'
already_seen = set()

mustChangeSemester = False
semester = ""

date_time = strftime("%Y-%m-%d %H%M", gmtime())
FILE_NAME = "fiu "+date_time+".csv"
file_lock = threading.Lock()
output_file = open(FILE_NAME, 'w')
output_file.write("Class Number, Campus, Class Name, Section Name, Instructor, Capacity, Enrolled, Available Seats, Wait List Capacity, Wait List Total")


#encoding
reload(sys)
sys.setdefaultencoding('utf8')

def log_entry(class_num,
        campus,
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
        output_file.write(("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (
        class_num,
        campus,
        class_name,
        section_name,
        instructor.replace(',', ';'),
        capacity,
        enrolled_num,
        available_seats,
        wait_list_capacity,
        wait_list_total,
        )).encode('utf8').replace('\n', ' ') + '\n')
        output_file.flush()
    except UnicodeEncodeError:
        print("goddammit with this")
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
        campus = driver.find_element_by_id('CAMPUS_TBL_DESCR').text
        log_entry(class_num, campus, class_name, section_name, instructor, capacity, enrolled_num, available_seats, wait_list_capacity, wait_list_total)
        back_button = driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_BACK')
        back_button.click()
        scraperhelpers.wait_for_stale_link(back_button)

def search_by_class_number(number, driver):
    if (mustChangeSemester == True):
        semester_select = driver.find_element_by_id('CLASS_SRCH_WRK2_STRM$35$')
        for option in semester_select.find_elements_by_tag_name('option'):
            if option.get_attribute('value') == semester:
                option.click()
                break

    course_number_select = driver.find_element_by_id('SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$4')
    for option in course_number_select.find_elements_by_tag_name('option'):
        if option.get_attribute('value') == 'C':
            option.click()
            break

    show_open_classes_toggle = driver.find_element_by_id('SSR_CLSRCH_WRK_SSR_OPEN_ONLY$7')
    if (show_open_classes_toggle.is_selected()):
        show_open_classes_toggle.click()

    course_career_select = driver.find_element_by_id('SSR_CLSRCH_WRK_ACAD_CAREER$5')
    for option in course_career_select.find_elements_by_tag_name('option'):
        if option.get_attribute('value') == 'UGRD':
            option.click()
            break

    course_number_input = driver.find_element_by_id('SSR_CLSRCH_WRK_CATALOG_NBR$4')
    course_number_input.clear()
    course_number_input.send_keys(number)
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
            print("too many in %s " % number)
    except common.exceptions.NoSuchElementException:
        click_through_classes(driver)

    try:
        new_search_button = driver.find_element_by_id('CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH')
        new_search_button.click()
        scraperhelpers.wait_for_stale_link(new_search_button)
    except common.exceptions.NoSuchElementException:
        pass


def get_semester():
    if (os.name == 'nt'):
        semesterdriver = webdriver.Chrome('chromedriver.exe')
    else:
        semesterdriver = webdriver.Chrome()

    semesterdriver.get(url)
    semesterdriver.get(url)

    try:
        search_iframe = semesterdriver.find_element_by_id('ptifrmtgtframe')
        semesterdriver.switch_to_frame(search_iframe)
    except common.exceptions.NoSuchElementException:
        pass

    semester_select = semesterdriver.find_element_by_id('CLASS_SRCH_WRK2_STRM$35$')
    for option in semester_select.find_elements_by_tag_name('option'):
        prompt = option.text, "y/n   "
        answer = raw_input(prompt)
        if (answer == "y"):
            if (option.get_attribute('selected') != 'selected'):
                global mustChangeSemester
                mustChangeSemester = True
                global semester
                semester = option.get_attribute('value')
            else:
                print "not already selected"
            break

    semesterdriver.close()


# lock acquisition specifically for getting length of stack
stack_lock = threading.Lock()
stack = deque(range(1000, 8000))


def spawn_driver():
    if (os.name == 'nt'):
        driver = webdriver.Chrome('chromedriver.exe')
    else:
        driver = webdriver.Chrome()
    driver.get(url)
    driver.get(url)
    stack_lock.acquire()
    while len(stack) > 0:
        number = stack.pop()
        stack_lock.release()
        while True:
            try:
                search_by_class_number("%03d" % number, driver)
            except:
                continue
            else:
                break
        while True:
            try:
                search_by_class_number("%03dL" % number, driver)
            except:
                continue
            else:
                break

        stack_lock.acquire()
        if len(stack) == 0:
            stack_lock.release()
    driver.close()

#get stupid semester
get_semester()

if (os.name == 'nt'):
    threadcount = 1
else:
    threadcount = 10

for num in range(threadcount):
    t = threading.Thread(target=spawn_driver)
    t.start()
