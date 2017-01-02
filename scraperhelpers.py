import time
from selenium.common.exceptions import StaleElementReferenceException

def wait_for_stale_link(element):
	def link_stale():
		try:
			element.find_elements_by_id('whatever')
			return False
		except StaleElementReferenceException:
			return True

	start_time = time.time()
	while True:
		if link_stale():
			return True
