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

import pygame, sys, pickle, zlib, defs
from copy import deepcopy

#Key: [frame, value]
class KeyFrame:
    def __init__(self, keys, keyed = False, interpol="linear"):
        self.interpol = interpol
        if keyed:
            self.keys = keys
            self.value = keys[0]
        else:
            self.keys = []
            self.value = keys
        self.frame = 1
        
    def __getitem__(self, *args):
        if len(args) > 1: raise RuntimeError
        return self.keys[args[0]]
    
    def insertkey(self, key=None):
        if key == None: key = [self.frame, self.value]
        self.removeframe(key[0])
        self.keys.append(key)
        self.clean()
        self.setframe(self.frame)
    
    def setframe(self, frame):
        if len(self.keys) == 0:
            val = self.value
        elif self.interpol == "const":
            val =  defs.interpolateConst(frame, self.keys)
        else:
            val = defs.interpolate(frame, self.keys, self.interpol)
        self.value = val
        self.frame = frame
        return val
    def __str__(self):
        keyString = "<keyframe interpol=\"" + self.interpol + "\" value=\"" + str(self.value) + "\">\n"
        for key in self.keys:
            keyString += "  <key frame=\"" + str(key[0]) +"\" value=\"" + str(key[1]) + "\"/>\n"
        keyString += "</keyframe>"
        return keyString
            
    def clean(self):
        if len(self.keys) > 1:
            self.sort()
            self.removedoubles()
    def sort(self):
        if len(self.keys) > 1:
            self.keys.sort()
    def removeframe(self, frame):
            self.keys = [self.keys[i] for i in range(len(self.keys)) if not self.keys[i][0] == frame]
    def removedoubles(self):
        if len(self.keys) > 1:
            self.keys = [self.keys[i] for i in range(len(self.keys)) if i == len(self.keys)-1 or not self.keys[i][0] == self.keys[i+1][0]]
            #self.keys = [self.keys[i] for i in range(len(self.keys)) if i == len(self.keys)-1 or not self.keys[i][0] == self.keys[i-1][0]]

class Vector:
    def __init__(self, x, y=None):
        if y == None:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y
    
    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"
    
    def __getitem__(self, *args):
        if args[0] == 0: #args.count(0) > 0:
            return self.x
        elif args[0] == 1: #args.count(1) > 0:
            return self.y
        else:
            raise IndexError
        
    def __setitem__(self, index, item):
        if index == 0:
            self.x = item
        elif index == 1:
            self.y = item
            
    def __add__(self, other):
        return Vector(self.x + other[0], self.y + other[1])
    
    def __sub__(self, other):
        return Vector(self.x - other[0], self.y - other[1])
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __div__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
        
    def __len__(self):
        return 2

#class Texture:
#    def __init__(self, overwritevals = dict()):
#        self.values = dict()
#        self.comments = dict()
#        self.defaultsetup()
#        defs.concatDict(self.values, overwritevals)
#        self.setframe(1)
#        self.oldinit()
#    def defaultsetup(self):
#        pass
#    def draw(self, Surface, point1, point2, limb, SizeRatio = 1):
#        pass
#    def insertKey(self):
#        for val in self.values:
#            val.insertkey([self.frame, key.value])
#    def setframe(self, frame):
#        self.frame = frame
#        for val in self.values.values():
#            val.setframe(self.frame)
#        return self
#    def oldinit(self):
#        pass
#    def valuekeys(self):
#        return self.values
#    def __str__(self):
#        return "Texture()"
    
class Texture:
    def __init__(self, overwritevals = dict(), shape=None):
        if not shape == None: overwritevals['shape'] = KeyFrame(shape, False, "const")
        self.values = dict(shape=KeyFrame("line", False, "const"), # "line", "circle", "text", "image"
                           caps=KeyFrame(True, False, "const"),
                           fill=KeyFrame(False, False, "const"),
                           text=KeyFrame("test",False,"const"),
                           flip=KeyFrame(True,False,"const"),
                           file=KeyFrame("splogoicon.png",False,"const"))
        self.comments = dict(caps="Adds round caps to the end of the line",
                             fill="Fills the circle with the limb colour",
                             text="The text to be displayed as the limb",
                             flip="Flips the shape so it isn't upside down when rotated",
                             file="Name of image file to be displayed")
        self.defaultsetup()
        defs.concatDict(self.values, overwritevals)
        self.setframe(1)
        self.oldinit()
    def defaultsetup(self):
        pass
    def draw(self, Surface, point1, point2, limb, SizeRatio = 1):
        if self.values['shape'].value == "line":
            defs.drawline(Surface, limb['colour'].value, point1, point2, limb['width'].value * SizeRatio, self.values['caps'].value)
            
        elif self.values['shape'].value == "circle":
            if limb['cartesian'].value:
                dist = defs.distance(point1, point2)
            else:
                dist = limb['dist'].value * SizeRatio
            defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], dist / 2, limb['width'].value * SizeRatio)
            if self.values['fill'].value: defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], dist / 2, 0)
            
        elif self.values['shape'].value == "text":
            font = pygame.font.Font(pygame.font.get_default_font(), int(limb['width'].value * SizeRatio))
            text = font.render(self.values['text'].value, True, limb['colour'].value)
            if self.values['flip'].value: text = pygame.transform.flip(text, True, True)
            text = pygame.transform.rotate(text, 90-defs.direction(point1, point2))
            Surface.blit(text, Vector(point1+point2)/2-Vector(text.get_size())/2)
            
        elif self.values['shape'].value == "image":
            try:
                image = pygame.image.load(self.values['file'].value)
                if self.values['flip'].value: image = pygame.transform.flip(image, True, True)
                #image = pygame.transform.rotate(image, 180 - defs.direction(point1, point2))
                image = pygame.transform.smoothscale(image, (image.get_width()*SizeRatio, image.get_height()*SizeRatio))
                image = pygame.transform.rotate(image, 180 - defs.direction(point1, point2))
                Surface.blit(image, Vector(point1+point2)/2-Vector(image.get_size())/2)
            except:
                pass
            
    def insertkey(self):
        #print self.values
        for val in self.values.values():
            #print val
            val.insertkey()
    def setframe(self, frame):
        self.frame = frame
        for val in self.values.values():
            val.setframe(self.frame)
        return self
    def oldinit(self):
        pass
    def valuekeys(self):
        return self.values
    def __str__(self):
        vals = ""
        for val in self.values.items():
            vals += "<" + val[0] + ">\n" + str(val[1]) + "\n</" + val[0] + ">\n"
        return "<texture>\n"+vals+"</texture>"

class Resource:
    def __init__(self):
        self.rec = {}
        self.setup()
    def addrec(self, name, rec):
        self.rec[name] = rec
        self.update()
    def setup(self):
        pass
    def update(self):
        pass
    def __getitem__(self, *args):
        return self.rec[args[0]]

#class TexLine(Texture):
#    def __init__(self, caps = KeyFrame(True, False, "const")):
#        self.caps = caps
#        self.setframe(1)
#    def draw(self, Surface, point1, point2, limb, SizeRatio = 1):
#        defs.drawline(Surface, limb['colour'].value, point1, point2, limb['width'].value * SizeRatio, self.caps.value)
#    def insertKey(self):
#        self.caps.insertkey([self.frame, self.caps.value])
#    def setframe(self, frame):
#        self.frame = frame
#        self.caps.setframe(frame)
#        return self
#    def valuekeys(self):
#        return {'caps':self.caps}
#    def __str__(self):
#        return "TexLine(caps=" + str(self.caps) + ")"

#class TexLine(Texture):
#    def defaultsetup(self):
#        self.values['caps'] = KeyFrame(True, False, "const")
#        self.comments['caps'] = "Adds round caps to the end of the line"
#    def draw(self, Surface, point1, point2, limb, SizeRatio = 1):
#        defs.drawline(Surface, limb['colour'].value, point1, point2, limb['width'].value * SizeRatio, self.values['caps'].value)
#    def __str__(self):
#        return "TexLine(caps="+ str(self.values['caps']) +")"
#    
#    def oldinit(self):
#        self.caps = self.values['caps']
#
#class TexCircle(Texture):
#    def defaultsetup(self):
#        self.values['fill'] = KeyFrame(False, False, "const")
#    def draw(self, Surface, point1, point2, limb, SizeRatio = 1):
#        if limb['cartesian'].value:
#            dist = defs.distance(point1, point2)
#            #defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], defs.distance(point1, point2) / 2, limb['width'].value * SizeRatio)
#            #if self.fill.value: defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], defs.distance(point1, point2) / 2, 0)
#        else:
#            dist = limb['dist'].value * SizeRatio
#            #defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], limb['dist'].value * SizeRatio / 2, limb['width'].value * SizeRatio)
#        defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], dist / 2, limb['width'].value * SizeRatio)
#        if self.values['fill'].value: defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], dist / 2, 0)
#    def __str__(self):
#        return "TexCircle(fill=" + str(self.values['fill']) + ")"
#    
#    def oldinit(self):
#        self.fill = self.values['fill']
#
#class TexText(Texture):
#    def defaultsetup(self):
#        self.values['text'] = KeyFrame("text",False,"const")
#        self.values['flip'] = KeyFrame(True,False,"const")
#    def draw(self, Surface, point1, point2, limb, SizeRatio = 1):
#        font = pygame.font.Font(pygame.font.get_default_font(), limb['width'].value * SizeRatio)
#        text = font.render(self.values['text'].value, True, limb['colour'].value)
#        if self.values['flip'].value: text = pygame.transform.flip(text, True, True)
#        text = pygame.transform.rotate(text, 90-defs.direction(point1, point2))
#        Surface.blit(text, Vector(point1+point2)/2-Vector(text.get_size())/2)
#    def __str__(self):
#        return "TexText(text='" + str(self.values['caps']) + "', flip=" + str(self.values['flip']) + ")"
#    
#    def oldinit(self):
#        self.text = self.values['text']
#        self.flip = self.values['flip']
#
##class TexCircle(Texture):
##    def __init__(self, fill=KeyFrame(False, False, "const")):
##        self.fill = fill
##        #self.values = {'fill':fill}
##        self.setframe(1)
##    def draw(self, Surface, point1, point2, limb, SizeRatio = 1):
##        if limb['cartesian'].value:
##            defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], defs.distance(point1, point2) / 2, limb['width'].value * SizeRatio)
##            if self.fill.value: defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], defs.distance(point1, point2) / 2, 0)
##        else:
##            defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], limb['dist'].value * SizeRatio / 2, limb['width'].value * SizeRatio)
##            if self.fill.value: defs.drawcircle(Surface, limb['colour'].value, [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2], limb['dist'].value * SizeRatio / 2, 0)
##    def insertKey(self):
##        self.fill.insertkey([self.frame, self.drawfill])
##    def setframe(self, frame):
##        self.frame = frame
##        self.fill.setframe(frame)
##        return self
##    def valuekeys(self):
##        return {'fill':self.fill}
##    def __str__(self):
##        return "TexCircle(fill=" + str(self.fill) + ")"
#
##class TexText(Texture):
##    def __init__(self, text=KeyFrame("text",False,"const"), flip=KeyFrame(True,False,"const")):
##        self.text = text
##        self.flip = flip
##        self.setframe(1)
##    def draw(self, Surface, point1, point2, limb, SizeRatio = 1):
##        font = pygame.font.Font(pygame.font.get_default_font(), limb['width'].value * SizeRatio)
##        text = font.render(self.text.value, True, limb['colour'].value)
##        if self.flip.value: text = pygame.transform.flip(text, True, True)
##        text = pygame.transform.rotate(text, 90-defs.direction(point1, point2))
##        Surface.blit(text, Vector(point1+point2)/2-Vector(text.get_size())/2)
##    def insertKey(self):
##        defs.insertKey(self.fill, [self.frame, self.drawfill], interpol="const")
##    def setframe(self, frame):
##        self.drame = frame
##        self.text.setframe(frame)
##        self.flip.setframe(frame)
##        return self
##    def valuekeys(self):
##        return {'text':self.text, 'flip':self.flip}
##    def __str__(self):
##        return "TexText(text='" + str(self.caps) + "', flip=" + str(self.flip) + ")"
#
#class TexImage(Texture):
#    def __init__(self, file=KeyFrame("splogoicon.png",False,"const"), flip=KeyFrame(True,False,"const")):
#        self.file = file
#        self.flip = flip
#        self.setframe(1)
#    def draw(self, Surface, point1, point2, limb, SizeRatio = 1):
#        try:
#            image = pygame.image.load(self.file.value)
#            if self.flip.value: image = pygame.transform.flip(image, True, True)
#            #image = pygame.transform.rotate(image, 180 - defs.direction(point1, point2))
#            image = pygame.transform.smoothscale(image, (image.get_width()*SizeRatio, image.get_height()*SizeRatio))
#            image = pygame.transform.rotate(image, 180 - defs.direction(point1, point2))
#            Surface.blit(image, Vector(point1+point2)/2-Vector(image.get_size())/2)
#        except:
#            pass
#    def setframe(self, frame):
#        self.frame = frame
#        self.file.setframe(frame)
#        self.flip.setframe(frame)
#        return self
#    def valuekeys(self):
#        return {'file':self.file, 'flip':self.flip}
#    def __str__(self):
#        return "TexImage(file='" + str(self.file) + "', flip=" + str(self.flip) + ")"
