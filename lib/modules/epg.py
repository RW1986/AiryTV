import os
import re
from datetime import datetime
from datetime import timedelta
from lib.modules import common

FilePath   = common.FilePath
WriteFile  = common.WriteFile
AppendFile = common.AppendFile

def EPGBuilder(tvgid, guide):
	guide_data = ''
	i = re.compile('\{"id":.+?,"title":"(.+?)","ads":.+?,"blockAds":.+?,"orderedAds":.+?,"description":(.+?),"view_duration":.+?,"stream_duration":(.+?),"view_start_at_iso":"(.+?)","stream_start_at_iso":".+?"\}').findall(guide)
	for name, plot, duration, start in i:
		start = start[0:19]
		frmt  = '%Y-%m-%dT%H:%M:%S'
		start = datetime.strptime(start, frmt)
		end   = start + timedelta(seconds=int(duration))
		if plot == 'null': description = ''
		else: description = '		<description>%s</description>\n' % plot.lstrip('"').rstrip('"')
		guide_entry = '	<programme channel="%s" start="%s +0000" stop="%s +0000">\n		<title>%s</title>\n%s	</programme>\n' % (tvgid, CleanTime(start), CleanTime(end), CleanString(name), CleanString(description))
		guide_data = guide_data + guide_entry
	return guide_data
		
def CleanTime(time):
	time = str(time)
	time = time.replace(':', '')
	time = time.replace('-', '')
	time = time.replace('T', '')
	time = time.replace(' ', '')
	return time
	
def CleanString(string):
	string = string.replace('\\/', '/')
	string = string.replace('_', ' ')
	return string