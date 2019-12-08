# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 16:17:13 2019

@author: darp_lord
"""
import requests
from bs4 import BeautifulSoup
import os
import sys

def writeToFile(soup,fName=None,Dir=os.path.expanduser("~")+"/Documents/Sites"):
	if not os.path.exists(Dir):
		os.makedirs(Dir)
	if fName is None:
		fName=input("Enter filename: ")
	with open(Dir+"/"+fName+".txt",'a') as f:
		f.write(soup.prettify())

if __name__=="__main__":
	links=[]
	try:
		links+=[sys.argv[1]]
	except IndexError:
		while True:
			links+=[input("Enter Link, enter empty to end: ")]
			if links[-1]=="":
				break

	for link in links:
		try:
			web_page=requests.get(link)
		except:
			continue
		html_page=web_page.content
		soup=BeautifulSoup(html_page,"lxml")
		#print(str(soup))
		writeToFile(soup,link.split("/")[2].replace(".","-"))
		print("Link:",link,"success")


