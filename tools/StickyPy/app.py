#    StickyPy - Stick Figure Animator
#    Copyright (C) 2009 Joshua Worth
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame, sys, os, pickle, zlib, webbrowser
import widgets, shapeeditor, keyframeeditor, editor
from objs import *
from defs import *

import thread

class StickFigureApp(widgets.MainWindow):
    def __init__(self, size, data):
        #self.setupwindow()
        self.data = data
        self.resources = AppResources()
        self.container = AppWidgets((0,0), size, self, data)
        self.setupwindow()

class AppResources(Resource):
    def setup(self):
        #self.addrec("", pygame.image.load(""))
        self.addrec("topgradient", pygame.image.load("topgradient.png"))
        self.addrec("buttonup", pygame.image.load("buttonup.png").convert())
        self.addrec("buttondown", pygame.image.load("buttondown.png").convert())
        self.addrec("checkboxon", pygame.image.load("checkboxon.png"))
        self.addrec("checkboxoff", pygame.image.load("checkboxoff.png"))
        self.addrec("scrollbarhori", pygame.image.load("scrollbarhori.png").convert())
        self.addrec("scrollbarvert", pygame.image.load("scrollbarvert.png").convert())
        self.addrec("textbox", pygame.image.load("textbox.png").convert())
        self.addrec("xbuttonup", pygame.image.load("xbuttonup.png").convert_alpha())
        self.addrec("xbuttondown", pygame.image.load("xbuttondown.png").convert_alpha())
        self.addrec("key", pygame.image.load("key.png").convert_alpha())
        self.addrec("keyoff", pygame.image.load("keyoff.png").convert_alpha())
        self.addrec("logo", pygame.image.load("logo.png").convert())

class AppWidgets(widgets.WidgetContainer):
    def __init__(self, pos, size, mainwindow, data):
        size = Vector(size)
        canvaspos = Vector(200,50) # Location of the editor
        
        self.topgradient = mainwindow.resources['topgradient']
        self.setupcontainer(pos, size, mainwindow, None, data)
        
        # Define all the widgets and their default values
        self.widgets = {'AddButton':AddButton(Vector(10,300), Vector(canvaspos[0]-30,30), self, data),
                        'lblSelAdd':widgets.Label(Vector(10,200), Vector(canvaspos[0]-30,30), "Preset sticks:", (255,255,255)),
                        'SelAddButton':SelAddButton(Vector(10,250), Vector(canvaspos[0]-30,30), self, data),
                        'StickEditor': editor.StickEditor(Vector(200,50), Vector(size.x-canvaspos.x, size.y-canvaspos.y-20), self, data),
                        'KeyFrameEditor':keyframeeditor.KeyFrameWidget(Vector(0,size[1]-200-20), Vector(size[0],200), self, mainwindow, data),
                        'ShapeEditor':shapeeditor.ShapeEditor(Vector(size[0]-300,100), Vector(300,size[1]-100), self, mainwindow, data),
                        'PlayButton':PlayButton(Vector(10,350), Vector(canvaspos[0]-30,30), self, data),
                        'CameraKeysButton':CameraKeysButton(Vector(10,500), Vector(canvaspos[0]-30,30), self, data),
                        #'lblFileName':widgets.Label(Vector(10,400), Vector(canvaspos[0]-30,30), "File name:", (255,255,255)),
                        #'FileName':widgets.TextBox(Vector(10,450), Vector(canvaspos[0]-30,30), self, data),
                        'StretchCheckBox':StretchCheckBox(Vector(10,100), Vector(canvaspos[0]-30,30), self, data),
                        'ExtrudeCheckBox':ExtrudeCheckBox(Vector(10,150), Vector(canvaspos[0]-30,30), self, data),
                        'lblFrame':widgets.Label(Vector(10,550), Vector(canvaspos[0]/2-30,30), "Frame:", (255,255,255)),
                        'lblFrameLimit':widgets.Label(Vector(10,600), Vector(canvaspos[0]-30,20), "Frame Limit:", (255,255,255)),
                        'lblFrameRate':widgets.Label(Vector(10,600), Vector(canvaspos[0]-30,20), "Frame Rate:", (255,255,255)),
                        'StartFrameScrollBox':StartFrameScrollBox(Vector(10,630), Vector(canvaspos[0]/2-30,30), self, data),
                        'EndFrameScrollBox':EndFrameScrollBox(Vector(canvaspos[0]/2,630), Vector(canvaspos[0]/2-30,30), self, data),
                        'FrameScrollBox':FrameScrollBox(Vector(canvaspos[0]/2,550), Vector(canvaspos[0]/2-30,30), self, data),
                        'FrameRateScrollBox':FrameRateScrollBox(Vector(10,550), Vector(canvaspos[0]-30,30), self, data),
                        'FrameScrollBar':FrameScrollBar(Vector(0,size[1]-20), Vector(size[0],20), self, data),
                        'EditorMenuBar':EditorMenuBar(Vector(0,0), Vector(size[0], 30), self, data),
                        'AboutDialog':AboutDialog(Vector(0,0), Vector(0,0), self, data),
                        'QuitDialog':QuitDialog(Vector(size)/2-Vector(200,80)/2, Vector(200,80), self, mainwindow, data),
                        'BrowserDialog':BrowserDialog(Vector(0,0), size, self, mainwindow, data),}
        #self.widgets['FileName'].textboxsetup("test")
        
        # Set the display order
        self.order = ['EditorMenuBar', 'StickEditor', 'PlayButton', 'CameraKeysButton', #'lblFileName', 'FileName',
                    'lblFrame', 'FrameScrollBox', 'lblFrameRate', 'FrameRateScrollBox', 'lblFrameLimit',
                    'StartFrameScrollBox', 'EndFrameScrollBox', 'StretchCheckBox', 'ExtrudeCheckBox',
                    'AddButton', 'SelAddButton', 'lblSelAdd', 'FrameScrollBar',
                    'KeyFrameEditor', 'ShapeEditor', 'QuitDialog', 'AboutDialog', 'BrowserDialog']
        self.organise() # Properly organise the widgets 
    def handleevent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if self.widgets['StickEditor'].selected: self.changeframe(self.data['frame']+1)
            if event.key == pygame.K_LEFT:
                if self.widgets['StickEditor'].selected: self.changeframe(self.data['frame']-1)
    def changeframe(self, frame, updatescrollbar=True):
        self.data['frame'] = frame
        changeFrame(self.data['scene'], int(frame))
        self.data['camera']['pos'].setframe(self.data['frame'])
        self.data['camera']['zoom'].setframe(self.data['frame'])
        
        if not self.data['editing'] == []: self.widgets['ShapeEditor'].changelimb()
        self.widgets['FrameScrollBox'].changetext(str(int(frame)))
        
        if self.data['OnionSkinning']: self.widgets['StickEditor'].drawonion() #thread.start_new_thread(self.widgets['StickEditor'].drawonion, ())
        self.widgets['StickEditor'].draw()
        if self.widgets['KeyFrameEditor'].visible: self.widgets['KeyFrameEditor'].draw()
        if updatescrollbar:
            self.widgets['FrameScrollBar'].scrollto(frame)
    def draw(self):
        #self.image.fill((0,0,0))
        #self.image.blit(pygame.transform.scale(self.topgradient, (self.size.x, self.topgradient.get_height())), (0,0))
        self.drawwidgets()
#        self.mousemask.set_alpha(100)
#        self.image.blit(self.mousemask, (0,0))
#        self.mousemask.set_alpha(255)

        self.redraw = True
    def drawbase(self):
        self.image.fill((0,0,0))
        self.image.blit(pygame.transform.scale(self.topgradient, (self.size.x, self.topgradient.get_height())), (0,0))
        self.window.fullredraw = True
    def organise(self):
        self.widgets['StickEditor'].resize(self.widgets['StickEditor'].pos, Vector(self.size.x-self.widgets['StickEditor'].pos.x - (self.widgets['ShapeEditor'].size.x if self.widgets['ShapeEditor'].visible else 0),
                                           self.size.y-self.widgets['StickEditor'].pos.y-20 - (self.widgets['KeyFrameEditor'].size.y if self.widgets['KeyFrameEditor'].visible else 0)))
        self.widgets['KeyFrameEditor'].resize(Vector(0, self.size.y-200-20), Vector(self.size.x,200))
        self.widgets['ShapeEditor'].resize(Vector(self.size[0]-300,50), Vector(300,self.size[1]-70))
        self.widgets['FrameScrollBar'].resize(Vector(0, self.size.y-self.widgets['FrameScrollBar'].size.y), Vector(self.size.x, self.widgets['FrameScrollBar'].size.y))
        self.widgets['EditorMenuBar'].resize(Vector(0, 0), Vector(self.size.x, self.widgets['EditorMenuBar'].size.y))
        self.widgets['BrowserDialog'].resize(Vector(0, 0), self.size)
        
        # Organise buttons down the left
        vertobjs = 12
        top = 100
        botspace = 50 + (self.widgets['KeyFrameEditor'].size.y if self.widgets['KeyFrameEditor'].visible else 0)
        objs = [['StretchCheckBox'], ['ExtrudeCheckBox'], ['lblSelAdd'], ['SelAddButton'], ['AddButton'], ['PlayButton'], ['CameraKeysButton'], ['lblFrame', 'FrameScrollBox'], ['lblFrameLimit'], ['StartFrameScrollBox', 'EndFrameScrollBox'], ['lblFrameRate'], ['FrameRateScrollBox']]
        for i in range(min(12,len(objs))):
            for obj in objs[i]:
                self.widgets[obj].pos.y = (self.size.y-top-botspace)/vertobjs*i+top

class EditorMenuBar(widgets.MenuBar):
    def setup(self):
        self.menusetup([("File", [("New", "new"), ("Open", "open"), ("Save", "save"), ("Import", "import"), ("Export", "export"), ("Render", "render"), ("Quit", "quit")]),
                        ("Edit", [("Delete", "delete"), ("Shape", "editshape"), ("Keyframes", "editkeys"), ("Toggle OnionSkinning", "toggleonion")]), ("Help",[("About", "showabout"), ("StickyPy Website", "website"), ("StickyPy Tutorial", "tutorial")])])
        self.texback = self.container.window.resources['textbox']
        self.draw()
    def menuaction(self, selected):
        if selected == "new":
            self.data['scene'] = dict(self.data['scene'], cartesian=KeyFrame(True), static=KeyFrame(True), hidden=KeyFrame(True), children=[])
            self.container.changeframe(1)
        if selected == "quit":
            self.container.widgets['QuitDialog'].disabled = False
            self.container.widgets['QuitDialog'].visible = True
        elif selected == "save":
            self.container.widgets['BrowserDialog'].visible = True
            self.container.widgets['BrowserDialog'].disabled = False
            self.container.widgets['BrowserDialog'].changemode("save")
            #filename = "test"
            #if len(self.container.widgets['FileName'].text) > 0: filename = self.container.widgets['FileName'].text 
            #file = open(filename + ".sps", "w")
            #pickle.Pickler(file).dump({'scene':self.data['scene'], 'camera':self.data['camera'], 'framerate':self.data['framerate'], 'framelimit':self.data['framelimit']})
        elif selected == "open":
            #filename = "test"
            #if len(self.container.widgets['FileName'].text) > 0: filename = self.container.widgets['FileName'].text
            #file = open(filename + ".sps", "r")
            #concatDict(self.data, pickle.Unpickler(file).load())
            #self.container.changeframe(1)
            self.container.widgets['BrowserDialog'].visible = True
            self.container.widgets['BrowserDialog'].disabled = False
            self.container.widgets['BrowserDialog'].changemode("load")
        elif selected == "delete":
            deleteVerts(self.data['editing'], self.data['scene'])
        elif selected == "toggleonion":
            self.data['OnionSkinning'] = not self.data['OnionSkinning']
            self.container.widgets['StickEditor'].draw()
        elif selected == "editshape":
            if not self.data['editing'] == []:
                self.container.widgets['ShapeEditor'].visible = True
                self.container.widgets['ShapeEditor'].changelimb()
                self.container.organise()
        elif selected == "editkeys":
            self.container.widgets['KeyFrameEditor'].changekeys(self.data['editing'])
            self.container.widgets['KeyFrameEditor'].show()
        elif selected == "showabout":
            print "StickyPy - Python Stick Figure Animation Program by Joshua Worth. Version: " + self.data['version']
            self.container.widgets['AboutDialog'].visible = True
            self.container.widgets['AboutDialog'].enable()
        elif selected == "website":
            webbrowser.open("http://stickypy.sourceforge.net")
        elif selected == "tutorial":
            webbrowser.open("http://stickypy.sourceforge.net/texttutorial.html")
        elif selected == "render":
            for i in range(self.data['framelimit'][1]):
                self.data['playing'] = True
                self.container.changeframe(i)
                if float(self.data['widgets'].container.widgets['StickEditor'].size.y) / float(self.data['widgets'].container.widgets['StickEditor'].size.x) < float(self.data['camera']['size'].y) / self.data['camera']['size'].x: 
                    self.data['zoom'] = float(self.data['widgets'].container.widgets['StickEditor'].size.y) / self.data['camera']['size'].y / self.data['camera']['zoom'].setframe(i)
                else:
                    self.data['zoom'] = float(self.data['widgets'].container.widgets['StickEditor'].size.x) / self.data['camera']['size'].x / self.data['camera']['zoom'].setframe(i)
                
                self.data['panning'] = -Vector(self.data['camera']['pos'].setframe(i))*self.data['zoom']
                pygame.image.save(self.container.widgets['StickEditor'].image, "render/"+("0"*(4-len(str(i)))+str(i))+".jpg")
                self.data['playing'] = False
        elif selected == "export":
            self.container.widgets['BrowserDialog'].visible = True
            self.container.widgets['BrowserDialog'].disabled = False
            self.container.widgets['BrowserDialog'].changemode("export")

class FrameScrollBar(widgets.ScrollBar):
    def setup(self):
        self.scrollbarsetup(False, self.data['framelimit'], 1)
    def always(self):
        if self.data['playing']:
            if self.drag:
                self.scroll()
            else:
                self.value = float(self.data['frame'])
                self.draw()
    def scroll(self):
        if self.value < self.range[0]: self.value = self.range[0]
        if self.value > self.range[1]: self.value = self.range[1]
        self.data['frame'] = int(self.value)
        if not self.data['playing']:
            self.container.changeframe(int(self.value), False)

class FrameScrollBox(widgets.NumberScrollBox):
    def setup(self):
        self.textboxsetup(str(self.data['frame']))
        self.comment = "Frame to display and edit"
    def edited(self):
        try:
            self.container.changeframe(int(float(self.text)))
        except:
            pass
        
class FrameRateScrollBox(widgets.NumberScrollBox):
    def setup(self):
        self.textboxsetup(str(self.data['framerate']))
        self.comment = "Frames per second for animation playback"
    def validate(self):
        try:
            self.text = str(max(float(self.text), 1))
        except:
            self.text = self.origtext
        self.draw()
    def edited(self):
        try:
            if int(float(self.text)) > 0:
                self.data['framerate'] = int(float(self.text))
        except:
            pass

class StartFrameScrollBox(widgets.NumberScrollBox):
    def setup(self):
        self.textboxsetup(str(self.data['framelimit'][0]))
        self.comment = "The first frame of the animation for playing and rendering"
    def validate(self):
        try:
            self.text = str(min(float(self.text), self.data['framelimit'][1]))
        except:
            self.text = self.origtext
        self.draw()
    def edited(self):
        try:
            if int(float(self.text)) < self.data['framelimit'][1]:
                self.data['framelimit'][0] = int(float(self.text))
                self.container.widgets['FrameScrollBar'].range[0] = self.data['framelimit'][0]
                self.container.widgets['FrameScrollBar'].draw()
        except:
            pass

class EndFrameScrollBox(widgets.NumberScrollBox):
    def setup(self):
        self.textboxsetup(str(self.data['framelimit'][1]))
        self.comment = "The last frame of the animation for playing and rendering"
    def validate(self):
        try:
            self.text = str(max(float(self.text), self.data['framelimit'][0]))
            
        except:
            self.text = self.origtext
        self.draw()
    def edited(self):
        try:
            if int(float(self.text)) > self.data['framelimit'][0]:
                self.data['framelimit'][1] = int(float(self.text))
                self.container.widgets['FrameScrollBar'].range[1] = self.data['framelimit'][1]
                self.container.widgets['FrameScrollBar'].draw() 
        except:
            pass

class PlayButton(widgets.Button):
    def setup(self):
        self.buttonsetup("Play")
        self.comment = "Play the animation, right click to reset to frame 1"
    def lrelease(self):
        if self.hover and self.selected:
            self.data['playing'] = not self.data['playing']
            if self.data['playing']:
                self.data['playingstart'] = pygame.time.get_ticks()
                self.changelabel("Stop")
            elif not self.data['playing']:
                self.changelabel("Start")
                self.container.widgets['StickEditor'].draw()
        
        self.draw()
    def rclick(self):
        if self.hover and self.selected:
            self.data['playingstart'] = pygame.time.get_ticks()
            self.container.changeframe(1)
    def handleevent(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.data['playing'] = not self.data['playing']
            if self.data['playing']:
                self.data['playingstart'] = pygame.time.get_ticks()
                self.changelabel("Stop")
            elif not self.data['playing']:
                self.changelabel("Start")
                self.container.widgets['StickEditor'].draw()
            
class AddButton(widgets.Button):
    def setup(self):
        self.buttonsetup("Add Stick")
        self.comment = "Add the selected figure from above"
    def lrelease(self):
        if self.hover and self.selected:
            self.data['scene']['children'].append(deepcopy(dict(self.data['PresetFigures'][self.container.widgets['SelAddButton'].label], pos=KeyFrame((100,100)))))
            self.container.changeframe(self.data['frame'])
        self.draw()

class CameraKeysButton(widgets.Button):
    def setup(self):
        self.buttonsetup("Edit Camera Keyframes")
        self.comment = "Edit the keyframes of the camera (blue rectangle)"
    def lrelease(self):
        if self.hover and self.selected:
            self.container.widgets['KeyFrameEditor'].changekeys([self.data['camera']])
            self.container.widgets['KeyFrameEditor'].show()
        self.draw()
        
class SelAddButton(widgets.Button):
    def setup(self):
        self.buttonsetup("StickMan")
        self.texbutup = self.container.window.resources['textbox']
        self.texbutdown = self.container.window.resources['textbox']
        self.draw()
        self.comment = "Select the figure you intend to add to the scene"
    def lrelease(self):
        if self.hover and self.selected:
            self.container.window.menu.showmenu([("StickMan", "StickMan")], Vector(self.pos[0], self.pos[1] + self.size[1]), self, 30)
        self.draw()
    def menuaction(self, selection):
        self.changelabel(selection)

#class AboutDialog(widgets.BaseWidget):
#    def __init__(self, pos, version, data):
#        self.pos = pos
#        self.data = data
#        self.image = pygame.image.load("logo.png")
#        font = pygame.font.Font(pygame.font.get_default_font(), 15)
#        self.size = Vector(self.image.get_size())
#        self.image.blit(font.render("Version: " + version, True, (0,0,0)), (1,self.size.y-16))
#        self.visible = False
#        
#        self.oldkeys = []
#        self.oldmousepos = (0,0)
#        self.oldmousebut = (False,False,False)
#        self.oldhover = False
#        self.disabled = False
#        self.hover = False
#        self.comment = ""
#        self.redraw = False
#    def mousemove(self):
#        self.visible = False
#        self.disabled = True
#        self.data['fullredraw'] = True
#    def draw(self):
#        pass

class AboutDialog(widgets.BaseWidget):
    def setup(self):
        self.image = self.container.window.resources['logo']
        self.size = Vector(self.image.get_size())
        self.visible = False
        self.disabled = False
        self.hover = False
        self.comment = ""
        self.draw()
    def mousemove(self):
        self.visible = False
        self.disabled = True
        self.container.window.fullredraw = True
    def draw(self):
        font = pygame.font.Font(pygame.font.get_default_font(), 15)
        self.image.blit(font.render("Version: " + self.data['version'], True, (0,0,0)), (1,self.size.y-16))

class StretchCheckBox(widgets.CheckBox):
    def setup(self):
        self.checkboxsetup("Stretch Mode")
        self.checked = False
        self.comment = "Check this box to change the limb distance aswell as its angle"

class ExtrudeCheckBox(widgets.CheckBox):
    def setup(self):
        self.checkboxsetup("Extrude Mode")
        self.checked = False
        self.comment = "Check this box to extrude vertices by clicking and dragging"

class BrowserDialog(widgets.WidgetContainer):
    def __init__(self, pos, size, container, mainwindow, data):
        self.setupcontainer(pos, size, mainwindow, container, data)
        self.widgets = {'FileName':widgets.TextBox(Vector(size.x/2+10,size.y-60), Vector(size.x/2,30), self, data),
                        'ScrollBar':BrowserScrollBar(Vector(400,0), Vector(20, size[1]), self, data),
                        'FileBrowser':FileBrowser(Vector(0,0), Vector(400,size[1]), self, data),
                        'AcceptButton':BrowserAcceptButton(Vector(0,size.y-30), Vector(size.x/2-10,30), self, data),
                        'CancelButton':CancelButton(Vector(size.x/2+10,size.y-30), Vector(size.x/2-10,30), self, data)}
        self.widgets['FileBrowser'].setdirlist()
        self.order = ['FileBrowser', 'ScrollBar', 'CancelButton', 'AcceptButton', 'FileName']
        self.mode = "" # Browser mode: save, load
        self.visible = False
        self.disabled = True
        self.organise()

    def changemode(self, mode):
        if mode == "save":
            self.mode = "save"
            self.widgets['AcceptButton'].changelabel("Save")
        elif mode == "load":
            self.mode = "load"
            self.widgets['AcceptButton'].changelabel("Load")
        elif mode == "export":
            self.mode = "export"
            self.widgets['AcceptButton'].changelabel("Export")
        else:
            print "Invalid mode for file browser: " + mode
            raise RuntimeError

    def resize(self, pos, size):
        self.pos = pos
        if size[0] < 1: size[0] = 1
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.setup() 
        self.organise()
        self.draw()

    def draw(self):
        self.drawwidgets()
        self.redraw = True

    def organise(self):
        self.widgets['FileName'].resize(Vector(0,self.size.y-70), Vector(self.size.x,30))
        self.widgets['ScrollBar'].resize(Vector(self.size.x-20,0), Vector(20, self.size.y-80))
        self.widgets['FileBrowser'].resize(Vector(0,0), Vector(self.size.x-20,self.size.y-80))
        self.widgets['AcceptButton'].resize(Vector(0,self.size.y-30), Vector(self.size.x/2-10,30))
        self.widgets['CancelButton'].resize(Vector(self.size.x/2+10,self.size.y-30), Vector(self.size.x/2-10,30))
    
class FileBrowser(widgets.BaseWidget):
    def setup(self):
        t = os.getcwd()
        #os.chdir("..")
        self.path = os.getcwd()
        os.chdir(t)
        #self.setdirlist()
        self.fontsize = 20
        self.visible = True
        self.disabled = False
        self.offset = 0
    def mousemove(self):
        if self.hover:
            self.draw()
    def mouseout(self):
        self.draw()
    def mwheelup(self):
        self.offset -= 1
        self.offset = min(len(self.dirlist), max(0, self.offset))
        self.container.widgets['ScrollBar'].scrollto(self.offset)
        self.draw()
    def mwheeldown(self):
        self.offset += 1
        self.offset = min(len(self.dirlist), max(0, self.offset))
        self.container.widgets['ScrollBar'].scrollto(self.offset)
        self.draw()
    def lclick(self):
        if self.hover:

            self.selected = (int(self.mousepos[1] - self.pos[1] + self.offset*self.fontsize) / self.fontsize)

            if self.selected >= len(self.dirlist):
                return

            path = os.path.join(self.path, self.dirlist[self.selected])
            if os.path.isdir(os.path.join(self.path, self.dirlist[self.selected])):
                os.chdir(path)
                self.path = os.getcwd()
                self.setdirlist()
                self.offset = 0
                self.container.widgets['ScrollBar'].scrollto(self.offset)
            else:
                if self.container.widgets['FileName'].text == self.dirlist[self.selected]:
                    self.container.widgets['AcceptButton'].action()
                else:
                    self.container.widgets['FileName'].changetext(self.dirlist[self.selected])
            self.draw()
    def setdirlist(self):
        self.dirlist = os.listdir(self.path)
        self.dirlist.sort()
        self.dirlist = ["..", "."] + [f for f in self.dirlist if os.path.isdir(os.path.join(self.path, f))] + [f for f in self.dirlist if os.path.isfile(os.path.join(self.path, f))]
        self.container.widgets['ScrollBar'].range[1] = len(self.dirlist)
        self.draw()
    def draw(self):
        self.image.fill((255,255,255))
        font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)
        hovering = (int(self.mousepos[1] - self.pos[1] + self.offset*self.fontsize) / self.fontsize)
        if self.hover and hovering < len(self.dirlist): pygame.draw.rect(self.image, (255,200,0), pygame.Rect((0,self.fontsize*hovering - self.offset*self.fontsize),(self.size[0], self.fontsize)))
        for i in range(len(self.dirlist)):
            colour = [0,0,0]
            if os.path.isdir(os.path.join(self.path, self.dirlist[i])): colour = [0,0,255]
            self.image.blit(font.render(self.dirlist[i], True, colour), (0,self.fontsize*(i - self.offset)))
            
        self.redraw = True

class BrowserScrollBar(widgets.ScrollBar):
    def setup(self):
        self.scrollbarsetup(True, [0,100], 0)
    #def always(self):
    #    if self.data['playing']:
    #        if self.drag:
    #            self.scroll()
    #        else:
    #            self.value = float(self.data['frame'])
    #            self.draw()
    def scroll(self):
        if self.value < self.range[0]: self.value = self.range[0]
        if self.value > self.range[1]: self.value = self.range[1]
        self.container.widgets['FileBrowser'].offset = self.value
        self.container.widgets['FileBrowser'].draw()
        #self.data['frame'] = int(self.value)
        
        #if not self.data['playing']:
            #self.container.changeframe(int(self.value), False)

class BrowserAcceptButton(widgets.Button):
    def setup(self):
        self.buttonsetup("Accept")
        self.comment = "Select file"
    def lrelease(self):
        if self.hover and self.selected:
            self.action()
    def action(self):
        path = os.path.join(self.container.widgets['FileBrowser'].path, self.container.widgets['FileName'].text)
        if self.container.mode == "save":
            if not self.container.widgets['FileName'].text == "":
                filename = self.container.widgets['FileName'].text
                if not filename[-4:] == ".sps": filename += ".sps"
                file = open(filename, "w")
                pickle.Pickler(file).dump({'scene':self.data['scene'], 'camera':self.data['camera'], 'framerate':self.data['framerate'], 'framelimit':self.data['framelimit']})
        elif self.container.mode == "load":
            if  path[-4:] == ".sps":
                file = open(path, "r")
                concatDict(self.data, pickle.Unpickler(file).load())
                self.container.container.widgets['StartFrameScrollBox'].changetext(str(self.data['framelimit'][0]))
                self.container.container.widgets['EndFrameScrollBox'].changetext(str(self.data['framelimit'][1]))
                self.container.container.widgets['FrameRateScrollBox'].changetext(str(self.data['framerate']))
                self.container.container.changeframe(1)

        elif self.container.mode == "export":

            filename = "test";
            if len(self.container.widgets['FileName'].text) > 0: 
                filename = self.container.widgets['FileName'].text 

            if not filename[-4:] == ".spe": 
                filename += ".spe"

            file = open(filename, "w")
            file.write(Export(self.data['scene']))

        self.container.visible = False
        self.container.disabled = True

class QuitDialog(widgets.WidgetContainer):
    def __init__(self, pos, size, container, mainwindow, data):
        self.setupcontainer(pos, size, mainwindow, container, data)
        self.widgets = {'QuitButton':QuitButton(Vector(0,size.y-30), Vector(size.x/2-10,30), self, data),
                        'CancelButton':CancelButton(Vector(size.x/2+10,size.y-30), Vector(size.x/2-10,30), self, data),
                        'lblQuit':widgets.Label(Vector(0,20), Vector(size.x, size.y-50), "Are you sure?", (255,255,255)),
                        'DragBar':widgets.DragBar(Vector(0,0), Vector(size.x,20), self, data)}
        self.order = ['CancelButton', 'QuitButton', 'lblQuit', 'DragBar']
        self.widgets['CancelButton'].comment = "Closes the quit dialog (Good decision)"
        self.visible = False
        self.disabled = True
    def resize(self, pos, size):
        self.pos = pos
        if size[0] < 1: size[0] = 1
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.setup() 
        self.organise()
        self.draw()
    def draw(self):
        #self.image.fill((0,0,0))
        self.drawwidgets()
        
        self.redraw = True
    def organise(self):
        pass

class QuitButton(widgets.Button):
    def setup(self):
        self.buttonsetup("Quit")
        self.comment = "Quits StickyPy (Please stay! There is so much more that you haven't done with me!)"
    def lrelease(self):
        if self.hover and self.selected:
            sys.exit()

class CancelButton(widgets.Button):
    def setup(self):
        self.buttonsetup("Cancel")
        self.comment = "Closes dialog"
        #self.comment = "Closes the quit dialog (Good decision)"
    def lrelease(self):
        if self.hover and self.selected:
            self.container.visible = False
            self.container.disabled = True

#def FileBrowser(directory):
