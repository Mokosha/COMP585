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

import widgets
from objs import *
from defs import *
from colorsys import *

# Shape editor container
class ShapeEditor(widgets.WidgetContainer):
    def __init__(self, pos, size, container, mainwindow, data):
        self.limb = None
        self.setupcontainer(pos, size, mainwindow, container, data)
        
        self.widgets = {'SelShapeButton':SelShapeButton(Vector(120,10), Vector(150,30), self, data),
                        'lblAng':widgets.Label(Vector(10,100), Vector(100,20), "Angle:"),
                        'AngTextBox':ValEditTextBox('ang', Vector(120,100), Vector(160,20), self, data, "Angle of limb relative to its parent's angle. Ignored when Cartesian is on"),
                        'lblDist':widgets.Label(Vector(10,130), Vector(100,20), "Distance:"),
                        'DistTextBox':ValEditTextBox('dist', Vector(120,130), Vector(160,20), self, data, "Distance of limb from its parent. Ignored when Cartesian is on", (-300000, 300000)),
                        'lblWidth':widgets.Label(Vector(10,160), Vector(100,20), "Width:"),
                        'WidthTextBox':ValEditTextBox('width', Vector(120,160), Vector(160,20), self, data, "Width of limb for use in most shapes"),
                        'lblPos':widgets.Label(Vector(10,190), Vector(100,20), "Position:"),
                        'XPosTextBox':XPosTextBox(Vector(120,190), Vector(70,20), self, data),
                        'lblPosSep':widgets.Label(Vector(190,190), Vector(20,20), "X"),
                        'YPosTextBox':YPosTextBox(Vector(210,190), Vector(70,20), self, data),
                        'lblColour':widgets.Label(Vector(10,220), Vector(100,20), "Colour:"),
                        'ShowColourButton':ShowColourButton(Vector(120,220), Vector(160,20), self, data),
                        'HiddenCheckBox':HiddenCheckBox(Vector(10,50), Vector(90,30), self, data),
                        'CartesianCheckBox':CartesianCheckBox(Vector(100,50), Vector(100,30), self, data),
                        'StaticCheckBox':StaticCheckBox(Vector(200,50), Vector(90,30), self, data),
                        'TexLineOptions':TexLineOptions(Vector(10,250), Vector(280,200), self, mainwindow, data),
                        'TexCircleOptions':TexCircleOptions(Vector(10,250), Vector(280,200), self, mainwindow, data),
                        'TexTextOptions':TexTextOptions(Vector(10,250), Vector(280,200), self, mainwindow, data),
                        'TexImageOptions':TexImageOptions(Vector(10,250), Vector(280,200), self, mainwindow, data),
                        'Preview':Preview(Vector(10,size.y - 290), Vector(280,200), self, data),
                        'lblSelShape':widgets.Label(Vector(40,10), Vector(70,30), "Shape:"),
                        'ColourChooser':ColourChooser(Vector(120,240), Vector(160,180), self, mainwindow, data),
                        'CloseShapeEditorButton':CloseShapeEditorButton(Vector(0,0), Vector(30,30), self, data)}
        self.order = ['Preview', 'SelShapeButton', 'HiddenCheckBox', 'CartesianCheckBox', 'StaticCheckBox', 'lblAng', 'AngTextBox', 'lblDist', 'DistTextBox', 'lblWidth', 'WidthTextBox',
                      'lblPos', 'XPosTextBox', 'lblPosSep', 'YPosTextBox', 'lblColour', 'ShowColourButton', 'lblSelShape', 'TexLineOptions', 'TexCircleOptions', 'TexTextOptions', 'TexImageOptions', 'ColourChooser', 'CloseShapeEditorButton']
        
        self.visible = False
    def changeframe(self, frame, updatescrollbar=True):
        pass
    def changelimb(self):
        for widget in ['Preview', 'SelShapeButton', 'HiddenCheckBox', 'CartesianCheckBox', 'StaticCheckBox', 'AngTextBox', 'DistTextBox', 'WidthTextBox', 'TexLineOptions', 'TexCircleOptions', 'TexTextOptions', 'TexImageOptions', 'XPosTextBox', 'YPosTextBox', 'ColourChooser']:
            self.widgets[widget].changelimb()
        self.draw()
    def rrelease(self):
        if self.widgetselected == 0 and self.hover:
            self.window.menu.showmenu([("Close shape editor","close"), ("Edit shape keys", "keys")], self.mousepos, self, 25)
    def resize(self, pos, size):
        self.pos = pos
        if size[0] < 1: size[0] = 1
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.setup()
        self.organise()
        #self.draw()
        self.window.fullredraw = True
    def menuaction(self, selected):
        if selected == "close":
            self.visible = False
            self.container.organise()
        elif selected == "keys":
            self.container.widgets['KeyFrameEditor'].visible = True
            self.container.widgets['KeyFrameEditor'].changekeys([self.data['editing'][0]['shape'].values])
    def draw(self):
        self.drawwidgets()
        if self.data['editing'] == []:
            self.image.set_alpha(150)
            self.disabled = True
        else:
            self.image.set_alpha(255)
            self.disabled = False
        #self.image.blit(self.mousemask, (0,0))
        
        self.redraw = True
    def drawbase(self):
        self.image.fill((100,100,100))
    def organise(self):
        self.widgets['Preview'].pos.y = self.size.y - self.widgets['Preview'].size.y - 10

#Box for sampling the shape without editing the figure itself
class Preview(widgets.BaseWidget):
    def setup(self):
        self.point1 = Vector(40,80)
        self.point2 = Vector(200,180)
        self.limb = None
        self.drag = 0
        self.comment = "Preview of the limb"
    def changelimb(self):
        self.draw()
    def lclick(self):
        self.drag = None
        if self.hover and sqrt((self.mousepos[0] - self.pos[0] - self.point1[0]) ** 2 + (self.mousepos[1] - self.pos[1] - self.point1[1]) ** 2) < self.data['editing'][0]['width'].value/2+2: self.drag = 1
        if self.hover and sqrt((self.mousepos[0] - self.pos[0] - self.point2[0]) ** 2 + (self.mousepos[1] - self.pos[1] - self.point2[1]) ** 2) < self.data['editing'][0]['width'].value/2+2: self.drag = 2
    def lrelease(self):
        if not self.drag == None or self.hover: self.draw()
        self.drag = None
    def mousemove(self):
        if not len(self.data['editing']) == 0 and self.hover:
            if self.drag == 1:
                self.point1 = self.mousepos - self.pos
                self.draw()
            elif self.drag == 2:
                self.point2 = self.mousepos - self.pos
                self.draw()
    def mouseover(self):
        self.draw()
    def mouseout(self):
        self.draw()
    def draw(self):
        self.image.fill((255,255,255))
        if not self.data['editing'][0]['hidden'].value: self.data['editing'][0]['shape'].draw(self.image, self.point1, self.point2, dict(self.data['editing'][0], ang=KeyFrame(direction(self.point1, self.point2)), dist=KeyFrame(distance(self.point1, self.point2))), 1)
        if self.hover and (not self.mousebut[0] or self.selected):
            drawcircle(self.image, (0,0,255), self.point1, (self.data['editing'][0]['width'].value/2+2))
            drawcircle(self.image, (0,255,0), self.point2, (self.data['editing'][0]['width'].value/2+2))
            
        self.redraw = True

#Drop down box to select between shapes like line and circle
class SelShapeButton(widgets.Button):
    def setup(self):
        self.buttonsetup("Line")
        self.texbutup = self.container.window.resources['textbox']
        self.texbutdown = self.container.window.resources['textbox']
        self.limb = None
        self.draw()
        self.comment = "The shape of the limb to be drawn on the screen"
    def changelimb(self):
        if self.data['editing'][0]['shape'].values['shape'].value == "line":
            self.label = "Line"
        elif self.data['editing'][0]['shape'].values['shape'].value == "circle":
            self.label = "Circle"
        elif self.data['editing'][0]['shape'].values['shape'].value == "text":
            self.label = "Text"
        elif self.data['editing'][0]['shape'].values['shape'].value == "image":
            self.label = "Image"
        self.draw()
    def lrelease(self):
        if self.hover:
            self.container.window.menu.showmenu([("Line", "Line"), ("Circle", "Circle"), ("Text", "Text"), ("Image", "Image")], Vector(self.pos[0], self.pos[1] + self.size[1])+self.container.pos, self, 30)
        self.draw()
    def menuaction(self, selection):
        for limb in self.data['editing']:
            if selection == "Line":
                limb['shape'].values['shape'].value = "line"
            elif selection == "Circle":
                limb['shape'].values['shape'].value = "circle"
            elif selection == "Text":
                limb['shape'].values['shape'].value = "text"
            elif selection == "Image":
                limb['shape'].values['shape'].value = "image"
        self.container.changelimb()
        self.changelabel(selection)
        self.container.widgets['Preview'].draw()

#Toggle hidden option of a limb. Essentially prevents shape class from being called when drawing figure
class HiddenCheckBox(widgets.CheckBox):
    def setup(self):
        self.checkboxsetup("Hidden")
        self.checked = False
        self.comment = "Prevents the limb from being drawn"
    def changelimb(self):
        self.checked = self.data['editing'][0]['hidden'].value
        self.draw()
    def changed(self):
        for limb in self.data['editing']:
            limb['hidden'].value = self.checked
        self.container.widgets['Preview'].draw()
        self.container.container.widgets['StickEditor'].draw()

#Toggle cartesian option of a limb. Takes offset from Pos value rather than Ang and Dist values
class CartesianCheckBox(widgets.CheckBox):
    def setup(self):
        self.checkboxsetup("Cartesian")
        self.checked = False
        self.comment = "Uses Cartesian (X, Y) coordinates rather than polar (Angle, Distance)"
    def changelimb(self):
        self.checked = self.data['editing'][0]['cartesian'].value
        self.draw()
    def changed(self):
        for limb in self.data['editing']:
            limb['cartesian'].value = self.checked
        self.container.container.widgets['StickEditor'].draw()

#Toggle static option of a limb. Prevents limb from being moved in the editing window
class StaticCheckBox(widgets.CheckBox):
    def setup(self):
        self.checkboxsetup("Static")
        self.checked = False
        self.comment = "Prevents the limb from being modified in the editing window"
    def changelimb(self):
        self.checked = self.data['editing'][0]['static'].value
        self.draw()
    def changed(self):
        for limb in self.data['editing']:
            limb['static'].value = self.checked

#Modifies Ang value of limb as part of a polar coordinate
class AngTextBox(widgets.NumberScrollBox):
    def changelimb(self):
        self.keyrange = (45, 57)
        if not self.editing:
            self.textboxsetup(str(self.data['editing'][0]['ang'].value))
            self.draw()
    def edited(self):
        for limb in self.data['editing']:
            try:
                limb['ang'].value = abs(float(self.text))
            except:
                pass
        self.container.container.widgets['StickEditor'].draw()
    def scrolled(self, offset):
        for limb in self.data['editing']:
            try:
                limb['ang'] = abs(limb['ang'] + offset)
            except:
                pass
        self.container.container.widgets['StickEditor'].draw()

#Modifies Dist value of limb as part of a polar coordinate
class DistTextBox(widgets.TextBox):
    def changelimb(self):
        self.keyrange = (45, 57)
        if not self.editing:
            self.textboxsetup(str(self.data['editing'][0]['dist']))
            self.draw()
    def edited(self):
        for limb in self.data['editing']:
            try:
                print abs(float(self.text))
                if abs(float(self.text)) < 30000:
                    limb['dist'] = abs(float(self.text))
            except:
                pass
        self.container.container.widgets['StickEditor'].draw()

#Modifies Width value of limb. The with is used to determine the side of drag points in the editing view, and it used for thickness values in a lot of shapes
class WidthTextBox(widgets.TextBox):
    def changelimb(self):
        self.keyrange  = (45, 57)
        if not self.editing:
            self.textboxsetup(str(self.data['editing'][0]['width']))
            self.draw()
    def edited(self):
        for limb in self.data['editing']:
            try:
                limb['width'] = abs(float(self.text))
            except:
                pass
        self.container.widgets['Preview'].draw()
        self.container.container.widgets['StickEditor'].draw()

#Modifies X Position value of limb as part of a Cartesian coordinate
class XPosTextBox(widgets.NumberScrollBox):
    def setup(self):
        self.textboxsetup()
        self.comment = "The limb's X (horizontal) offset from its parent. Ignored when Cartesian isn't checked"
    def changelimb(self):
        self.keyrange  = (45, 57)
        if not self.editing:
            self.textboxsetup(str(self.data['editing'][0]['pos'].value[0]))
            self.draw()
    def edited(self):
        for limb in self.data['editing']:
            try:
                limb['pos'].value[0] = float(self.text)
            except:
                pass
        self.container.container.widgets['StickEditor'].draw()

#Modifies Y Position value of limb as part of a Cartesian coordinate
class YPosTextBox(widgets.NumberScrollBox):
    def setup(self):
        self.textboxsetup()
        self.comment = "The limb's Y (vertical) offset from its parent. Ignored when Cartesian isn't checked"
    def changelimb(self):
        self.keyrange  = (45, 57)
        if not self.editing:
            self.textboxsetup(str(self.data['editing'][0]['pos'].value[1]))
            self.draw()
    def edited(self):
        for limb in self.data['editing']:
            try:
                limb['pos'].value[1] = float(self.text)
            except:
                pass
        self.container.container.widgets['StickEditor'].draw()

#Container for TexLine specific values
class TexLineOptions(widgets.WidgetContainer):
    def __init__(self, pos, size, container, mainwindow, data):
        self.setupcontainer(pos, size, mainwindow, container, data)
        self.limb = None
        self.widgets = {'CapsCheckBox':LineCapsCheckBox(Vector(0,10), Vector(280,30), self, data)}
        self.order = ['CapsCheckBox']
        self.visible = False
#        self.disabled = True
    def changelimb(self):
        if self.data['editing'][0]['shape'].values['shape'].value == "line":
            self.widgets['CapsCheckBox'].changelimb()
            self.visible = True
        else:
            self.visible = False
        self.draw()
    def resize(self, pos, size):
        self.pos = pos
        if size[0] < 1: size[0] = 1
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.setup()
        self.organise()
        self.draw()
    def menuaction(self, selected):
        if selected == "close":
            self.visible = False
    def draw(self):
        self.drawwidgets()
        #self.image.blit(self.mousemask, (0,0))
        
        self.redraw = True
    def drawbase(self):
        self.image.fill((100,100,100))
    def organise(self):
        pass

#Toggles Caps of TexLine
class LineCapsCheckBox(widgets.CheckBox):
    def setup(self):
        self.checkboxsetup("Caps")
        self.checked = False
        self.comment = "Adds round caps to the end of the line"
    def changelimb(self):
        #try:
            #self.checked = self.data['editing'][0]['shape'].value.caps.value
        self.checked = self.data['editing'][0]['shape'].values['caps'].value
        #except: pass
        self.draw()
    def rrelease(self):
        if self.selected and self.hover:
            #print self.mousepos, self.container.pos
            self.container.window.menu.showmenu([("Insert keyframe", "insertkey")], self.container.window.mousepos, self, 20)
    def menuaction(self, selection):
        if selection == "insertkey":
            for limb in self.data['editing']:
                #insertKey(limb['shape'].caps, [self.data['frame'], self.checked], interpol="const")
                try:
                    limb['shape'].values['caps'].insertkey()
                except:
                    pass
                #updateUnKeyed(limb)
                
    def changed(self):
        for limb in self.data['editing']:
            try:
                limb['shape'].values['caps'].value = self.checked
            except:
                pass
            #updateUnKeyed(limb)
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()

class TexCircleOptions(widgets.WidgetContainer):
    def __init__(self, pos, size, container, mainwindow, data):
        self.setupcontainer(pos, size, mainwindow, container, data)
        self.limb = None
        self.widgets = {'FillCheckBox':CircleFillCheckBox(Vector(0,10), Vector(280,30), self, data)}
        self.order = ['FillCheckBox']
        self.visible = False
#        self.disabled = True
    def changelimb(self):
        if self.data['editing'][0]['shape'].values['shape'].value == "circle":
            self.widgets['FillCheckBox'].changelimb()
            self.visible = True
        else:
            self.visible = False
        self.draw()
    def resize(self, pos, size):
        self.pos = pos
        if size[0] < 1: size[0] = 1
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.setup()
        self.organise()
        self.draw()
    def menuaction(self, selected):
        if selected == "close":
            self.visible = False
    def draw(self):
        self.drawwidgets()
        #self.image.blit(self.mousemask, (0,0))
        
        self.redraw = True
    def drawbase(self):
        self.image.fill((100,100,100))
    def organise(self):
        pass

class CircleFillCheckBox(widgets.CheckBox):
    def setup(self):
        self.checkboxsetup("Fill")
        self.checked = False
        self.comment = "Fills the circle with the limb colour"
    def changelimb(self):
        #self.checked = self.data['editing'][0]['shape'].value.fill.value
        self.checked = self.data['editing'][0]['shape'].values['fill'].value
        self.draw()
    def rrelease(self):
        if self.selected and self.hover:
            self.container.window.menu.showmenu([("Insert keyframe", "insertkey")], self.container.window.mousepos, self, 20)
    def menuaction(self, selection):
        if selection == "insertkey":
            for limb in self.data['editing']:
                limb['shape'].insertKey()
                #updateUnKeyed(limb)
    def changed(self):
        for limb in self.data['editing']:
            limb['shape'].values['fill'].value = self.checked
            #updateUnKeyed(limb)
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()

class TexTextOptions(widgets.WidgetContainer):
    def __init__(self, pos, size, container, mainwindow, data):
        self.setupcontainer(pos, size, mainwindow, container, data)
        self.limb = None
        self.widgets = {'FlipCheckBox':TextFlipCheckBox(Vector(0,50), Vector(280,30), self, data),
                    'TextTextTextBox':TextTextTextBox(Vector(0,10), Vector(280,30), self, data)}
        self.order = ['FlipCheckBox', 'TextTextTextBox']

        self.visible = False
#        self.disabled = True
    def changelimb(self):
        if self.data['editing'][0]['shape'].values['shape'].value == "text":
            self.widgets['FlipCheckBox'].changelimb()
            self.visible = True
        else:
            self.visible = False
        self.draw()
    def resize(self, pos, size):
        self.pos = pos
        if size[0] < 1: size[0] = 1
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.setup()
        self.organise()
        self.draw()
    def menuaction(self, selected):
        if selected == "close":
            self.visible = False
    def draw(self):
        self.drawwidgets()
        #self.image.blit(self.mousemask, (0,0))
        
        self.redraw = True
    def drawbase(self):
        self.image.fill((100,100,100))
    def organise(self):
        pass

class TextFlipCheckBox(widgets.CheckBox):
    def setup(self):
        self.checkboxsetup("Flip")
        self.checked = False
        self.comment = "Flips the text so it isn't upside down when rotated"
    def changelimb(self):
        self.checked = self.data['editing'][0]['shape'].values['flip'].value
        self.draw()
    def rrelease(self):
        if self.selected and self.hover:
            self.container.window.menu.showmenu([("Insert keyframe", "insertkey")], self.container.window.mousepos, self, 20)
    def menuaction(self, selection):
        if selection == "insertkey":
            for limb in self.data['editing']:
                limb['shape'].insertKey()
                #updateUnKeyed(limb)
    def changed(self):
        for limb in self.data['editing']:
            limb['shape'].values['flip'].value = self.checked
            #updateUnKeyed(limb)
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()

class TextTextTextBox(widgets.TextBox): #lol
    def setup(self):
        self.textboxsetup("text")
        self.checked = False
        self.comment = "The text to be displayed as the limb"
    def changelimb(self):
        self.checked = self.data['editing'][0]['shape'].values['text'].value
        self.draw()
    def rrelease(self):
        if self.selected and self.hover:
            self.container.window.menu.showmenu([("Insert keyframe", "insertkey")], self.container.window.mousepos, self, 20)
    def menuaction(self, selection):
        if selection == "insertkey":
            for limb in self.data['editing']:
                limb['shape'].insertKey()
                #updateUnKeyed(limb)
    def edited(self):
        for limb in self.data['editing']:
            limb['shape'].values['text'].value = self.text
            #print "tet"
            #updateUnKeyed(limb)
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()

#Picture Options
class TexImageOptions(widgets.WidgetContainer):
    def __init__(self, pos, size, container, mainwindow, data):
        self.setupcontainer(pos, size, mainwindow, container, data)
        self.limb = None
        self.widgets = {'FlipCheckBox':ImageFlipCheckBox(Vector(0,50), Vector(280,30), self, data),
                    'FileTextBox':ImageFileTextBox(Vector(0,10), Vector(280,30), self, data)}
        self.order = ['FlipCheckBox', 'FileTextBox']
        self.visible = False
#        self.disabled = True
    def changelimb(self):
        if self.data['editing'][0]['shape'].values['shape'].value == "image":
            self.widgets['FlipCheckBox'].changelimb()
            self.visible = True
        else:
            self.visible = False
        self.draw()
    def resize(self, pos, size):
        self.pos = pos
        if size[0] < 1: size[0] = 1
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.setup()
        self.organise()
        self.draw()
    def menuaction(self, selected):
        if selected == "close":
            self.visible = False
    def draw(self):
        self.drawwidgets()
        #self.image.blit(self.mousemask, (0,0))
        
        self.redraw = True
    def drawbase(self):
        self.image.fill((100,100,100))
    def organise(self):
        pass

class ImageFlipCheckBox(widgets.CheckBox):
    def setup(self):
        self.checkboxsetup("Flip")
        self.checked = False
        self.comment = "Flips the image around the diagonal"
    def changelimb(self):
        self.checked = self.data['editing'][0]['shape'].values['flip'].value
        self.draw()
    def rrelease(self):
        if self.selected and self.hover:
            self.container.window.menu.showmenu([("Insert keyframe", "insertkey")], self.container.window.mousepos, self, 20)
    def menuaction(self, selection):
        if selection == "insertkey":
            for limb in self.data['editing']:
                limb['shape'].insertKey()
                #updateUnKeyed(limb)
    def changed(self):
        for limb in self.data['editing']:
            limb['shape'].values['flip'].value = self.checked
            #updateUnKeyed(limb)
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()

class ImageFileTextBox(widgets.TextBox): #lol
    def setup(self):
        self.textboxsetup("text")
        self.checked = False
        self.comment = "Name of image file to be displayed"
    def changelimb(self):
        self.checked = self.data['editing'][0]['shape'].values['file'].value
        self.draw()
    def rrelease(self):
        if self.selected and self.hover:
            self.container.window.menu.showmenu([("Insert keyframe", "insertkey")], self.container.window.mousepos, self, 20)
    def menuaction(self, selection):
        if selection == "insertkey":
            for limb in self.data['editing']:
                limb['shape'].insertKey()
                #updateUnKeyed(limb)
    def edited(self):
        for limb in self.data['editing']:
            limb['shape'].values['file'].value = self.text
            #print "tet"
            #updateUnKeyed(limb)
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()
#End picture options

class ShowColourButton(widgets.Button):
    def setup(self):
        self.buttonsetup("Pick Colour")
        self.comment = "Limb's colour"
    def lrelease(self):
        if self.hover and self.selected:
            self.container.widgets['ColourChooser'].visible = not self.container.widgets['ColourChooser'].visible
        self.draw()
    def draw(self):
        self.drawbutton()
        try:
            pygame.draw.rect(self.image, self.data['editing'][0]['colour'].value, pygame.Rect(self.size.x-self.size.y, 0, self.size.y, self.size.y))
        except:
            pass
        
        self.redraw = True
    def drawbase(self):
        self.image.fill((100,100,100))

class ColourChooser(widgets.WidgetContainer):
    def __init__(self, pos, size, container, mainwindow, data):
        self.setupcontainer(pos, size, mainwindow, container, data)
        self.colour = (0,0,0)
        self.limb = None
        self.widgets = {'colourWheel':ChooserColourWheel(Vector(0,0), Vector(size.x,size.x-20), self, data),
                        'lblR':widgets.Label(Vector(0,size.x-20), Vector(10,20), "R", [255,255,255]),
                        'RTextBox': ColourRTextBox(Vector(10,size.x-20), Vector(size.x/3-10,20), self, data),
                        'lblG':widgets.Label(Vector(size.x/3,size.x-20), Vector(10,20), "G", [255,255,255]),
                        'GTextBox': ColourGTextBox(Vector(size.x/3+10,size.x-20), Vector(size.x/3-10,20), self, data),
                        'lblB':widgets.Label(Vector(size.x/3*2,size.x-20), Vector(10,20), "B", [255,255,255]),
                        'BTextBox': ColourBTextBox(Vector(size.x/3*2+10,size.x-20), Vector(size.x/3-10,20), self, data),
                        'CloseButton': CloseButton(Vector(0,size.x), Vector(size.x,20), self, data)}
        self.order = ['colourWheel', 'RTextBox', 'GTextBox', 'BTextBox', 'lblR', 'lblG', 'lblB', 'CloseButton']
        self.visible = False
    def changelimb(self):
        for limb in ['colourWheel', 'RTextBox', 'GTextBox', 'BTextBox']:
            self.widgets[limb].changelimb()
    def resize(self, pos, size):
        self.pos = pos
        if size[0] < 1: size[0] = 1
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.setup()
        self.organise()
        self.draw()
    def menuaction(self, selected):
        if selected == "close":
            self.visible = False
    def draw(self):
        self.drawwidgets()
        #self.image.blit(self.mousemask, (0,0))
        
        self.redraw = True
    def drawbase(self):
        self.image.fill((0,0,0))
    def organise(self):
        self.widgets['Preview'].pos.y = self.size.y - self.widgets['Preview'].size.y - 10

class colourWheel(widgets.BaseWidget):
    def setup(self):
        self.colourwheelsetup()
    def colourwheelsetup(self):
        self.hsvcolour = [0,0,1]
        self.vwidth = 20
        self.grabvalue = False
        #print (self.size.x-self.vwidth, self.size.x-self.vwidth)
        self.wheel = pygame.Surface((self.size.x-self.vwidth, self.size.x-self.vwidth)).convert_alpha()
        self.wheel.fill((0,0,0,0))
        self.midpt = Vector(self.wheel.get_size()) / 2
        wheelpa = pygame.PixelArray(self.wheel)
        for y in range(self.wheel.get_height()):
            for x in range(self.wheel.get_width()):
                if distance(self.midpt, (x,y))/(self.wheel.get_width()/2) < 1: wheelpa[x][y] = hsv_to_rgb(direction(self.midpt, (x,y))/360, distance(self.midpt, (x,y))/(self.wheel.get_width()/2), 255)
        del wheelpa
        #for y in range(self.wheel.get_height()):
        #    for x in range(self.wheel.get_width()):
        #        if distance(self.midpt, (x,y))/(self.wheel.get_width()/2) < 1: self.wheel.set_at((x,y), hsv_to_rgb(direction(self.midpt, (x,y))/360, distance(self.midpt, (x,y))/(self.wheel.get_width()/2), 255))
        self.value = pygame.Surface((self.vwidth, self.size.y))
        self.drawvalue()
        self.draw()
    def drawvalue(self):
        for y in range(self.size.y):
            try:
                pygame.draw.line(self.value, hsv_to_rgb(self.hsvcolour[0], self.hsvcolour[1], y/float(self.size.y)*255), (0,y),(self.vwidth,y),1)
            except:
                pass
    def mousemove(self):
        if self.selected:
            if self.mousebut[0]:
                if self.grabvalue:
                    self.hsvcolour[2] = max(min(float(self.mousepos.y - self.pos.y) / self.size.y, 1), 0)
                else:
                    self.hsvcolour[0] = direction(self.midpt, self.mousepos-self.pos)/360
                    self.hsvcolour[1] = distance(self.midpt, self.mousepos-self.pos)/(self.wheel.get_width()/2)
                    self.hsvcolour[0] = min(self.hsvcolour[0], 1)
                    self.hsvcolour[1] = min(self.hsvcolour[1], 1)
                    self.drawvalue()
                self.changed()
                self.draw()
    def lclick(self):
        self.grabvalue = self.mousepos.x-self.pos.x > self.size.x - self.vwidth
        self.mousemove()
    def setrgb(self, rgb):
        hsv = rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
        self.hsvcolour = [hsv[0], hsv[1], hsv[2]]
        self.drawvalue()
        self.draw()
    def rgb(self):
        return hsv_to_rgb(self.hsvcolour[0], self.hsvcolour[1], self.hsvcolour[2]*255)
    def changed(self):
        pass
    def draw(self):
#        self.image.fill((0,0,0))
        #print col, self.hsvcolour
        self.image.fill(hsv_to_rgb(self.hsvcolour[0], self.hsvcolour[1], self.hsvcolour[2]*255))
        self.image.blit(self.wheel, (0,0))
        self.image.blit(self.value, (self.size.x-self.vwidth,0))
        #hsvcolour = rgb_to_hsv(float(self.colour[0])/255, float(self.colour[1])/255, float(self.colour[2])/255)
        #print self.colour, hsvcolour, hsvcolour[0]*360, hsvcolour[1]*self.size.y
        #print self.hsvcolour
        col = intlist(hsv_to_rgb(self.hsvcolour[0], self.hsvcolour[1], 255))
        pygame.draw.circle(self.image, (255-col[0], 255-col[1], 255-col[2]), Vector(intlist(polar2cart(self.hsvcolour[0]*360, self.hsvcolour[1]*(self.wheel.get_width()/2)))) + self.midpt, 3, 2)
        pygame.draw.circle(self.image, (255,255,255), intlist((self.size.x-self.vwidth/2, self.hsvcolour[2]*self.size.y)), 3, 0)
        pygame.draw.circle(self.image, (0,0,0), intlist((self.size.x-self.vwidth/2, self.hsvcolour[2]*self.size.y)), 4, 1)
        
        self.redraw = True

class ChooserColourWheel(colourWheel):
    def changelimb(self):
        if not self.mousebut[0] or not self.selected: self.setrgb(self.data['editing'][0]['colour'].value)
        self.draw()
    def changed(self):
        for limb in self.data['editing']:
            limb['colour'].value = self.rgb()
#            updateUnKeyed(limb)
        self.container.changelimb()
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()

class ColourRTextBox(widgets.NumberScrollBox):
    def setup(self):
        self.textboxsetup()
        self.comment = "The red value of the RGB colour value"
    def changelimb(self):
        if not self.editing:
            self.textboxsetup(str(self.data['editing'][0]['colour'].value[0]))
            self.draw()
    def edited(self):
        for limb in self.data['editing']:
            try:
                if float(self.text) < 0: self.text = "0"
                if float(self.text) > 255: self.text = "255"
                limb['colour'].value = [min(abs(float(self.text)),255), limb['colour'].value[1], limb['colour'].value[2]]
                #updateUnKeyed(limb)
            except:
                pass
        self.container.widgets['colourWheel'].changelimb()
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()

class ColourGTextBox(widgets.NumberScrollBox):
    def setup(self):
        self.textboxsetup()
        self.comment = "The green value of the RGB colour value"
    def changelimb(self):
        if not self.editing:
            self.textboxsetup(str(self.data['editing'][0]['colour'].value[1]))
            self.draw()
    def edited(self):
        for limb in self.data['editing']:
            try:
                if float(self.text) < 0: self.text = "0"
                if float(self.text) > 255: self.text = "255"
                limb['colour'].value = [limb['colour'].value[0], min(abs(float(self.text)),255), limb['colour'].value[2]]
                #updateUnKeyed(limb)
            except:
                pass
        self.container.widgets['colourWheel'].changelimb()
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()

class ColourBTextBox(widgets.NumberScrollBox):
    def setup(self):
        self.textboxsetup()
        self.comment = "The blue value of the RGB colour value"
    def changelimb(self):
        if not self.editing:
            self.textboxsetup(str(self.data['editing'][0]['colour'].value[2]))
            self.draw()
    def edited(self):
        for limb in self.data['editing']:
            try:
                if float(self.text) < 0: self.text = "0"
                if float(self.text) > 255: self.text = "255"
                limb['colour'].value = [limb['colour'].value[0], limb['colour'].value[1], min(abs(float(self.text)),255)]
                #updateUnKeyed(limb) 
            except:
                pass
        self.container.widgets['colourWheel'].changelimb()
        self.container.container.widgets['Preview'].draw()
        self.container.container.container.widgets['StickEditor'].draw()

class CloseButton(widgets.Button):
    def setup(self):
        self.buttonsetup("Close")
        self.comment = "Closes the colour picker"
    def lrelease(self):
        if self.hover and self.selected:
            self.container.visible = False
        self.draw()

class ValEditTextBox(widgets.NumberScrollBox):
    def __init__(self, limbval, pos, size, container = None, data = None, comment = "", limits = (-1e308, 1e308)):
        self.limbval = limbval
        self.initwidget(pos, size, container, data)
        self.comment = comment
        self.limits = limits
    def changelimb(self):
        if not self.editing:
            self.textboxsetup(str(self.data['editing'][0][self.limbval].value))
            self.draw()
    def edited(self):
        for limb in self.data['editing']:
            try:
                if float(self.text) > self.limits[0] and float(self.text) < self.limits[1]: 
                    limb[self.limbval].value = float(self.text)
            except:
                pass
        self.container.widgets['Preview'].draw()
        self.container.container.widgets['StickEditor'].draw()
    def scrolled(self, offset):
        for limb in self.data['editing']:
            try:
                limb[self.limbval].value += offset
            except:
                pass
        self.container.widgets['Preview'].draw()
        self.container.container.widgets['StickEditor'].draw()

class CloseShapeEditorButton(widgets.Button):
    def setup(self):
        self.buttonsetup("")
        self.image = pygame.Surface(self.size).convert_alpha()
        self.texbutup = self.container.window.resources['xbuttonup']
        self.texbutdown = self.container.window.resources['xbuttondown']
        self.comment = "Closes the limb shape editor"
    def draw(self):
        self.image.fill((0,0,0,0))
        self.drawbutton()
        
        self.redraw = True
        self.container.window.fullredraw = True
    def lrelease(self):
        if self.hover and self.selected:
            self.container.visible = False
            self.container.container.organise()
        self.draw()