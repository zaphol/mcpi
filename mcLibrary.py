#!/usr/bin/python
#Minecraft Library of Functions

import sys, time, os
from mcServer import mcpi


################## Letter Definitions ##################
## Each letter is a list which pixels in a 3x5 grid to place 
blank = [0]
A = [1,3,4,6,7,8,9,10,12,14]
B = [1,2,4,6,7,8,10,12,13,14]
C = [2,3,4,7,10,14,15]
D = [1,2,4,6,7,9,10,12,13,14]
E = [1,2,3,4,7,8,10,13,14,15]
F = [1,4,7,8,10,13,14,15]
G = [2,3,4,6,7,10,14,15]
H = [1,3,4,6,7,8,9,10,12,13,15]
I = [1,2,3,5,8,11,13,14,15]
J = [2,4,6,9,12,15]
K = [1,3,4,6,7,8,10,12,13,15]
L = [1,2,3,4,7,10,13]
M = [1,3,4,6,7,8,9,10,11,12,13,15]
N = [1,3,4,6,7,8,9,10]
O = [2,4,6,7,9,10,12,14]
P = [1,4,7,8,10,12,13,14]
Q = [3,5,7,9,10,12,14]
R = [1,3,4,6,7,8,10,12,13,14]
S = [1,2,6,8,9,10,14,15]
T = [2,5,8,11,13,14,15,]
U = [1,2,3,4,6,7,9,10,12,13,15]
V = [2,4,6,7,9,10,12,13,15]
W = [1,3,4,5,6,7,9,10,12,13,15]
X = [1,3,4,6,8,10,12,13,15]
Y = [2,5,8,10,12,13,15]
Z = [1,2,3,4,8,12,13,14,15]
one = [1,2,3,5,8,10,11,14]
two = [1,2,3,4,8,12,13,14]
three = [1,2,6,7,8,12,13,14]
four = [3,6,7,8,9,10,12,13,15]
five = [1,2,6,7,8,9,10,13,14,15]
six = [1,2,3,4,6,7,8,9,10,13,14,15]
seven = [2,5,8,12,13,14,15]
eight = [1,2,3,4,6,7,8,9,10,12,13,14,15]
nine = [3,6,7,8,9,10,12,13,14,15]
zero = [1,2,3,4,6,7,9,10,12,13,14,15]
openparen = [2,3,4,5,7,10,11,14,15]
closeparen = [1,2,5,6,9,11,12,13,14]
exclamation = [2,8,11,14]
forslash = [1,4,5,8,11,12,15]
backslash = [3,5,6,8,10,11,13]
question = [2,8,12,13,14]
plus = [5,7,8,9,11]
minus = [7,8,9]
comma = [2,4,5]
openbracket = [1,2,3,4,7,10,13,14,15]
closebracket = [1,2,3,6,9,12,13,14,15]
colon = [5,11]
semicolon = [1,5,11]
quotes = [10, 12, 13, 15]
apostrophe = [10,14]


## Dictionary to key lower case characters to lists defined above
abc = {'a': A, 'b': B, 'c': C, 'd': D, 'e': E, 'f': F, 'g': G, 'h': H, 'i': I, 'j': J, 'k': K, 'l': L, 'm': M, 'n': N, 'o': O, 'p': P, 'q': Q, 'r': R, 's': S, 't': T, 'u': U, 'v': V, 'w': W, 'x': X, 'y': Y, 'z': Z, ' ': blank, '1': one, '2': two, '3': three, '4': four, '5': five, '6': six, '7': seven, '8': eight, '9': nine, '0': zero, '(': openparen, ')': closeparen, '!': exclamation, '/': forslash, '//': backslash, '?': question, '+': plus, '-': minus, str(','): comma, '[': openbracket, ']': closebracket, str(':'): colon, ';': semicolon, '"': quotes, str('\''): apostrophe}

def drawLetter(Letter,x,y,z,blockID):
#Using a 3x5 grid of pixels, place a block in each one called out by
#list of pixels for the letter passed in
	mcpi.setBlocks(x,y,z,x+2,y+4,z,0)
	
	if 1 in Letter:
		mcpi.setBlock(x,y,z,blockID)
	if 2 in Letter:
		mcpi.setBlock(x+1,y,z,blockID)
	if 3 in Letter:
		mcpi.setBlock(x+2,y,z,blockID)
	if 4 in Letter:
		mcpi.setBlock(x,y+1,z,blockID)
	if 5 in Letter:
		mcpi.setBlock(x+1,y+1,z,blockID)
	if 6 in Letter:
		mcpi.setBlock(x+2,y+1,z,blockID)
	if 7 in Letter:
		mcpi.setBlock(x,y+2,z,blockID)
	if 8 in Letter:
		mcpi.setBlock(x+1,y+2,z,blockID)
	if 9 in Letter:
		mcpi.setBlock(x+2,y+2,z,blockID)
	if 10 in Letter:
		mcpi.setBlock(x,y+3,z,blockID)
	if 11 in Letter:
		mcpi.setBlock(x+1,y+3,z,blockID)
	if 12 in Letter:
		mcpi.setBlock(x+2,y+3,z,blockID)
	if 13 in Letter:
		mcpi.setBlock(x,y+4,z,blockID)
	if 14 in Letter:
		mcpi.setBlock(x+1,y+4,z,blockID)
	if 15 in Letter:
		mcpi.setBlock(x+2,y+4,z,blockID)

def mcSkyWrite(sinput,x,y,z,blockID):
#Break string into words, decide where to place each word and letter	
	#Set z height of top line and number of chars per line
	topline = 50
	linewidth = 15	

	line = 0          #line number
	characters = 0	  #number of characters already on the line
	words = sinput.lower().split(" ")
	for word in words: #for each word in the string
		if (characters + len(word)) > linewidth:  #the word is too long for the current line
			#clear rest of line, move to the next line, reset characters count	
			mcpi.setBlocks(x+characters*4,topline-7*line,z,x+linewidth*4,topline-7*line+5,z,0)
			line = line + 1
			characters = 0	
		for letter in word:  #for each character in the current word
			if letter == '\n':  #start on the next line
				#clear rest of line, move to next line, reset characters count
				mcpi.setBlocks(x+characters*4,topline-7*line,z,x+linewidth*4,topline-7*line+5,z,0)
				line = line + 1
				characters = 0
			else:
				try:    #drawing the letter
					drawLetter(abc[letter],x+characters*4,topline-7*line,z,blockID)
				except: #When the letter is not in dict abc[], draw a blank
					drawLetter(abc[' '],x+characters*4,topline-7*line,z,blockID)
				characters = characters + 1	
		#After each word
		drawLetter(blank, x+characters*4, topline-7*line, z, blockID)
		characters = characters + 1
	#After all words are drawn, clear the rest of the current line and the next few lines
	mcpi.setBlocks(x+characters*4,topline-7*line,z,x+linewidth*4,topline-7*line+5,z,0)
	line = line + 1
	characters = 0
	mcpi.setBlocks(x+characters*4,topline-7*line,z,x+linewidth*4,topline-7*line+5,z,0)
	line = line + 1
	mcpi.setBlocks(x+characters*4,topline-7*line,z,x+linewidth*4,topline-7*line+5,z,0)
	line = line + 1
	mcpi.setBlocks(x+characters*4,topline-7*line,z,x+linewidth*4,topline-7*line+5,z,0)

