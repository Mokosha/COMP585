#	StickyPy - Stick Figure Animator
#	Copyright (C) 2009 Joshua Worth
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame, sys
import cProfile

from copy import deepcopy
from math import *

from defs import *
from objs import *
from app import *

import thread

pygame.init()

version = "Alpha 20"

screensize = Vector([1024,768])
pygame.display.set_icon(pygame.image.load("splogoicon.png"))
pygame.display.set_caption("StickyPy")
screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)# + pygame.HWSURFACE + pygame.DOUBLEBUF)

def main(screen):
	sys.setrecursionlimit(10000)
	pygame.key.set_repeat(250, 25)
	#print pygame.NOEVENT
	#pygame.time.set_timer(1, 300)
	
	canvaspos = Vector(200,50)
	canvassize = screensize-canvaspos
	canvas = pygame.Surface(canvassize)
	limb = dict(ang=KeyFrame(0), dist=KeyFrame(0), pos=KeyFrame(Vector(0,0)), shape=Texture(shape="line"), width=KeyFrame(7), colour=KeyFrame([0,0,0]), cartesian=KeyFrame(False, False, "const"), static=KeyFrame(False, False, "const"), hidden=KeyFrame(False, False, "const"), children=[])
	
#	StickMan = dict(limb, pos=Vector(canvassize[0]/2, canvassize[1] / 2), ang=90, top=True, children=[
#					dict(limb, ang=KeyFrame([[1, 270],[100,470],[200,1000],[120,480]]), dist=KeyFrame([[1,60],[50,20],[100,200],[150,1000]]), children=[
#								dict(limb, ang=0, dist=36, shape=1),
#								dict(limb, ang=135, dist=40, children=[
#											dict(limb, ang=15, dist=40)
#								]),
#								dict(limb, ang=225, dist=40, children=[
#											dict(limb, ang=-15, dist=40)
#								])
#					]),
#					dict(limb, ang=67, dist=50, colour=KeyFrame([[1,(0,0,0)],[200,(255,0,0)]]), children=[
#								dict(limb, ang=0, dist=50)
#					]),
#					dict(limb, ang=113, dist=50, width=KeyFrame([[1,7], [20,25], [40, 7]]), children=[
#								dict(limb, ang=0, dist=50)
#					])
#			])
	
	# Define the default StickMan
	StickMan = dict(deepcopy(limb), pos=KeyFrame(Vector(640/2, 480 / 2)), ang=KeyFrame(90), cartesian=KeyFrame(True, False, "const"), hidden=KeyFrame(True, False, "const"), children=[
					dict(deepcopy(limb), ang=KeyFrame(270), dist=KeyFrame(60), children=[
								dict(deepcopy(limb), ang=KeyFrame(0), dist=KeyFrame(36), shape=Texture(shape="circle")),
								dict(deepcopy(limb), ang=KeyFrame(135), dist=KeyFrame(40), children=[
											dict(deepcopy(limb), ang=KeyFrame(15), dist=KeyFrame(40))
								]),
								dict(deepcopy(limb), ang=KeyFrame(225), dist=KeyFrame(40), children=[
											dict(deepcopy(limb), ang=KeyFrame(-15), dist=KeyFrame(40))
								])
					]),
					dict(deepcopy(limb), ang=KeyFrame(67), dist=KeyFrame(50), colour=KeyFrame((0,0,0)), children=[
								dict(deepcopy(limb), ang=KeyFrame(0), dist=KeyFrame(50))
					]),
					dict(deepcopy(limb), ang=KeyFrame(113), dist=KeyFrame(50), width=KeyFrame(7), children=[
								dict(deepcopy(limb), ang=KeyFrame(0), dist=KeyFrame(50))
					])
			]) 
	
	# Make the default animation
	MainStick = dict(limb, cartesian=KeyFrame(True, False, "const"), static=KeyFrame(True, False, "const"), hidden=KeyFrame(True, False, "const"), children=[deepcopy(StickMan)])
	
	# Get keyframes from default animation
	#keys = gatherKeyFrames(MainStick)
	#for key in keys:
	#	key.clean()
	
	# Define all the defaul application values
	cam = {'pos':KeyFrame(Vector(0,0)), 'zoom':KeyFrame(1), 'size':Vector(640,480)}
	data = {'scene':MainStick,
			'camera':cam, # All animation stuff for the camera goes here
			'panning':Vector(0,0), # View panning (Units, not pixels!)
			'zoom':1, # View zoom multiplier. 1 means each position is in pixels. Above 1 zooms in.
			'drag':None, # The limb being dragged. This is a reference when set.
			'editing':[], # Selected vertices, all limb references
			'limbcopy':[], # Stores copied limbs for pasting
			'playing':False, # If the animation is playing
			'playingstart':0, # The time when the animation started for finding the desired playback frame
			'frame':1, # Current frame for displaying and editing
			'framerate':25, # Playback FPS (Fames Per Second)
			'framelimit':[1,200], # 0: Low playback frame limit, 1: High playback frame limit 
			'StoredSelection':[], # Selected vertices are stored here for retrieval later
			"OnionSkinning":True, # If onion skinning (Motion blur) is enabled
			'PresetFigures':{'StickMan':StickMan}, # Dictionary of figure presets for adding to the scene
			'version':version} # StickyPy version (string)
	data['widgets'] = StickFigureApp(screensize, data) # Define the main application
	
	# Set blank image for fast screen filling
	blank = screen.copy()
	blank.fill((0,0,0))
	
	clock = pygame.time.Clock() # Clock object for timing and stuff

	#oldmousebut = pygame.mouse.get_pressed()
	
	#edited = True
	
	firstloop = True # If the main loop is on its first time through
	
	while True:
		#starttime = pygame.time.get_ticks()
		events = []
		if not data['playing'] and not firstloop: events += [pygame.event.wait()]
		events += pygame.event.get()
		mousepos = Vector(pygame.mouse.get_pos())
		mousebut = pygame.mouse.get_pressed()
		keys = pygame.key.get_pressed()
		
		#data['panning'] += Vector(1,1)
		if data['playing']:
			frame = (pygame.time.get_ticks() - data['playingstart']) / (float(1000)/data['framerate'])+1
			#print int(frame)
			if frame >= data['framelimit'][1]: data['playingstart'] = pygame.time.get_ticks()
			#print float(data['widgets'].container.widgets['StickEditor'].size.y) / float(data['widgets'].container.widgets['StickEditor'].size.x), data['camera']['size'].y / data['camera']['size'].x
			if float(data['widgets'].container.widgets['StickEditor'].size.y) / float(data['widgets'].container.widgets['StickEditor'].size.x) < float(data['camera']['size'].y) / data['camera']['size'].x: 
				data['zoom'] = float(data['widgets'].container.widgets['StickEditor'].size.y) / data['camera']['size'].y / data['camera']['zoom'].setframe(frame)
			else:
				data['zoom'] = float(data['widgets'].container.widgets['StickEditor'].size.x) / data['camera']['size'].x / data['camera']['zoom'].setframe(frame)
			
			data['panning'] = -Vector(data['camera']['pos'].setframe(frame))
			#print data['zoom']
			data['widgets'].container.changeframe(frame)
		
		if len(events) == 1 and mousebut[0] and not mousebut[1] and not mousebut[2]: clock.tick(30)
		for event in events:
			if event.type == pygame.VIDEORESIZE:
				screensize.x = event.w
				screensize.y = event.h
				screen = pygame.display.set_mode(screensize, pygame.RESIZABLE)
				data['widgets'].container.resize(screensize, (0,0))
				data['widgets'].fullredraw = True
				
			if event.type == pygame.QUIT:
				sys.exit()
		
		if keys[pygame.K_ESCAPE]: sys.exit()
		
		data['widgets'].update(screen, keys, mousepos, mousebut, events)
		#screen.blit(data['widgets'].image, data['widgets'].pos)
		
		pygame.display.flip()
		#pygame.display.update(data['widgets'].updaterects)
		
		#oldmousebut = mousebut
		
		firstloop = False
		
		#if 1000 / float(pygame.time.get_ticks() - starttime) > 115:
		#print 1000 / float(pygame.time.get_ticks() - starttime)
		
mouse = [
		"           XX           ",
		"          X..X          ",
		"         X....X         ",
		"        X......X        ",
		"       XXXXXXXXXX       ",
		"           XX           ",
		"           XX           ",
		"    X      XX      X    ",
		"   XX      XX      XX   ",
		"  X.X      XX      X.X  ",
		" X..X      XX      X..X ",
		"X...XXXXXXXXXXXXXXXX...X",
		"X...XXXXXXXXXXXXXXXX...X",
		" X..X      XX      X..X ",
		"  X.X      XX      X.X  ",
		"   XX      XX      XX   ",
		"    X      XX      X    ",
		"           XX           ",
		"           XX           ",
		"       XXXXXXXXXX       ",
		"        X......X        ",
		"         X....X         ",
		"          X..X          ",
		"           XX           "]

mouse = [
		"..                      ",
		".X.                     ",
		".XX.                    ",
		".XXX.                   ",
		".XX.X.                  ",
		".XX.XX.                 ",
		"......X.                ",
		".XX.XXXX.               ",
		".XX.XXXXX.              ",
		".XXXXX.....             ",
		".XX.XX.                 ",
		".X. .XX.                ",
		"..  .XX.                ",
		".    .XX.               ",
		"     .XX.               ",
		"      ..                ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        ",
		"                        "]  # Possibly use this mouse in extrude mode
m = pygame.cursors.compile(mouse, ".", "X")
#pygame.mouse.set_cursor((24,24), (12,12), m[0], m[1])
#pygame.mouse.set_cursor((24,24), (0,0), m[0], m[1])
#main(screen)

def timer():
	while True:
		pygame.time.wait(350)
		pygame.event.post(pygame.event.Event(pygame.NOEVENT))
thread.start_new_thread(timer, ())

#cProfile.run('main(screen)')
main(screen)
