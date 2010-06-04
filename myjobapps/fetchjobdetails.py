__author__ = "James Baster (james@jarofgreen.co.uk)"
__copyright__ = "(C) 2009 James Baster. GNU GPL 3."

import urllib
import html2text
import re

def fetch(url):
	# part 1: get data
	f = urllib.urlopen(url)
	data = f.read()

	p = re.compile('<title>([^<]*)</title>')
	title = p.search(data).group(1)
	# part 2: any url specific dividing we can do now?


	# part 3: strip tags, and white space chars
	data = html2text.html2text(data, url)
	
	# part 4: any more url specific dividing we can do now?


	# part 5: finally done
	return (title,data)



