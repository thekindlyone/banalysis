# coding: utf-8
import requests
from bs4 import BeautifulSoup as bs
import re
import csv
from multiprocessing import Pool

r=requests.get('http://www.tblop.com/')
soup=bs(r.content,'lxml')
links=[(div.h2.text,[a.get('href') for a in div.findAll('a')]) for div in soup.findAll('div','a_list') if all(item not in div.h2.text.lower() for item in ['subreddit','tumblr','documentaries','software','addons','rapidshare'])]
def check_ban(args):
    site_type,url=args
    # print 'trying url ',url
    # rv=None
    try:
        r=requests.get(url,timeout=30)
        if len(r.text)<=300:
            rv= site_type,url,'Banned'
        else:
            rv= site_type,url,'Not Banned'
    except:
        rv= site_type,url,'ERROR'
    print rv
    return rv





urllist=[]
for site_type,urls in links:
    for url in urls:
        urllist.append( (site_type,url) )

p = Pool(35)
results=p.map(check_ban,urllist)


headers=['Type','URL','Result']
with open('report.csv','w') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(headers)
    writer.writerows(results)