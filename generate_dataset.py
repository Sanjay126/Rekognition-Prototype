from requests import exceptions
import requests
import argparse
import cv2
import os
from bs4 import BeautifulSoup as bs
import re
import urllib
import json
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())


MAX_RESULTS = 15
GROUP_SIZE = 1
URLsearch="https://www.google.com/search"


term = args["query"]+' cast IMDb'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'}
params = {"q": term, "ie":"utf-8", "oe":"utf-8"}

search = requests.get(URLsearch, headers=headers, params=params)
search.raise_for_status()

html = bs(search.text, 'html.parser')
imdb_url = html.find('div', class_="r").find("a")['href']
r = requests.get(imdb_url)
html = bs(r.text, 'html.parser')
odds = html.find_all('tr', class_="odd")
evens = html.find_all('tr', class_="even")
listOfCast = [i.find_all("td")[1].text for i in odds[:10]] + [i.find_all("td")[1].text for i in evens[:10]]
print("Generating dataset.........")
for cast in listOfCast:
	
	cast=cast.strip('\n')
	cast=cast.strip(' ')
	cast=cast.strip('\n')
	term=cast
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	params = {"q": term, "source":"lnms", "tbm":"isch"}
	
	search = requests.get(URLsearch, headers=headers, params=params)
	search.raise_for_status()
	soup = bs(search.text, 'html.parser')
	ActualImages = []
	outputPath=os.path.sep.join([args["output"],cast])
	if not os.path.isdir(outputPath):
		os.makedirs(outputPath)	
	totalImages=0
	for a in soup.find_all("div",{"class":"rg_meta"}):
		link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
		ActualImages.append((link,Type))
		totalImages+=1
		if totalImages>MAX_RESULTS:
			break
	term=cast+' look in '+args["query"]
	header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
	params = {"q": term, "source":"lnms", "tbm":"isch"}
	
	search = requests.get(URLsearch, headers=headers, params=params)
	search.raise_for_status()
	soup = bs(search.text, 'html.parser')
	totalImages=0
	for a in soup.find_all("div",{"class":"rg_meta"}):
		link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
		ActualImages.append((link,Type))
		totalImages+=1
		if totalImages>5:
			break
	for i , (img , Type) in enumerate(ActualImages):
		try:
			req = urllib.request.Request(img, headers=header)
			raw_img = urllib.request.urlopen(req).read()
			path=""
			if len(Type)==0:
				path=os.path.join(outputPath ,str(i).zfill(8)+".jpg")
				f = open(path, 'wb')
			else :
				path=os.path.join(outputPath ,str(i).zfill(8)+"."+Type)
				f = open(path, 'wb')


			f.write(raw_img)
			f.close()
		except Exception as e:
			pass
	