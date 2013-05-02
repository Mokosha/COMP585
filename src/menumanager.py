import os, sys, time
from utils import *

import pygame

from eventmanager import Events, InputManager

class Screen:

	def __init__(self, topLeftCorner, width, height, layout, bckgrdClr, drawSurface, selection):
		self.loc = topLeftCorner
		self.mySurface = pygame.Surface((width, height))
		self.layout = layout
		self.color = bckgrdClr
		self.mySurface.fill(self.color)
		self.drawSurface = drawSurface
		self.currentlySelected = selection
		self.myOptions = []

	def runMenu(self, menuDrawer):
		myMessage = ""
		pygame.display.flip()
		pygame.event.clear()
		while not menuDrawer.done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
					filename = getRootPath() + os.sep + "assets" + os.sep + "sound" + os.sep + "Cursor_tones" + os.sep  + "cursor_style_2.ogg"
					pygame.mixer.Sound(filename).play()
					if self.currentlySelected == 0:
						self.currentlySelected = len(self.myOptions) - 1
					else:
						self.currentlySelected = self.currentlySelected - 1
					return menuDrawer.initMenu(self.drawSurface, self.currentlySelected)
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
					filename = getRootPath() + os.sep + "assets" + os.sep + "sound" + os.sep + "Cursor_tones" + os.sep  + "cursor_style_2.ogg"
					pygame.mixer.Sound(filename).play()
					if self.currentlySelected >= (len(self.myOptions) - 1):
						self.currentlySelected = 0
					else:
						self.currentlySelected = self.currentlySelected + 1
					return menuDrawer.initMenu(self.drawSurface, self.currentlySelected)
				elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_p):
					menuDrawer.done = True
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
					filename = getRootPath() + os.sep + "assets" + os.sep + "sound" + os.sep + "Confirm_tones" + os.sep + "style3" + os.sep + "confirm_style_3_001.ogg"
					pygame.mixer.Sound(filename).play()
					myMessage = menuDrawer.execute(self.myOptions[self.currentlySelected].myText)
					if (myMessage == "Update"):
						return menuDrawer.initMenu(self.drawSurface, self.currentlySelected)
		return myMessage

class Options:

	def __init__(self, parent, topLeftRelative, width, height, text, isSelected):
		if isSelected:
			fontSize = 28
		else:
			fontSize = 24
		font = pygame.font.SysFont('comicsansms',fontSize)
		self.myText = text
		self.newSurface = font.render(text, True, pygame.Color('black'))
		if (parent.layout == 'horiz'):
			pass
		elif (parent.layout == 'vert'):
			xOffset = self.findCentralPosition(parent.mySurface.get_width(),width)
			yOffset = topLeftRelative * (height + 20)
			parent.mySurface.blit(self.newSurface, (xOffset, yOffset))
		parent.myOptions.append(self)

	def findCentralPosition(self, outerLength, innerLength):
		return ((outerLength - innerLength) / 2)

class PauseMenu:
	
	done = False

	def run(self, theSurface):
		pygame.mixer.init()
		self.surface = theSurface
		filename = getRootPath() + os.sep + "assets" + os.sep + "sound" + os.sep + "Confirm_tones" + os.sep + "style2" + os.sep + "confirm_style_2_001.ogg"
		pygame.mixer.Sound(filename).play()
		return self.initMenu(theSurface, 0)

	def initMenu(self, theSurface, currentlySelected):
		myMenu = Screen((150, 100), 300, 400, 'vert', pygame.Color('orange'), theSurface, currentlySelected)
		text = ['Resume', 'Controls', 'Return to Title']
		options = []
		for i in range(len(text)):
			isSelected = (currentlySelected == i)
			options.append(Options(myMenu, i, 200, 50, text[i], isSelected))
		myMenu.drawSurface.blit(myMenu.mySurface, myMenu.loc)
		return myMenu.runMenu(self)

	def execute(self, myOption):
		if myOption == 'Resume':
			self.done = True
			return "Quit Pause Menu"
		if myOption == 'Controls':
			ControlsSelect().run(self.surface)
			return "Update"
		if myOption == 'Return to Title':
			self.done = True
			return "Quit Game"

class TitleMenu:

	done = False

	def run(self, theSurface):
		self.surface = theSurface
		pygame.mixer.init()
		filename = getRootPath() + os.sep + "assets" + os.sep + "sound" + os.sep + "Confirm_tones" + os.sep + "style2" + os.sep + "confirm_style_2_001.ogg"
		pygame.mixer.Sound(filename).play()
		return self.initMenu(theSurface, 0)

	def initMenu(self, theSurface, currentlySelected):
		myMenu = Screen((0, 0), 800, 600, 'vert', pygame.Color('orange'), theSurface, currentlySelected)
		text = ['New Game', 'Choose Level', 'Controls', 'About', 'Music', 'Exit']
		options = []
		for i in range(len(text)):
			isSelected = (currentlySelected == i)
			options.append(Options(myMenu, i, 200, 50, text[i], isSelected))
		myMenu.drawSurface.blit(myMenu.mySurface, myMenu.loc)
		return myMenu.runMenu(self)

	def execute(self, myOption):
		if myOption == 'New Game':
			self.done = True
			return "start"
		if myOption == 'Choose Level':
			result = LevelSelectMenu().run(self.surface)
			if result == "start" or result == "next":
				self.done = True
				return result
			else:
				return self.initMenu(self.surface, 0)
		if myOption == 'Controls':
			ControlsSelect().run(self.surface)
			return "Update"
		if myOption == 'About':
			return None
		if myOption == "Music":
			pygame.mixer.stop()
			MusicMenu().run(self.surface)
			pygame.mixer.Sound(getAssetsPath() + os.sep + "sound" + os.sep + "Music" + os.sep + "TitleScreen.ogg").play()
			return "Update"
		if myOption == 'Exit':
			sys.exit()

class LevelSelectMenu:

	done = False

	def run(self, theSurface):
		self.levels = [
			['Tutorial','start'],
			['Level One','next'],
			['Level Two','Level2'],
			['Level Three','Level3'],
			['Level Four','Level4'],
			['Level Five','Level5'],
			['Level Six','Level6'],
			['Level Seven','Level7'],
			['Boss Fight','Achroma'],
			['Back','Back']
		]

		pygame.mixer.init()
		filename = getRootPath() + os.sep + "assets" + os.sep + "sound" + os.sep + "Confirm_tones" + os.sep + "style2" + os.sep + "confirm_style_2_001.ogg"
		pygame.mixer.Sound(filename).play()
		return self.initMenu(theSurface, 0)

	def initMenu(self, theSurface, currentlySelected):
		myMenu = Screen((0, 0), 800, 600, 'vert', pygame.Color('orange'), theSurface, currentlySelected)
		options = []
		for i in range(len(self.levels)):
			isSelected = (currentlySelected == i)
			options.append(Options(myMenu, i, 200, 30, self.levels[i][0], isSelected))
		myMenu.drawSurface.blit(myMenu.mySurface, myMenu.loc)
		return myMenu.runMenu(self)

	def execute(self, myOption):
		self.done = True
		for pair in self.levels:
			if pair[0] == myOption:
				return pair[1]
		return None

class ControlsSelect:

	done = False

	def run(self, theSurface):
		self.controls = ["Jump", "Right", "Left", "Reset Color", "Use Color 1", "Use Color 2", "Use Color 3", "Done"]
		self.surface = theSurface
		pygame.mixer.init()
		filename = getRootPath() + os.sep + "assets" + os.sep + "sound" + os.sep + "Confirm_tones" + os.sep + "style2" + os.sep + "confirm_style_2_001.ogg"
		pygame.mixer.Sound(filename).play()
		return self.initMenu(theSurface, 0)

	def initMenu(self, theSurface, currentlySelected):
		myMenu = Screen((0, 0), 800, 600, 'vert', pygame.Color('orange'), theSurface, currentlySelected)
		options = []
		for i in range(len(self.controls)):
			isSelected = (currentlySelected == i)
			buttontext = self.controls[i]
			if self.controls[i] != "Done":
				buttontext = buttontext + ": " + pygame.key.name(eventmanager.cheesyReverseMapping[eventmanager.nameMapping[self.controls[i]]])
			options.append(Options(myMenu, i, 200, 30, buttontext, isSelected))
		myMenu.drawSurface.blit(myMenu.mySurface, myMenu.loc)
		return myMenu.runMenu(self)

	def execute(self, myOption):
		if myOption == "Done":
			self.done = True
		else:
			changed = False
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
						return ""
					elif event.type == pygame.KEYDOWN:
						name = myOption.partition(':')[0]
						eventmanager.changeMappings(event.key, eventmanager.nameMapping[name])				
						return "Update"		

class MusicMenu:

	done = False

	def run(self, theSurface):
		self.surface = theSurface
		pygame.mixer.init()
		filename = getRootPath() + os.sep + "assets" + os.sep + "sound" + os.sep + "Confirm_tones" + os.sep + "style2" + os.sep + "confirm_style_2_001.ogg"
		pygame.mixer.Sound(filename).play()
		return self.initMenu(theSurface, 0)

	def initMenu(self, theSurface, currentlySelected):
		myMenu = Screen((0, 0), 800, 600, 'vert', pygame.Color('orange'), theSurface, currentlySelected)
		options = []
		myMusic = ["Power", "Bioluminescence", "Some things are...", "Scarleted", "Light", "Fire tundra", "Drops of Glass", "Void", "to make suffer", "Start New Game?", "Done"]
		for i in range(len(myMusic)):
			isSelected = (currentlySelected == i)
			options.append(Options(myMenu, i, 200, 30, myMusic[i], isSelected))
		myMenu.drawSurface.blit(myMenu.mySurface, myMenu.loc)
		return myMenu.runMenu(self)

	def execute(self, myOption):
		if myOption == "Done":
			self.done = True
		else:
			track = ""
			if myOption == "Some things are...":
				track = "Level2"
			if myOption == "Bioluminescence":
				track = "next"
			if myOption == "Power":
				track = "start"
			if myOption == "Void":
				track = "Level7b"
			if myOption == "Start New Game?":
				track = "TitleScreen"
			if myOption == "Scarleted":
				track = "Level4"
			if myOption == "Light":
				track = "Level5"
			if myOption == "Fire tundra":
				track = "Level6"
			if myOption == "Drops of Glass":
				track = "Level7a"
			if myOption == "to make suffer":
				track = "Level7c"
			self.runTrack(track)
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					if event.type == pygame.KEYDOWN:
						pygame.mixer.stop()
						return "Update"

	def runTrack(self, trackName):
		filename = getAssetsPath() + os.sep + "sound" + os.sep + "Music" + os.sep + trackName + ".ogg"
		pygame.mixer.Sound(filename).play()