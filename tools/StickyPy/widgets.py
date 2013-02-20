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
from objs import *

import thread

class BaseWidget:
	def __init__(self, pos, size, container = None, data = None):
		self.initwidget(pos, size, container, data)
	def initwidget(self, pos, size, container = None, data = None):
		self.data = data
		self.container = container
		self.pos = pos
		self.size = size
		self.image = pygame.Surface(self.size).convert()
		self.visible = True
		self.oldvisible = self.visible
		
		self.selected = False
		self.oldkeys = []
		self.oldmousepos = (0,0)
		self.oldmousebut = (False,False,False)
		self.oldhover = False
		self.keys = []
		self.mousepos = (0,0)
		self.mousebut = (False,False,False)
		self.hover = False
		self.disabled = False
		self.redraw = True
		self.comment = ""
		self.setup()
		
	def setup(self):
		pass
	def update(self, keyboard, mousepos, mousebut, hover, selected, events = [], threadcount = 0):
		self.events = events
		self.keyboard = keyboard
		self.mousepos = mousepos
		self.mousebut = mousebut
		self.hover = hover
		self.selected = selected
		if not self.disabled:
	#		if self.mousebut[0] and not self.oldmousebut[0]: self.lclick()
	#		if self.mousebut[1] and not self.oldmousebut[1]: self.mclick()
	#		if self.mousebut[2] and not self.oldmousebut[2]: self.rclick()
	#		if not self.mousebut[0] and self.oldmousebut[0]: self.lrelease()
	#		if not self.mousebut[1] and self.oldmousebut[1]: self.mrelease()
	#		if not self.mousebut[2] and self.oldmousebut[2]: self.rrelease()
			for event in self.events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: self.lclick()
					elif event.button == 2: self.mclick()
					elif event.button == 3: self.rclick()
					elif event.button == 4: self.mwheelup()
					elif event.button == 5: self.mwheeldown()
				elif event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1: self.lrelease()
					elif event.button == 2: self.mrelease()
					elif event.button == 3: self.rrelease()
				self.handleevent(event)
			if self.hover and not self.oldhover: self.mouseover()
			elif not self.hover and self.oldhover: self.mouseout()
			if not self.mousepos[0] == self.oldmousepos[0] or not self.mousepos[1] == self.oldmousepos[1]: self.mousemove() 
			self.always()
			
			self.oldkeyboard = self.keyboard
			self.oldmousepos = self.mousepos
			self.oldmousebut = self.mousebut
			self.oldhover = self.hover
			self.oldvisible = self.visible
			self.oldselected = self.selected
			
		#threadcount -= 1
		
		return self.image
	def enable(self):
		self.oldkeyboard = self.keyboard
		self.oldmousepos = self.mousepos
		self.oldmousebut = self.mousebut
		self.oldhover = self.hover
		self.oldvisible = self.visible
		self.oldselected = self.selected
		self.disabled = False
		self.update(self.oldkeyboard, self.oldmousepos, self.oldmousebut, self.oldhover, self.oldselected, [])
	def handleevent(self, event):
		pass
	def lclick(self):
		pass
	def mclick(self):
		pass
	def rclick(self):
		pass
	def lrelease(self):
		pass
	def mrelease(self):
		pass
	def rrelease(self):
		pass
	def mwheelup(self):
		pass
	def mwheeldown(self):
		pass
	def mousemove(self):
		pass
	def mouseover(self):
		pass
	def mouseout(self):
		pass
	def always(self):
		pass
	def menuaction(self, selection):
		pass
	def resize(self, pos, size):
		self.pos = pos
		if size[0] < 1: size[0] = 1
		if size[1] < 1: size[1] = 1
		self.size = size
		self.image = pygame.Surface(self.size)
		self.draw()
	def draw(self):
		self.image.fill((0,0,0))
		
		self.redraw = True
		return self.image

class MainWindow:
	def __init__(self, data):
		self.resources = None # Insert resource object here
		self.container = None # Insert widget container here
	def setupwindow(self):
		self.menu = WindowMenu(self)
		
		self.comment = ["", Vector(0,0), 0] #[Comment, Position, Hover time]
		self.oldcomment = deepcopy(self.comment)
		self.commenttimestart = 1000
		self.commenttimeend = 4000
		
		#self.updaterects = []
		self.fullredraw = True
	def update(self, screen, keyboard, mousepos, mousebut, events = []):
		#self.updaterects = []
		menuvisible = self.menu.visible
		self.mousepos = mousepos
		if self.menu.visible:
			hover = pygame.Rect(self.menu.pos, self.menu.size).collidepoint(mousepos)
			self.menu.update(keyboard, mousepos, mousebut, hover, True, events)
			mousebut = (False,False,False)
			
		self.container.update(keyboard, mousepos, mousebut, not menuvisible, not menuvisible, events)
		if self.container.redraw: screen.blit(self.container.image, (0,0))
		
		if self.menu.visible:
			screen.blit(self.menu.image, self.menu.pos)
			
		if not self.comment[0] == "":
			if not self.comment[0] == self.oldcomment[0]: self.comment[2] = pygame.time.get_ticks()
			if pygame.time.get_ticks() > self.comment[2] + self.commenttimestart and pygame.time.get_ticks() < self.comment[2] + self.commenttimeend:
				#self.updaterects.append(pygame.Rect(pos-Vector(1,1), Vector(fontrender.get_size())+Vector(2,2)))
				font = pygame.font.Font(pygame.font.get_default_font(), 15)
				fontrender = font.render(self.comment[0], True, (0,0,0))
				pos = Vector(min(self.comment[1][0], self.container.size.x-fontrender.get_width()),self.comment[1][1]-fontrender.get_height())
				#pygame.draw.rect(screen, (0,0,0,100), pygame.Rect(pos+Vector(3,3), fontrender.get_size()))
				pygame.draw.rect(screen, (255,255,180), pygame.Rect(pos, fontrender.get_size()))
				pygame.draw.rect(screen, (0,0,0), pygame.Rect(pos-Vector(1,1), Vector(fontrender.get_size())+Vector(2,2)), 1)
				screen.blit(fontrender, pos)
				#self.updaterects.append(pygame.Rect(pos-Vector(1,1), Vector(fontrender.get_size())+Vector(2,2)))
		self.oldcomment = deepcopy(self.comment)
		
		self.fullredraw = False

class WidgetContainer(BaseWidget):
	def __init__(self, pos, size, widgets, order, mainwindow):
		self.setupcontainer(pos, size, mainwindow)
		self.widgets = widgets
		self.order = order
	def setupcontainer(self, pos, size, mainwindow, container = None, data = None):
		self.window = mainwindow
		self.widgetselected = 0
		self.initwidget(pos, size, container, data)
		self.drawbase()
	def setup(self):
		self.image = pygame.Surface(self.size)
		self.mousemask = self.image.copy()
		self.mousemask.fill((0,0,0))
		self.blank = self.mousemask
		#print "test"
	def resize(self, size, pos):
		self.size = size
		self.pos = pos
		self.setup()
		self.organise()
	def lclick(self):
		self.setSelected()
	def mclick(self):
		self.setSelected()
	def rclick(self):
		self.setSelected()
	def setSelected(self):
		self.widgetselected = 0
		mpos = Vector(self.mousepos-self.pos) 
		if mpos.x > 0 and mpos.x < self.mousemask.get_width() and mpos.y > 0 and mpos.y < self.mousemask.get_height():
			self.widgetselected = (self.mousemask.get_at(mpos)[0])
	def organise(self):
		pass
	def always(self):
		if len(self.events) > 0:
			self.mousemask = self.blank.copy()
			
		for i in range(len(self.order)):
			if self.widgets[self.order[i]].visible: pygame.draw.rect(self.mousemask, (i+1,0,0), pygame.Rect(self.widgets[self.order[i]].pos, self.widgets[self.order[i]].size))
			
		threadcount = 0
		for i in range(len(self.order)):
			hover = False
			if self.mousepos[0]- self.pos[0] > 0 and self.mousepos[0]- self.pos[0] < self.mousemask.get_width() and self.mousepos[1] - self.pos[1] > 0 and self.mousepos[1] - self.pos[1] < self.mousemask.get_height():
				hover = (self.mousemask.get_at(self.mousepos-self.pos)[0] == i+1) and self.hover
				if self.mousemask.get_at(self.mousepos-self.pos)[0] == 0: self.window.comment[0] = ""
			
			if hover:
				self.window.comment[0] = self.widgets[self.order[i]].comment
				self.window.comment[1] = self.window.mousepos#; print self.widgets[self.order[i]].comment
			if self.mousebut[0]or self.mousebut[1] or self.mousebut[2]: self.window.comment[0] = ""
				
			selected = False
			if self.widgetselected == i+1:
				selected = self.selected
			self.widgets[self.order[i]].update(self.keyboard, self.mousepos-self.pos, self.mousebut, hover, selected, self.events)
			#threadcount += 1
			#thread.start_new_thread(self.widgets[self.order[i]].update, (self.keyboard, self.mousepos-self.pos, self.mousebut, hover, selected, self.events, threadcount))
			#pygame.time.wait(200)
			#print threadcount
		#while threadcount > 0: print threadcount
		self.draw()
	def draw(self):
		#self.image.fill((0,0,0))
		#self.image.blit(canvas, canvaspos)
		self.drawwidgets()
		
		#self.redraw = True
	def drawwidgets(self):
		if self.window.fullredraw: self.drawbase()
		
		for widget in self.order:
			if self.widgets[widget].visible and (self.widgets[widget].redraw or self.window.fullredraw):
				self.image.blit(self.widgets[widget].image, self.widgets[widget].pos)
				#self.window.updaterects.append(pygame.Rect(self.widgets[widget].pos, self.widgets[widget].image.get_size()))
				#self.window.updaterects.append(pygame.Rect(self.widgets[widget].pos, self.widgets[widget].image.get_size()))
				self.redraw = self.redraw or self.widgets[widget].redraw #Redraw if anything changes in any widget
				self.widgets[widget].redraw = False
	def drawbase(self):
		self.image.fill((0,0,0))

#class QuestionDialogWindow(WidgetContainer):
#	def __init__(self, question, type = "yesno", title = "Question", action = sys.exit):
#		self.question = question
#		self.action = action
#		if type == "yesno":
#			self.widgets = {'YesButton':Button}

#class QuestionDialogYesButton

class DragBar(BaseWidget):
	def setup(self):
		self.dragging = False
		self.image.fill((0,100,255))
	def lclick(self):
		if self.hover:
			self.dragging = True
			self.dragmouse = self.container.window.mousepos
			self.dragpos = self.container.pos
	def mousemove(self):
		if self.dragging:
			self.container.pos = Vector(self.dragpos + self.container.window.mousepos - self.dragmouse)
			self.container.window.fullredraw = True
	def lrelease(self):
		self.dragging = False
	def draw(self):
		pass

class Button(BaseWidget):
	def setup(self):
		self.buttonsetup()
	def buttonsetup(self, label = "Button"):
		self.label = label
		self.texbutup = self.container.window.resources['buttonup']
		self.texbutdown = self.container.window.resources['buttondown']
		self.updatefont()
		self.update([], self.oldmousepos, self.oldmousebut, self.oldhover, False)
		self.draw()
		return self
	def changelabel(self, label):
		self.label = label
		self.updatefont()
		self.draw()
	def updatefont(self):
		self.font = pygame.font.Font(pygame.font.get_default_font(), self.size[1])
		twidth = self.font.render(self.label, True, (0,0,255)).get_width()
		if twidth > self.size[0]: self.font = pygame.font.Font(pygame.font.get_default_font(), int(float(self.size[0]) / float(twidth) * float(self.size[1])))
	def lclick(self):
		self.draw()
	def lrelease(self):
		self.draw()
	def mouseover(self):
		self.draw()
	def mouseout(self):
		self.draw()
	def draw(self):
		self.drawbutton()
	def drawbutton(self):
		if self.mousebut[0] and self.hover and self.selected:
			#self.image.fill([0,0,0,0])
			self.image.blit(pygame.transform.smoothscale(self.texbutdown, (self.size[0], self.size[1])), (0,0))
		else:
			#self.image.fill([0,0,255])
			self.image.blit(pygame.transform.smoothscale(self.texbutup, (self.size[0], self.size[1])), (0,0))
		if self.hover and (not self.mousebut[0] or self.selected):
			colour = (255,0,0)
		else:
			colour = (200,0,0)
		text = self.font.render(self.label, True, colour)
		self.image.blit(text, (0,self.size[1]/2 - text.get_height()/2))
		
		self.redraw = True
		return self.image

class Label(BaseWidget):
	def __init__(self, pos, size, label, colour = (0,0,0), container = None, data = None):
		self.colour = colour
		self.initwidget(pos, size, container, data)
		self.labelsetup(label)
	def setup(self):
		self.labelsetup()
	def labelsetup(self, label = "Button"):
		self.image = pygame.Surface(self.size).convert_alpha()
		self.label = label
		self.updatefont()
		self.draw()
	def changelabel(self, label):
		self.label = label
		self.updatefont()
		self.draw()
	def updatefont(self):
		self.font = pygame.font.Font(pygame.font.get_default_font(), self.size[1])
		twidth = self.font.render(self.label, True, (0,0,255)).get_width()
		if twidth > self.size[0]: self.font = pygame.font.Font(pygame.font.get_default_font(), int(float(self.size[0]) / float(twidth) * float(self.size[1])))
	def update(self, keyboard, mousepos, mousebut, hover, selected, events = [], threadcount=0):
		threadcount -= 1
	def draw(self):
		self.image.fill([0,0,0,0])
		text = self.font.render(self.label, True, self.colour)
		self.image.blit(text, (0,self.size[1]/2 - text.get_height()/2))
		
		self.redraw = True
		return self.image

class CheckBox(BaseWidget):
	def setup(self):
		self.checkboxsetup()
	def checkboxsetup(self, label = "Check Box", fontsize = 15):
		self.image = pygame.Surface(self.size).convert_alpha()
		self.label = label
		self.texchkon = self.container.window.resources['checkboxon']
		self.texchkoff = self.container.window.resources['checkboxoff']
		self.fontsize = fontsize
		self.updatefont()
		self.update([], self.oldmousepos, self.oldmousebut, self.oldhover, False)
		self.checked = False
		self.draw()
		return self
	def changelabel(self, label):
		self.label = label
		self.updatefont()
		self.draw()
	def updatefont(self):
		self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)
		twidth = self.font.render(self.label, True, (0,0,255)).get_width()
		if twidth > self.size[0]: self.font = pygame.font.Font(pygame.font.get_default_font(), float(self.size[0]) / float(twidth) * float(self.fontsize))
	def lclick(self):
		self.draw()
	def lrelease(self):
		if self.hover and self.selected:
			self.checked = not self.checked
			self.changed()
		self.draw()
	def mouseover(self):
		self.draw()
	def mouseout(self):
		self.draw()
	def changed(self):
		pass
	def draw(self):
		self.image.fill([0,0,0, 0])
		if self.checked:
			self.image.blit(pygame.transform.smoothscale(self.texchkon, (self.size[1], self.size[1])), (0,0))
		else:
			self.image.blit(pygame.transform.smoothscale(self.texchkoff, (self.size[1], self.size[1])), (0,0))
		if self.hover and (not self.mousebut[0] or self.selected):
			colour = (255,0,0,0)
		else:
			colour = (200,0,0,0)
		text = self.font.render(self.label, True, colour)
		self.image.blit(text, (self.size[1],self.size[1]/2 - text.get_height()/2))
		
		self.redraw = True
		self.container.window.fullredraw = True
		return self.image

class DropDownMenu(BaseWidget):
	def setup(self):
		self.menusetup()
	def menusetup(self, pos=(0,0), items=[("Item", "item")], fontsize = 12):
		self.items = items
		self.pos = pos
		self.fontsize = fontsize
		self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)
		maxwidth = 0
		for item in self.items:
			twidth = self.font.render(item[0], True, (0,0,0)).get_width()
			if twidth > maxwidth: maxwidth = twidth
		self.size = (maxwidth, self.fontsize*len(self.items))
		self.image = pygame.Surface(self.size)
	def lrelease(self):
		self.visible = False
		if self.hover and self.oldvisible:
			self.action(int(self.mousepos[1] - self.pos[1]) / self.fontsize)
	def mrelease(self):
		self.visible = False
		if self.hover and self.oldvisible:
			self.action(int(self.mousepos[1] - self.pos[1]) / self.fontsize)
	def rrelease(self):
		self.visible = False
		if self.hover and self.oldvisible:
			self.action(int(self.mousepos[1] - self.pos[1]) / self.fontsize)
	def mousemove(self):
		if self.oldvisible:
			self.draw()
	def action(self, selection):
		pass
	def draw(self):
		self.image.fill((230,230,230))
		if self.hover: pygame.draw.rect(self.image, (255,200,0), pygame.Rect((0,self.fontsize*(int(self.mousepos[1] - self.pos[1]) / self.fontsize)),(self.size[0], self.fontsize)))
		pygame.draw.rect(self.image, (0,0,0), pygame.Rect((0,0),self.size), 1)
		for i in range(len(self.items)):
			self.image.blit(self.font.render(self.items[i][0], True, (0,0,0)), (0,self.fontsize*i))
			
		self.redraw = True
		return self.image

class WindowMenu(DropDownMenu):
	def __init__(self, window):
		self.initwidget(Vector(0,0), Vector(1,1), None, None)
		self.visible = False
		self.oldvisible = self.visible
		self.window = window
	def showmenu(self, items, pos, caller, fontsize = 20):
		self.menusetup(Vector(pos), items, fontsize)
		if self.pos[0] + self.size[0] > self.window.container.size[0]: self.pos[0] = self.window.container.size[0] - self.size[0]
		if self.pos[1] + self.size[1] > self.window.container.size[1]: self.pos[1] = self.window.container.size[1] - self.size[1]
		self.caller = caller
		self.visible = True
		self.draw()
	def setup(self):
		pass
	def action(self, selection):
		self.caller.menuaction(self.items[selection][1])

class ScrollBar(BaseWidget):
	def scrollbarsetup(self, vertical=False, range=(0,100), value=0, griplength = 100):
		self.vertical = vertical
		self.range = range
		self.griplength = griplength
		self.texbarhori = self.container.window.resources['scrollbarhori']
		self.texbarvert = self.container.window.resources['scrollbarvert']
		self.value = value
		self.drag = False
		self.dragpos = 0
		self.updatefont()
		self.draw()
	def resize(self, pos, size):
		self.pos = pos
		if size[0] < 1: size[0] = 1
		if size[1] < 1: size[1] = 1
		self.size = size
		self.image = pygame.Surface(self.size)
		self.updatefont()
		self.draw()
	def updatefont(self):
		if self.vertical:
			self.font = pygame.font.Font(pygame.font.get_default_font(), self.size.x)
		else:
			self.font = pygame.font.Font(pygame.font.get_default_font(), self.size.y)
	def lclick(self):
		if self.hover:
			self.drag = True
			if self.vertical:
				self.dragpos = (float(self.mousepos.y) / (self.size.y - self.griplength) * self.range[1] + self.range[0])
			else:
				self.dragpos = (float(self.mousepos.x) / (self.size.x - self.griplength) * self.range[1] + self.range[0])
	def lrelease(self):
		self.drag = False
		self.draw()
	def mousemove(self):
		if self.drag:
			if self.vertical:
				off = (float(self.mousepos.y) / (self.size.y - self.griplength) * self.range[1] + self.range[0]) - self.dragpos
				self.value += off
				self.dragpos = (float(self.mousepos.y) / (self.size.y - self.griplength) * self.range[1] + self.range[0])
			else:
				off = (float(self.mousepos.x) / (self.size.x - self.griplength) * self.range[1] + self.range[0]) - self.dragpos
				self.value += off
				self.dragpos = (float(self.mousepos.x) / (self.size.x - self.griplength) * self.range[1] + self.range[0])
			if off != 0: self.scroll()
			self.draw()
	def scroll(self):
		pass
	def scrollto(self, value):
		self.value = value
		self.draw()
	def draw(self):
		self.image.fill((30,30,50))
		if self.vertical:
			sliderpos = float(self.value - self.range[0]) / (self.range[1] - self.range[0]) * (self.size.y - self.griplength)
			self.image.blit(pygame.transform.scale(self.texbarvert, (self.size[0], self.griplength)), (0, sliderpos))
			fontrender = self.font.render(str(int(self.value)), True, (255,255,255))
			fontrender = pygame.transform.rotate(fontrender, -90)
			self.image.blit(fontrender, (0, sliderpos + self.griplength / 2 - fontrender.get_height() / 2))
		else:
			sliderpos = float(self.value - self.range[0]) / (self.range[1] - self.range[0]) * (self.size.x - self.griplength)
			self.image.blit(pygame.transform.scale(self.texbarhori, (self.griplength, self.size[1])), (sliderpos, 0))
			fontrender = self.font.render(str(int(self.value)), True, (255,255,255))
			self.image.blit(fontrender, (sliderpos + self.griplength / 2 - fontrender.get_width() / 2, 0))
		
		self.redraw = True

class TextBox(BaseWidget):
	def setup(self):
		self.textboxsetup()
	def textboxsetup(self, text = ""):
		try:
			pygame.scrap.init()
			pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
		except:
			pass
		self.text = text
		self.origtext = text
		self.cursorpos = 0
		self.scroll = 0
		self.updatefont()
		self.editing = False
		self.keyrange = (32,126)
		self.draw()
	def changetext(self, text = ""):
		if not self.editing:
			self.text = text
			self.draw()
	def updatefont(self):
		self.font = pygame.font.Font(pygame.font.get_default_font(), self.size.y)
	def getcursorpos(self, x):
		if len(self.text) > 0:
			for i in range(len(self.text)+1):
				cursorpos = i
				if cursorpos < len(self.text):
					textwidth = self.font.render(self.text[:cursorpos], True, (0,0,0)).get_width()
					charwidth = self.font.render(self.text[cursorpos], True, (0,0,0)).get_width()
					if textwidth + charwidth / 2 > x + self.scroll:
						break
		else:
			cursorpos = 0
		return cursorpos
	def lclick(self):
		if self.hover:
			if not self.editing: self.origtext = self.text
			self.editing = True
			self.cursorpos = self.getcursorpos(self.mousepos.x - self.pos.x)
			self.setscroll()
		else:
			if self.editing: self.validate()
			self.editing = False
		self.draw()
	def mclick(self):
		if self.hover:
			if not self.editing: self.origtext = self.text
			self.editing = True
			self.cursorpos = self.getcursorpos(self.mousepos.x - self.pos.x)
			clip = pygame.scrap.get(pygame.SCRAP_TEXT)
			if clip: self.text = self.text[:self.cursorpos] + clip + self.text[self.cursorpos:]
			self.setscroll()
		else:
			if self.editing: self.validate()
			self.editing = False
		self.draw()
	def rclick(self):
		if self.hover:
			if not self.editing: self.origtext = self.text
			self.editing = True
			self.cursorpos = self.getcursorpos(self.mousepos.x - self.pos.x)
			self.setscroll()
		else:
			if self.editing: self.validate()
			self.editing = False
		self.draw()
	def always(self):
		# 32-126 are keyboard keys
		if self.editing:
			for event in self.events:
				if event.type == pygame.KEYDOWN:
					if event.key >= self.keyrange[0] and event.key <= self.keyrange[1]:
						self.text = self.text[:self.cursorpos] + event.unicode + self.text[self.cursorpos:]
						self.cursorpos += 1
					elif event.key == pygame.K_BACKSPACE:
						self.text = self.text[:self.cursorpos-1] + self.text[self.cursorpos:]
						self.cursorpos -= 1
					elif event.key == pygame.K_DELETE:
						self.text = self.text[:self.cursorpos] + self.text[self.cursorpos + 1:]
					elif event.key == pygame.K_RIGHT:
						self.cursorpos += 1
					elif event.key == pygame.K_LEFT:
						self.cursorpos -= 1
					elif event.key == pygame.K_END:
						self.cursorpos = len(self.text)
					elif event.key == pygame.K_HOME:
						self.cursorpos = 0
					if self.cursorpos < 0: self.cursorpos = 0
					if self.cursorpos > len(self.text): self.cursorpos = len(self.text)
					self.edited()
					self.setscroll()
					#print self.text, self.cursorpos
					self.draw()
	def setscroll(self):
		cursorx = self.font.render(self.text[:self.cursorpos], True, (0,0,0)).get_width()
		if self.scroll < cursorx - self.size.x:
			self.scroll = cursorx - self.size.x
		elif self.scroll > cursorx:
			self.scroll = cursorx
		if self.scroll < 0: self.scroll = 0
	def edited(self):
		pass
	def validate(self):
		pass
	def draw(self):
		self.image.fill((255,255,255))
		if self.editing:
			cursorx = self.font.render(self.text[:self.cursorpos], True, (0,0,0)).get_width()
			pygame.draw.line(self.image, (255,0,0), (cursorx-self.scroll, 0), (cursorx-self.scroll, self.size.y), 3)
		self.image.blit(self.font.render(self.text, True, (0,0,0)), (-self.scroll,0))
		
		self.redraw = True

class NumberScrollBox(TextBox):
	def textboxsetup(self, text = ""):
		self.text = text
		self.origtext = text
		self.cursorpos = 0
		self.scroll = 0
		self.updatefont()
		self.editing = False
		self.dragging = False
		self.clickmousepos = self.mousepos
		self.keyrange = (32,126)
		self.draw()
	def lclick(self):
		if self.hover and not self.editing:
			self.clickmousepos = self.mousepos
		elif self.hover and self.editing:
			self.cursorpos = self.getcursorpos(self.mousepos.x - self.pos.x)
			self.setscroll()
		else:
			if self.editing: self.validate()
			self.editing = False
		self.draw()
	def lrelease(self):
		#print self.clickmousepos, self.mousepos, self.hover, str(self.clickmousepos) == str(self.mousepos)
		if self.hover and str(self.clickmousepos) == str(self.mousepos):
			self.editing = True
			self.cursorpos = self.getcursorpos(self.mousepos.x - self.pos.x)
			self.setscroll()
		elif not self.hover:
			#if self.editing:
			self.validate()
			self.editing = False
		self.draw()
	def scrolled(self, offset):
		self.edited()
	def validate(self):
		try:
			self.text = str(float(self.text))
		except:
			self.text = self.origtext
		self.draw()
	def mousemove(self):
		if self.mousebut[0] and self.selected and not self.editing:
			self.validate()
			self.text = str(float(self.text) + (self.oldmousepos.y - self.mousepos.y))
			self.origtext = self.text
			self.scrolled(self.oldmousepos.y - self.mousepos.y)
			self.draw()

class MenuBar(BaseWidget):
	def setup(self):
		self.menusetup([("File", [("Quit", "quit")])])
		self.texback = self.container.window.resources['textbox']
		self.draw()
	def menusetup(self, menu):
		self.menu = menu
		self.updatefont()
	def updatefont(self):
		self.font = pygame.font.Font(pygame.font.get_default_font(), self.size[1])
		twidth = ((self.size[0]/(len(self.menu)))) #self.font.render(self.list[self.selected], True, (0,0,255)).get_width()
		if twidth > self.size[0]: self.font = pygame.font.Font(pygame.font.get_default_font(), float(self.size[0]) / float(twidth) * float(self.size[1]))
	def resize(self, pos, size):
		self.pos = pos
		if size[0] < 1: size[0] = 1
		if size[1] < 1: size[1] = 1
		self.size = size
		self.image = pygame.Surface(self.size)
		self.draw()
	def lrelease(self):
		if self.hover:
			self.selected = int(float(self.mousepos.x - self.pos.x) / self.size.x * len(self.menu))
			menupos = (self.size.x / len(self.menu) * self.selected, self.size.y)
			self.container.window.menu.showmenu(self.menu[self.selected][1], menupos, self, self.size.y)
	def mouseover(self):
		self.draw()
	def mouseout(self):
		self.draw()
	def menuaction(self, selected):
		if selected == "quit": sys.exit()
	def draw(self):
		self.image.blit(pygame.transform.scale(self.texback, (self.size[0], self.size[1])), (0,0))
		if self.hover and (not self.mousebut[0] or self.selected):
			colour = (255,0,0)
		else:
			colour = (200,0,0)
		for i in range(len(self.menu)):
			text = self.font.render(self.menu[i][0], True, colour)
			self.image.blit(text, (i*((self.size[0]/(len(self.menu)))),self.size[1]/2 - text.get_height()/2))
			
		self.redraw = True