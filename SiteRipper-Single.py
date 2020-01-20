# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 16:17:13 2019

@author: darp_lord
"""
import requests
from bs4 import BeautifulSoup
import os
import sys

def writeToFile(content,Dir,fName=None):
	if not os.path.exists(Dir):
		os.makedirs(Dir)
	if fName is None:
		fName=input("Enter filename: ")
	with open(os.path.join(Dir,fName),'a') as f:
		f.write(content)

def ripIt(html_pag,sub_dir,fName):
	soup=BeautifulSoup(html_page,"lxml")
	#print(str(soup))
	writeToFile(soup.prettify(),sub_dir,fName)
	css=soup.find_all("link")
	js=soup.find_all("script")
	for tag in css:
	    try:
	        res_link=tag['href']
	        if(not res_link.startswith("http")):
	            res_fname=res_link.split("/")[-1]
	            res_dir=res_link.split("/")[:-1]
	            res=requests.get(os.path.join(link,res_link)).content
	            writeToFile(res,os.path.join(sub_dir,res_dir),res_fname)
	    except:
	        continue
	for tag in js:
	    try:
	        res_link=tag['src']
	        if(not tag['src'].startswith("http")):
	            res_fname=res_link.split("/")[-1]
	            res_dir=res_link.split("/")[:-1]
	            res=requests.get(os.path.join(link,res_link)).content
	            writeToFile(res,os.path.join(sub_dir,res_dir),res_fname)
	    except:
	        continue
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
		sub_dir=os.path.join(parent_dir,link.split("/")[2].replace(".","-"))
		html_page=web_page.content
		ripIt(html_page,sub_dir,link.split("/")[-1])
		print("Link:",link,"success")


