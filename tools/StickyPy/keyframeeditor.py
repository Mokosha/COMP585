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

import pygame, widgets
from objs import *
from defs import *

W_SZ_Y = 100

class KeyFrameWidget(widgets.WidgetContainer):
    def __init__(self, pos, size, container, mainwindow, data):
        self.setupcontainer(pos, size, mainwindow, container, data)
        self.widgets = {'KeyFrameEditor':KeyFrameEditor(Vector(0,0), size, self, data),
                        'CloseKeyEditorButton':CloseKeyEditorButton(Vector(0,0), Vector(30,30), self, data)}
        self.order = ['KeyFrameEditor', 'CloseKeyEditorButton']
        self.visible = False
        self.organise()

    def resize(self, pos, size):
        self.pos = pos
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.setup()
        self.organise()
        self.draw()

    def changekeys(self, keys):
        self.widgets['KeyFrameEditor'].changekeys(keys)

    def updatezoom(self, frame_range):
        self.widgets['KeyFrameEditor'].updatezoom(frame_range)

    def close(self):
        self.visible = False
        self.window.fullredraw = True
        self.container.organise()

    def show(self):
        self.visible = True
        self.window.fullredraw = True
        self.container.organise()

    def draw(self):
        self.drawwidgets()
        self.redraw = True

    def organise(self):
        self.widgets['KeyFrameEditor'].resize(Vector(30,0), self.size - Vector(30,0))

class KeyFrameEditor(widgets.BaseWidget):

    def setup(self):
        self.editing = []
        self.texkeyon = self.container.window.resources['key']
        self.texkeyoff = self.container.window.resources['keyoff']
        self.drag = None
        self.fontsize = 16
        self.select = [False,None, "box"]
        self.zoom = 4
        self.maxzoom = 48.0
        self.minzoom = 0.01
        self.pan = 0
        self.visible = True
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontsize)

        self.keys = []
        self.textwidth = 0
        self.range = [1, 2]

    def resize(self, pos, size):
        self.pos = pos
        self.size = size
        self.image = pygame.Surface(self.size)
        if self.container.visible: self.draw()

    def updatezoom(self, frame_range=None):

        if frame_range == None:
            frame_range = self.range

        width = self.size.x - self.textwidth - 2*self.texkeyoff.get_size()[0]
        self.minzoom = float(width) / (frame_range[1] - frame_range[0])

        self.zoom = self.minzoom
        self.range = frame_range

    def changekeys(self, keys):
        self.keys = keys
        maxwidth = 0

        self.validKeys = []
        if not self.keys == []:
            for item in self.keys[0].keys():
                twidth = self.font.render(item, True, (0,0,0)).get_width()
                if twidth > maxwidth: maxwidth = twidth

            for i in range(len(self.keys[0])):
                kf = self.keys[0].values()[i]
                if isinstance(kf, KeyFrame) and kf.keyed:
                    self.validKeys.append(i)

        self.textwidth = maxwidth

        self.updatezoom()
        if self.visible:
            self.draw()
            self.container.organise()

    def getCollide(self, map):
        collisions = []
        for kn in range(len(self.validKeys)):

            i = self.validKeys[kn]
            for key in self.keys[0].values()[i].keys:
                point = Vector(self.texkeyoff.get_size())/2 + self.getkeypos(key, kn)
                point = Vector(int(point.x), int(point.y))
                if point[0] > 0 and point[0] < self.size.x and map.get_at(point)[0] > 150:
                    collisions.append(key)

        return collisions

    def getdrag(self):
        for kn in range(len(self.validKeys)):
            i = self.validKeys[kn]
            for key in self.keys[0][self.keys[0].keys()[i]].keys:
                if pygame.Rect(self.getkeypos(key, kn), self.texkeyon.get_size()).collidepoint(self.mousepos-self.pos):
                    return key

    def mwheelup(self):
        if self.hover:
            self.zoom = min(self.zoom * 1.2, self.maxzoom)
            self.draw()

    def mwheeldown(self):
        if self.hover:
            self.zoom = max(self.zoom / 1.2, self.minzoom)
            self.draw()

    def lclick(self):
        if not self.hover or not self.selected:
            return

        self.drag = self.getdrag()
        if self.drag != None:
            if self.keyboard[pygame.K_RSHIFT] or self.keyboard[pygame.K_LSHIFT]:
                contains = False
                for key in self.editing:

                    if key is self.drag:
                        contains = True
                        if len(self.editing) > 1: 
                            self.editing = [k for k in self.editing if not k is key]
                        break

                if not contains: 
                    self.editing += [self.drag]
            else:
                contains = False
                for key in self.editing:
                    if key is self.drag:
                        contains = True
                        break

                if not contains: 
                    self.editing = [self.drag]

        elif self.keyboard[pygame.K_LCTRL] or self.keyboard[pygame.K_RCTRL]:
            self.select = [True, [self.mousepos - self.pos], "lasso"]
        else:
            self.select = [True, self.mousepos, "box"]
        self.dragging = True
        self.dragpos = deepcopy(self.editing)
        self.dragmouse = self.mousepos
        self.selected = self.drag
        self.draw()

    def lrelease(self):
        if self.container.visible:
            self.drag = None
            for currkey in self.keys:
                for key in currkey.values():
                    if isinstance(key, KeyFrame): key.clean()
            self.draw()
                    
        if self.select[0]:
            map = pygame.Surface(self.image.get_size())
            map.fill((0,0,0))
            if self.select[2] == "box":
                pygame.draw.rect(map, (255,255,255), pygame.Rect(self.select[1] - self.pos, self.mousepos - self.select[1]))
            elif self.select[2] == "lasso" and len(self.select[1]) > 2:
                pygame.draw.polygon(map, (255,255,255), self.select[1])
                
            if self.keyboard[pygame.K_LSHIFT] or self.keyboard[pygame.K_RSHIFT]:
                self.editing += self.getCollide(map)
            else:
                self.editing = self.getCollide(map)
            self.select[0] = False
            self.draw()

    def mclick(self):
        pass

    def rrelease(self):
        if self.hover and self.selected:
            self.selectedkey = self.getdrag()

            menuoptions = []
            if not self.selectedkey == None:
                menuoptions.append(("Delete keyframe", "deletekey"))
                menuoptions.append(("Go to frame", "gotoframe"))
                menuoptions.append(("Set linear interpolation", "linear"))
                menuoptions.append(("Set smoothstep interpolation", "smoothstep"))
            else:
                menuoptions.append(("Insert Keyframe", "insertkey"))
                menuoptions.append(("Close keyframe editor", "closeeditor"))

            self.menumousepos = self.mousepos - self.pos
            self.container.window.menu.showmenu(menuoptions, self.container.window.mousepos, self, 15)

    def mousemove(self):
        if self.select[0] and self.select[2] == "lasso":
            self.select[1] += [self.mousepos - self.pos]
        if self.mousebut[1] and self.selected:
            self.pan += self.mousepos.x - self.oldmousepos.x
        if not self.drag == None:
            for i in range(len(self.editing)):
                self.editing[i][0] = self.dragpos[i][0] + (self.mousepos.x - self.dragmouse.x) / self.zoom
            for currkey in self.keys:
                for key in currkey.values():
                    if isinstance(key, KeyFrame): key.sort()
            self.container.container.changeframe(self.data['frame'])
        if self.visible and self.hover:
            self.draw()

    def always(self):
        if self.data['playing'] and self.visible:
            self.draw()

    def menuaction(self, selected):
        if selected == "deletekey":
            for key in self.editing:
                for currkey in self.keys:
                    for keyfr in currkey.values():
                        if isinstance(keyfr, KeyFrame):
                            keyfr.keys = [k for k in keyfr.keys if not k is key]
                            keyfr.setframe(self.data['frame'])
            self.draw()

        elif selected == "gotoframe":
            self.data['frame'] = self.selectedkey[0]
            self.container.changeframe(self.data['frame'])
            self.draw()

        elif selected == "insertkey":
            frame, attrib = self.getposkey(self.menumousepos)

            for limb in self.keys:
                k = limb.keys()[self.validKeys[attrib]]

                oldframe = limb[k].frame
                limb[k].setframe(frame)
                limb[k].insertkey()
                limb[k].setframe(oldframe)
            
            self.draw()

        elif selected == "closeeditor":
            self.container.close()
        elif selected == "linear" or selected == "smoothstep":
            for key in self.editing:
                for currkey in self.keys:
                    for keyfr in currkey.values():
                        if isinstance(keyfr, KeyFrame):
                            keyfr.interpol = selected
            self.draw()

    def getposkey(self, pos):
        dy = self.size[1]/len(self.validKeys)
        dx = self.zoom

        frame = int((pos[0] - self.textwidth) / dx + 0.5) + 1
        attrib = int(pos[1] / dy)

        return frame, attrib

    def getkeypos(self, key, row):
        dy = len(self.validKeys)
        return ((key[0]-1)*self.zoom+self.textwidth+self.pan - self.texkeyoff.get_width()/2, self.size[1]/dy*row+(self.size[1]/dy)/2 - self.texkeyon.get_height()/2)

    def draw(self):

        if not self.container.visible: 
            return

        self.image.fill((100,100,100))

        line_x = (self.data['frame'] - 1)*self.zoom+self.textwidth+self.pan
        pygame.draw.line(self.image, (0,0,0), (line_x, 0), (line_x, self.size[1]), 3)

        for kn in range(len(self.validKeys)):
            i = self.validKeys[kn]
            fontrender = self.font.render(self.keys[0].keys()[i], True, (0,0,0))
            
            dy = len(self.validKeys)
            self.image.blit(fontrender, (0,self.size[1]/dy*kn+(self.size[1]/dy)/2 - fontrender.get_height()/2))
            pygame.draw.line(self.image, (0,0,0), (self.textwidth,self.size[1]/dy*kn+(self.size[1]/dy)/2), (self.size[0],self.size[1]/dy*kn+(self.size[1]/dy)/2))
                
        for kn in range(len(self.validKeys)):
            i = self.validKeys[kn]
            for key in self.keys[0].values()[i].keys:
                selected = False
                for editkey in self.editing:
                    if key is editkey: selected = True
                if selected:
                    self.image.blit(self.texkeyon, self.getkeypos(key, kn))
                else:
                    self.image.blit(self.texkeyoff, self.getkeypos(key, kn))

        if self.selected and self.select[0]:
            if self.select[2] == "box":
                pygame.draw.rect(self.image, (0,0,0), pygame.Rect(self.select[1] - self.pos, self.mousepos - self.select[1]), 2)
            elif self.select[2] == "lasso" and len(self.select[1]) > 2:
                pygame.draw.polygon(self.image, (0,0,0), self.select[1], 2)
        
        self.redraw = True

class CloseKeyEditorButton(widgets.Button):
    def setup(self):
        self.buttonsetup("")
        self.image = pygame.Surface(self.size).convert_alpha()
        self.texbutup = self.container.window.resources['xbuttonup']
        self.texbutdown = self.container.window.resources['xbuttondown']
        self.comment = "Closes the key frame editor"
    def draw(self):
        self.image.fill((0,0,0,0))
        self.drawbutton()
        
        self.redraw = True
    def lrelease(self):
        if self.hover and self.selected:
            self.container.close()
            
        self.draw()
