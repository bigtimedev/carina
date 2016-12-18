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
	while time.time() < start_time + 30:
		if link_stale():
			return True
		else:
			time.sleep(0.1)
	raise Exception('Timeout waiting for stale link')
