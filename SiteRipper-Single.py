# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 16:17:13 2019

@author: darp_lord
"""
import requests
from bs4 import BeautifulSoup
import os
import sys
from urllib.parse import urlparse, urljoin

def writeToFile(content,Dir,fName=None):
	if not os.path.exists(Dir):
		os.makedirs(Dir)
	if fName is None:
		fName=input("Enter filename: ")
	with open(os.path.join(Dir,fName),'a') as f:
		f.write(content)

def getResource(soup, parentTag, attr, sub_dir, link):
	parent=soup.find_all(parentTag)
	for tag in parent:
		try:
			res_link=urlparse(tag[attr])
			if(not res_link[0].startswith("http")):
				res_fname=res_link[2].split("/")[-1]
				res_dir=res_link[2][:-len(res_fname)]
				res=requests.get(urljoin(link,res_link[2])).text
				writeToFile(res,os.path.normpath(sub_dir+res_dir),res_fname)
		except Exception as e:
			print(e)
			continue
	
def ripIt(html_page,sub_dir,link):
	soup=BeautifulSoup(html_page,"lxml")
	#print(str(soup))
	writeToFile(soup.prettify(),sub_dir,"index.html")
	getResource(soup, "link", "href", sub_dir, link)
	getResource(soup, "script", "src", sub_dir, link)
	getResource(soup, "img", "src", sub_dir, link)
	
if __name__=="__main__":
	links=[]
	try:
		links+=[sys.argv[1]]
	except IndexError:
		while True:
			links+=[input("Enter Link, enter empty to end: ")]
			if links[-1]=="":
				break
	parent_dir=input("Enter parent directory(~/Documents/Sites/): ")
	   
	if(not os.path.isdir(parent_dir)):	
		parent_dir=os.path.expanduser("~")+"/Documents/Sites"

	for link in links:
		try:
			web_page=requests.get(link)
		except:
			continue
		urlDat=urlparse(link)
		urlLoc=urlDat[2][:-len(urlDat[2].split("/")[-1])]
		sub_dir=os.path.join(parent_dir,os.path.join(urlDat[1].replace(".","-"),urlLoc))
		html_page=web_page.content
		ripIt(html_page,sub_dir,link)
		print("Link:",link,"success")


