import time
import os
import errno
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

def wait_for_stale_link(element):
	def link_stale():
		try:
			element.find_elements_by_id('whatever')
			return False
		except StaleElementReferenceException:
			return True
		except TimeoutException:
			return True
		except IOError as err:
			if (err.errno == 10048):
					print("10048")
					time.sleep(.50)
			return True


	start_time = time.time()
	while True:
		if link_stale():
			return True
