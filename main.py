import os
import re
from lib.modules import common
from lib.modules import epg

FilePath  = common.FilePath
OpenURL   = common.OpenURL
WriteFile = common.WriteFile

AiryAPI   = 'https://api.airy.tv/api/v2.1.0/channels?isIos=false&type=desktop&device=website&version=1.0'
LocalM3U8 = os.path.join(FilePath, 'airy_tv.m3u8')
LocalEPG  = os.path.join(FilePath, 'airy_tv.xml')

def Main():
	ids = []
	m3u8_entry     = '#EXTM3U8\n'
	xml_channels   = ''
	xml_programmes = ''
	r = OpenURL(AiryAPI)
	m = re.compile('\{"id":(.+?),"hls":.+?,"name":"(.+?)","number":(.+?),"private":.+?,"broadcasts":\[(.+?)\],"banner_url":.+?,"is_favorites":.+?,"source_url":"(.+?)"\}').findall(r)
	for tvgid, name, chno, guide, stream in m:
		if tvgid not in ids:
			ids.append(tvgid)
			name    = name.replace('_', ' ')
			stream  = stream.replace('\\', '')
			
			m3u8_channel = '#EXTINF:-1 tvg-id="%s" tvg-chno="%s",%s\n%s\n' % (tvgid, chno, name, stream)
			xml_channel  = '	<channel id="%s">\n		<display-name>%s</display-name>\n	</channel>\n' % (tvgid, name)
			xml_epg      = epg.EPGBuilder(tvgid, guide)
			
			m3u8_entry     = m3u8_entry   + m3u8_channel
			xml_channels   = xml_channels + xml_channel
			guide_data     = epg.EPGBuilder(tvgid, guide)
			xml_programmes = xml_programmes + guide_data
		
	WriteFile(LocalM3U8, m3u8_entry)
	WriteFile(LocalEPG, '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE tv SYSTEM "xmltv.dtd"><tv generator-info-name="www.github.com/RW1986">\n' + xml_channels + xml_programmes + '</tv>')
		
Main()