#!/usr/bin/python
#Pianobar event_command script

import sys, mcLibrary
import subprocess

try:
	tmp = open('/home/pi/minecraft/mcpi/api/python/mcpi/tmp')	
	tmp.close()
except:
	remote = subprocess.Popen(['python', '/home/pi/minecraft/mcpi/api/python/mcpi/hitblock.py'])
	print("instantiate")

def main():
	event = sys.argv[1]
	lines = sys.stdin.readlines()
	fields = dict([line.strip().split("=", 1) for line in lines])

	# fields: title, artist, album, songDuration, songPlayed, rating, stationName, pRet, pRetStr, wRet, wRetStr, rating
	artist = fields["artist"]
	title = fields["title"]

	if event == "songstart":
		if title:
			mcLibrary.mcSkyWrite(title + '\n' + 'by ' + artist, -50,43,-30,247)	
	elif event == "songmove":
		print("song moved!")

	

if __name__ == "__main__":
	main()
