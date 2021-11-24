import os
import re
import urllib.error
import urllib.parse
import urllib.request

FilePath = os.getcwd()

def OpenURL(url):
	req      = urllib.request.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
	response = urllib.request.urlopen(req)
	link     = response.read()
	response.close()
	link     = link.decode('utf-8')
	return link

def OpenFile(file):
	data = open(file, 'r', encoding='utf-8')
	data = data.read()
	return data

def WriteFile(file, entry):
	data = open(file, 'w', encoding='utf-8')
	data.write(entry)
	data.close()

def AppendFile(file, entry):
	data = open(file, 'a', encoding='utf-8')
	data.write(entry)
	data.close()