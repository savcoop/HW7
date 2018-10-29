# To run this, you need to install BeautifulSoup if you aren't using anaconda
# https://pypi.python.org/pypi/beautifulsoup4

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import unittest
import re 

def getSumSpans(url):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False 
	ctx.verify_mode = ssl.CERT_NONE

	html = urlopen(url, context =ctx).read()
	soup = BeautifulSoup(html, 'html.parser')
	span_tags = soup.find_all('span')
	total = 0 
	for n in span_tags:
		nums = re.findall(r'\b\d+\b', n.text)
		for x in nums:
			total += int(x)
	return total


def followLinks(url, numAnchor, numTimes):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False 
	ctx.verify_mode = ssl.CERT_NONE

	html = urlopen(url, context =ctx).read()

	list_of_names = []
	for x in range(numTimes): 
		soup = BeautifulSoup(html, 'html.parser')
		a_tag = soup.find_all('a')
		new_link = a_tag[numAnchor-1]
		list_of_names.append(new_link.text)
		new_url = new_link['href']
		
		html = urlopen(new_url, context =ctx).read()

	return list_of_names[-1]
    

def getGradeHistogram(url):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False 
	ctx.verify_mode = ssl.CERT_NONE

	html = urlopen(url, context =ctx).read()
	soup = BeautifulSoup(html, 'html.parser')
	span_tags = soup.find_all('span')
	grades = {} 
	for n in span_tags:
		nums = re.findall(r'\b\d+\b', n.text)
		for x in nums:
			if len(x) > 1: 
				g_range = int(x[0]) * 10
			else: 
				g_range = 0 

			if g_range not in grades:
				grades[g_range] = 1 
			else: 
				grades[g_range] += 1 

	t_list = sorted(list(grades.items()), reverse = True)
	return t_list

    


class TestHW7(unittest.TestCase):

    def test_sumSpan1(self):
        self.assertEqual(getSumSpans("http://py4e-data.dr-chuck.net/comments_42.html"), 2553)

    def test_sumSpan2(self):
        self.assertEqual(getSumSpans("http://py4e-data.dr-chuck.net/comments_132199.html"), 2714)

    def test_followLinks1(self):
        self.assertEqual(followLinks("http://py4e-data.dr-chuck.net/known_by_Fikret.html",3,4), "Anayah")

    def test_followLinks2(self):
        self.assertEqual(followLinks("http://py4e-data.dr-chuck.net/known_by_Charlie.html",18,7), "Shannah")

    def test_getGradeHistogram(self):
       self.assertEqual(getGradeHistogram("http://py4e-data.dr-chuck.net/comments_42.html"), [(90, 4), (80, 4), (70, 7), (60, 7), (50, 6), (40, 3), (30, 5), (20, 4), (10, 6), (0, 4)])


unittest.main(verbosity=2)
