# -*- coding: utf-8 -*-
import urllib2 as web_walker
from bs4 import BeautifulSoup
import csv

"""
FAQ:
Q: Can I upload images with this app?
A: Not yet.

Q: Where i can find result csv?
A: In the same folder where you save this script.

Q: May i use it for free?
A: Yes, you can.

Q: How i can run it?
A: Go to the folder with script in console and type: python main.py

Q: I have an error ( "No Module Named bs4.")
A: You need to install BeautifulSoup (pip install bs4)


"""

class PostCrawler:
	'This is alpha version of context crawler with search deep = 1'

	def __init__(self, link, data):
		self.link = link
		self.data = data


	def link_checker(self, link_in):

		if link_in.startswith('/'):
			out_link =  self.link+link_in
			print "GOTCHA"

		else:
			out_link = link_in

		return out_link


	@property
	def link_watcher(self):
			
		strike = web_walker.Request(self.link)
		strike.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
		out = web_walker.urlopen(strike)
		soup = BeautifulSoup(out.read(), 'lxml')		
		link_container = []
		titles =[]
		file_ = open(self.data, 'w')		
		writer = csv.writer(file_, delimiter=',')

		for tag in soup.find_all('a'):

			post =''
			title=''
			text = []

			print tag.attrs['href']			

			if tag.attrs['href'] not in link_container:
				
				item_link = self.link_checker(tag.attrs['href'])
				print item_link
			
				try:
					req_item = web_walker.Request(item_link)
					req_item.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
					inner = web_walker.urlopen(req_item)
					title_soup = BeautifulSoup(inner.read(), 'lxml')
					link_container.append(tag.attrs['href'])
											
					for tag in title_soup.find_all('h1'):
						if len(tag.text)>3 and '404' not in tag.text:
							title = tag.text
							titles.append(tag.text)
							
					print title

					# Good title  == long title
					if len(title)<4:
						break
					
					for tag in title_soup.find_all('p'):
						text.append(tag.text)
					
					for item in text:
						post = post+item+'\n'

					# I think that less then 200 characters in post it's not enought
					if len(post.replace(' ','').replace('\n', ''))<200:
						break

					writer.writerow([title.encode('utf-8'), post.encode('utf-8')])
								
				except Exception:
					pass
		

		file_.close()
		
		return titles


crawler = PostCrawler(link="http://www.segodnya.ua", data = 'segodnya.csv')
crawler.link_watcher

# http://www.independent.co.uk ^^
# https://www.thetimes.co.uk/ ^^
# http://www.segodnya.ua ^^


