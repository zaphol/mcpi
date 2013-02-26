MinecraftPi
===========

Code used in Minecraft RaspberryPi Edition

Since only one script can be connected to a Minecraft instance at a time, I concocted a scheme of two file (a library and a server) which allow other functions to interact with a Minecraft instance without extra overhead or intereference issues. 

The mcLibrary.py file contains my custom minecraft functions. At present the only functions in there are to support SkyWriting but I'm hopeful I'll put time into more functions. 

How Pianobar Integration Works:
In the Pianobar config file it allows you to choose a script to run on each Pianobar event. The script should parse what type of event occurred and act accordingly. pianobar_eventcmd.py is my script which runs for each Pianobar event. If it detects a new song event it writes the title and artist name to the minecraft sky. It also ensures my hitblock.py script is running so that the remote control will always be available.

When the hitblock.py (I should find a better name) script runs it waits for a right-click event on a specific type of block. When it sees a right-click on that type of block it "opens a menu" and waits for the user to right-click a menu option. A menu selection is written to Pianobar's named pipe 'ctl'. The script checks every 20 seconds to make sure Pianobar is still running. (It's useless if Pianobar isn't running anymore)
