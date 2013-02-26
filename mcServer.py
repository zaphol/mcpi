#!/usr/bin/python
#Serve as single connection to Minecraft instance
#
#To avoid connection conflicts, any script connecting to the open minecraft should use
#
#from mcServer import mcpi
#
#and use 'mcpi' as minecraft instance


import minecraft as mc
mcpi = mc.Minecraft.create()

