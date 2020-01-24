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
	try:
		Tfile=open(os.path.join(Dir,fName),'r')
		Tfile.close()
	except FileNotFoundError:
		with open(os.path.join(Dir,fName),'w') as f:
			f.write(content)

def getResource(soup, parentTag, attr, sub_dir, link):
	parent=soup.find_all(parentTag)
	for tag in parent:
		try:
			#print(tag)
			res_link=urlparse(tag[attr])
			if(not (res_link[0].startswith("http") or res_link[2]=="")):
				res_fname=res_link[2].split("/")[-1]
				res_dir=res_link[2][:-len(res_fname)]
				#print(res_link)
				#print(res_link)
				print(link, urljoin(link,res_link[2]), res_link[2])
				res=requests.get(urljoin(link,res_link[2])).text
				#print(res)
				writeToFile(res,os.path.normpath(sub_dir+res_dir),res_fname)
		except Exception as e:
			#print(e)
			continue
	
def ripIt(html_page,sub_dir,link):
	soup=BeautifulSoup(html_page,"lxml")
	#print(str(soup))
	if(not (link.endswith(".html") and link.endswith(".php"))):
		if not link.endswith("/"):
			link+="/"
		sub_dir+="/"+link.split("/")[-2]+"/"
		fName="index.html"
	else:
		fName=link.split("/")[-1]
		
		
	writeToFile(soup.prettify(),sub_dir,fName)
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
	#parent_dir=input("Enter parent directory(~/Documents/Sites/): ")
	   
	
	parent_dir=os.path.expanduser("~")+"/Documents/Sites"
	if(not os.path.isdir(parent_dir)):	
		os.mkdir(parent_dir)
	for link in links:
		try:
			web_page=requests.get(link)
		except:
			continue
		urlDat=urlparse(link)
		urlLoc=urlDat[2][:-len(urlDat[2].split("/")[-1])]
		#print(urlDat)
		sub_dir=os.path.join(parent_dir,os.path.normpath(urlDat[1].replace(".","-")+urlLoc))
		#print(parent_dir, sub_dir)
		html_page=web_page.content
		ripIt(html_page,sub_dir,link)
		print("\nSucess:",link,"\nCheck in ~/Documents/Sites/")


