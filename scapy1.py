from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import re
import csv
import requests
#from requests.exceptions import HTTPError


#################################################################################3
url1 = "http://www.drps.ed.ac.uk/19-20/dpt/cx_schindex.htm"

containers_schools = [] # 25 schools from 3 colleges
containers_course = [] # ~9k courses
containers_course_descriptor = [] # Descriptions of individual ~9k courses

f = csv.writer(open('schools.csv', 'w')) # url list of 25 schools
f.writerow(['Link'])
f1 = csv.writer(open('course_url.csv', 'w')) # url list of ~175 disciplines
f1.writerow(['Course_URL'])
f2 = csv.writer(open('course_description_url.csv', 'w')) # url list of ~9k Courses
f2.writerow(['Description_URL'])

uClient1 = urlopen(url1)
page_html1 = uClient1.read()
uClient1.close()
page_soup1 = soup(page_html1, "html.parser")
containers1 = page_soup1.find_all("a", href = True)

for link in containers1:
    names1 = link ['href']
    #print (type(names))
    if "cx_s_su" in names1:
        containers_schools.append('http://www.drps.ed.ac.uk/19-20/dpt/'+link ['href'])
        f.writerow(['http://www.drps.ed.ac.uk/19-20/dpt/'+link ['href']])
#################################################################################

#################################################################################
print ("Total # of Schools" + str(len(containers_schools)))

for slink in containers_schools:
    url = slink
    print (url)

    r = requests.get(url)
    if r.status_code != 404:
        uClient = urlopen(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        containers = page_soup.find_all("a", href = True)

        for link in containers:
            names = link ['href']
            #print (type(names))
            if "cx_sb_" in names:
                if not ("cx_sb_accp.htm" in names):
                    containers_course.append('http://www.drps.ed.ac.uk/19-20/dpt/'+link ['href'])
                    f1.writerow(['http://www.drps.ed.ac.uk/19-20/dpt/'+link ['href']])

# #################################################################################

print ("Total # of disciplines" + str(len(containers_course)))

for slink in containers_course:
    url = slink
    print (url)

    r = requests.get(url)
    if r.status_code != 404:
        uClient = urlopen(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        containers = page_soup.find_all("a", href = True)

        for link in containers:
            names = link ['href']
            #print (type(names))
            if "cx" in names:
                if not ("_" in names):
                    if not ("bich10001" in names):
                        containers_course_descriptor.append('http://www.drps.ed.ac.uk/19-20/dpt/'+link ['href'])
                        f2.writerow(['http://www.drps.ed.ac.uk/19-20/dpt/'+link ['href']])

######################################################################################


for slink in containers_course_descriptor:
    url = slink
    filename = url[-13:-4] + '.txt'
    print (url)
    print (filename)

    r = requests.get(url)
    if r.status_code != 404:
        uClient = urlopen(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        containers = page_soup.find_all("table", {"class":"sitstablegrid"})

        ftext = open(filename, 'w');
        output = ''
        blacklist = [
        	'[document]',
        	'noscript',
        	'header',
        	'html',
        	'meta',
        	'head',
        	'input',
        	'script',
        	# there may be more elements you don't want, such as "style", etc.
        ]

        for t in containers:
            if t.parent.name not in blacklist:
                output += '{} '.format(t)
                ftext.write(output)
