# -*- coding: utf-8 -*-
import urllib2 as web_walker
from bs4 import BeautifulSoup
import csv

"""
FAQ:
Q: Can I upload images with this app?
A: Not yet.
UPD: In that moment you can see image's links

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
    """ver:0002"""

    def __init__(self, link, data):
        self.link = link
        self.data = data

    def link_checker(self, link_in):
        if link_in.startswith('/'):
            out_link = self.link+link_in
            print "GOTCHA"

        else:
            out_link = link_in

        return out_link

    def tagSoup(self, target_link):
        strike = web_walker.Request(target_link)
        strike.add_header(
            'User-Agent',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
        )
        out = web_walker.urlopen(strike)
        soup = BeautifulSoup(out.read(), 'lxml')

        return soup

    def loop_linker(self):
        linker_container = []

        for tag in self.tagSoup(self.link).find_all('a'):
            try:
                link_to_page = self.link_checker(tag.attrs['href'])
                if link_to_page not in linker_container\
                        and self.link in link_to_page:
                    linker_container.append(link_to_page)
            except KeyError:
                pass

        return linker_container

    def tag_loop(self, target_obj, elem, io):
        out_values = []
        for tag in self.tagSoup(target_obj).find_all(elem):
            if io == 0:
                value = tag.text.encode('utf-8')
            else:
                value = tag.attrs['src']

            # out_value = value.encode('utf-8')
            if value not in out_values:
                out_values.append(value)

        return out_values

    @property
    def body_checker(self):
        file_ = open(self.data, 'w')
        writer = csv.writer(file_, delimiter=',')
        post_counter = 0

        for item in self.loop_linker():
            if item is not None:

                print item
                try:
                    title = ''
                    for header in self.tag_loop(item, 'h1', 0):
                        title = header
                        break

                    post = ''
                    for text in self.tag_loop(item, 'p', 0):
                        post = post+text+'\n'
                    print post

                    img_set = ''
                    for img in self.tag_loop(item, 'img', 1):
                        if img.startswith('/') and 'www' not in img:
                            img_set = img_set+self.link+img+'\n'
                        elif 'facebook.com' not in img\
                                and 'twitter' not in img:
                            img_set = img_set+img+'\n'

                    print img_set

                    if len(post.replace(' ', '').replace('\n', '')) < 200:
                        break
                    if title != '':
                        writer.writerow([title, post, img_set])
                    post_counter += 1

                except TypeError:
                    pass
                except KeyError:
                    pass

        file_.close()

        return "Obtained %d items" % post_counter

crawler = PostCrawler(link="http://www.segodnya.ua", data='segodnya.csv')
print crawler.body_checker

# http://www.independent.co.uk ^^
# https://www.thetimes.co.uk/ ^^
# http://www.segodnya.ua ^^
