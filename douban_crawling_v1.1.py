# TO RUN WITH PYTHON 2

import time

import requests 

import re

# use this module, OR add .encode('utf-8') to each line in the 2nd 'for' loop
import sys
import threading
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup as bs


filename = "my_douban.csv"
f = open(filename, "w")
headers = "movie,douban_link,date,rating,tag,comment\n"
f.write(headers)


for page in range(77):

	url = "https://movie.douban.com/people/<your username>/collect?start={}&sort=time&rating=all&filter=all&mode=grid".format(page*15)
	url_text = requests.get(url).text
	soup = bs(url_text, 'html.parser')
	douban_data = soup.find_all("div", {"class" : "item"})

	for item in douban_data:
		
		# movie name
		movie = item.find("div", {"class": "pic"}).find("a").get("title")
		print(movie)
		
		# douban link of the movie
		douban_link = item.find("li", {"class": "title"}).find("a").get("href")
		print(douban_link)
		
		# date
		date = item.find("span", {"class": "date"}).text
		print(date)
		
		# rating
		try: 
			rating = item.find("span", {"class": re.compile("^rating")}).get("class")[0][6] # find() returns a bs4.element.Tag, instead of text
		except AttributeError: # this error will happen when no rating is given
			rating = ""
		print(rating)
		
		# tag
		try: 
			tag = item.find("span", {"class": "tags"}).text[4:]
		except AttributeError: # this error will happen when no tag is given
			tag = ""
		print(tag)
		
		# comment
		try:
			comment = item.find("span", {"class": "comment"}).text
		except AttributeError: # this error will happen when no comment is given
			comment = ""
		print(comment)

		f.write(movie + "," + douban_link + "," + date + "," + rating + "," + tag + "," + comment + "\n")

		time.sleep(2)

f.close()
		
		
