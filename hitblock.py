#!/usr/bin/python
#Pianobar Remote Control
#
#Converts block hit events in a running minecraft session into commands which are sent to Pianobar
#
#The player right-clicks a specific type of block which activates a 'menu'
#The menu is an arrangement of colored blocks which can be right-clicked 
#Buttons:
#  P = Play/Pause  N = Next Song  Vu/d = Volume up/down  Tu/d = Thumbs up/down
#
#  _   _  |Vu|  |Tu|
# |P| |N|  
#         |Vd|  |Td|  

import sys, time, os
from subprocess import Popen, PIPE
from mcServer import mcpi


#When the script runs, tmp file exists
#scripts calling this one should check if this file exists
tmp = open("/home/pi/minecraft/mcpi/api/python/mcpi/tmp", "a")
tmp.write("Pianobar Remote Running")
tmp.close()

#set which block type to hit to open the menu
BlockToOpenMenu = 12
menutimeout = 20	#Menu timeout in seconds

def isThisProcessRunning( process_name ):
#Given a process name, search the ps list
#If the named process shows up, return True, else False

	ps = Popen("ps -e | grep "+process_name, shell=True, stdout=PIPE)
	outstring = ps.communicate()[0]

	if not outstring:
		output = False
	else: output = True

	return output


#setup variables for main loop
exit = False 	#exit for main while loop, if Pianobar isn't running program should exit
paused = False	#variable to keep track of play/pause state of Pianobar. Could easily get out of sync
counter = 0
PianobarRunning = isThisProcessRunning('pianobar')


#main loop wating for block hit events, should exit if pianobar is not running
while not exit | (not PianobarRunning):
	hits = mcpi.events.pollBlockHits()
	
	if len(hits) > 0: 
	#A hit event happened, Let's see what type of block was hit
		hitblock = str(hits[0]).split(",")
		blockID = mcpi.getBlock(int(hitblock[1]), int(hitblock[2]), int(hitblock[3]))
		PianobarRunning = isThisProcessRunning('pianobar')
		
		if (blockID == BlockToOpenMenu) & PianobarRunning: #Ensure Pianobar is still running
		#The hit block was correct! Open the menu!
			menuPos = int(hitblock[1]), int(hitblock[2]), int(hitblock[3])
			
			Ppos = menuPos[0] - 2, menuPos[1] + 1, menuPos[2] - 2
			Npos = menuPos[0], menuPos[1] + 1, menuPos[2] - 2
			Vupos = menuPos[0] + 2, menuPos[1] + 2, menuPos[2] - 2
			Vdpos = menuPos[0] + 2, menuPos[1] + 0, menuPos[2] - 2
			Tupos = menuPos[0] + 4, menuPos[1] + 2, menuPos[2] - 2
			Tdpos = menuPos[0] + 4, menuPos[1] + 0, menuPos[2] - 2

			#Keep track of what block types we are replacing
			Pblock = mcpi.getBlock(Ppos[0], Ppos[1], Ppos[2])	#Green/Red - Play/Pause
			Nblock = mcpi.getBlock(Npos[0], Npos[1], Npos[2])	#Orange - Next	
			Vublock = mcpi.getBlock(Vupos[0], Vupos[1], Vupos[2])	#Pink - Volume up
			Vdblock = mcpi.getBlock(Vdpos[0], Vdpos[1], Vdpos[2])	#Gray - Volume Down
			Tublock = mcpi.getBlock(Tupos[0], Tupos[1], Tupos[2])	#White - Thumbs up song
			Tdblock = mcpi.getBlock(Tdpos[0], Tdpos[1], Tdpos[2])	#Black - Thumbs down song
			
			#Setup menu blocks
			mcpi.setBlock(menuPos[0], menuPos[1], menuPos[2], 246)
			if paused == False:
				mcpi.setBlock(Ppos[0], Ppos[1], Ppos[2], 35, 5)  	#Green - Playing
			else: 	mcpi.setBlock(Ppos[0], Ppos[1], Ppos[2], 35, 14)  	#Red - Paused
			mcpi.setBlock(Npos[0], Npos[1], Npos[2], 35, 1)			#Orange - Next	
			mcpi.setBlock(Vupos[0], Vupos[1], Vupos[2], 35, 6)		#Pink - Volume up
			mcpi.setBlock(Vdpos[0], Vdpos[1], Vdpos[2], 35, 8)		#Gray - Volume Down
			mcpi.setBlock(Tupos[0], Tupos[1], Tupos[2], 35, 0)		#White - Thumbs up song
			mcpi.setBlock(Tdpos[0], Tdpos[1], Tdpos[2], 35, 15)		#Black - Thumbs down song
			mcpi.postToChat("Pause, Next, Volume, Thumbs up/down")

			#Menu interactions
			#Menu stays open for 20 seconds of inactivity
			menuOpen = True
			counter = 0
			countertimeout = menutimeout*10
			while menuOpen:
				hits = mcpi.events.pollBlockHits()
				if counter >= countertimeout:
					menuOpen = False

				if len(hits) > 0: 
				#There was a hit, if the menu was hit let's handle it
					hitblock = str(hits[0]).split(",")
					hitPos = int(hitblock[1]), int(hitblock[2]), int(hitblock[3])
					pianobar = open("/home/pi/.config/pianobar/ctl", 'w')

					if hitPos == (Ppos[0], Ppos[1], Ppos[2]):
						counter = 0
						pianobar.write("p")

						if paused == False:
							paused = True
							mcpi.postToChat("Paused")
							mcpi.setBlock(Ppos[0], Ppos[1], Ppos[2], 35, 14)  	#Red - Paused
						else:
							paused = False
							mcpi.postToChat("Play")
							mcpi.setBlock(Ppos[0], Ppos[1], Ppos[2], 35, 5)  	#Green - Playing
					
					elif hitPos == (Npos[0], Npos[1], Npos[2]):
						counter = 0
						mcpi.postToChat("Next Song")
						pianobar.write("n")
						time.sleep(0.5)
						paused = False
						mcpi.setBlock(Ppos[0], Ppos[1], Ppos[2], 35, 5)  	#Green - Playing

					elif hitPos == (Vupos[0], Vupos[1], Vupos[2]):
						counter = 0
						mcpi.postToChat("Volume Up")
						pianobar.write(")")

					elif hitPos == (Vdpos[0], Vdpos[1], Vdpos[2]):
						counter = 0
						mcpi.postToChat("Volume Down")
						pianobar.write("(")

					elif hitPos == (Tupos[0], Tupos[1], Tupos[2]):
						counter = 0
						mcpi.postToChat("Thumbs Up!")
						pianobar.write("+")
						
					elif hitPos == (Tdpos[0], Tdpos[1], Tdpos[2]):
						counter = 0
						mcpi.postToChat("Thumbs down...")
						pianobar.write("-")
						
					elif hitPos == menuPos:
					
						menuOpen = False
				
					pianobar.close()
				
				if menuOpen == False:
					#Close menu
					mcpi.setBlock(Ppos[0], Ppos[1], Ppos[2], Pblock)  	#Green - Play/Pause
					mcpi.setBlock(Npos[0], Npos[1], Npos[2], Nblock)	#Orange - Next	
					mcpi.setBlock(Vupos[0], Vupos[1], Vupos[2], Vublock)	#Pink - Volume up
					mcpi.setBlock(Vdpos[0], Vdpos[1], Vdpos[2], Vdblock)	#Gray - Volume Down
					mcpi.setBlock(Tupos[0], Tupos[1], Tupos[2], Tublock)	#White - Thumbs up song
					mcpi.setBlock(Tdpos[0], Tdpos[1], Tdpos[2], Tdblock)	#Black - Thumbs down song
					mcpi.setBlock(menuPos[0], menuPos[1], menuPos[2], BlockToOpenMenu)
					counter = 0
				counter = counter + 1
				time.sleep(0.1)
		elif not PianobarRunning:
			exit = True
	
	if counter > 300:
		PianobarRunning = isThisProcessRunning('pianobar')
		counter = 0
	counter = counter + 1
	time.sleep(0.1)


try:
	x = Popen(['rm', '/home/pi/minecraft/mcpi/api/python/mcpi/tmp'])
except:
	x = 0	

