from lxml import html
import requests

# hit the peoplesoft whining page babe
url = 'https://pslinks.fiu.edu/psc/cslinks/EMPLOYEE/CAMP/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL&FolderPath=PORTAL_ROOT_OBJECT.HC_CLASS_SEARCH_GBL&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder?&'
page = requests.get(url)

# grab all the cookies babe
sendcookies = {}
sendcookies['TS0132f89f']=page.cookies['TS0132f89f']
sendcookies['TS017a172d']=page.cookies['TS017a172d']
sendcookies['pscsdkweb01-PORTAL-PSJSESSIONID']=page.cookies['pscsdkweb01-PORTAL-PSJSESSIONID']

# get to the search page babe
searchpage = requests.get(url, cookies=sendcookies)
searchtree = html.fromstring(searchpage.content)

# for each menu item babe
rootxpath = '//*[@id="SSR_CLSRCH_WRK_ACAD_ORG$2"]'
i = 1
while(1):
	subxpath = rootxpath + '/option['+str(i)+']'
	result = searchtree.xpath(subxpath)
	if (len(result)>0):
		print 'item ', i, ': ', result[0].text
		i = i+1
	else:
		break
