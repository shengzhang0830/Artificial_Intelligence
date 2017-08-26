# Web Scraper - Douban Movie Sites

# Import libraries
import urllib
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv

# Specify output file
csvfile = file('douban_2016.csv','wb')
writer = csv.writer(csvfile)

total_list = list()

# Loop through urls
for i in range(1988,2016):
	for j in range(0,100):
		
		fhand = urllib.urlopen('https://movie.douban.com/tag/'+ str(i) +'?start='+ str(j*20) +'&type=O')

		# Parse the html with BeautifulSoup
		html = fhand.read()
		soup = BeautifulSoup(html, "lxml")

		# Extract useful information (movie genre, movie rating, number of ratings, etc.)
		try:
			divTag = soup.find_all("div", {"class":"pl2"})
			for k in range(0,20):
				components = str(divTag[k]).split('>')
				print k
				writer.writerow(components)
		except:
			continue

csvfile.close()
