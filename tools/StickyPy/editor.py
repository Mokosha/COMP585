import pygame, thread, widgets
from objs import *
from defs import *

class StickEditor(widgets.BaseWidget):
    def setup(self):
        self.viewdrag = False
        self.image.fill((255,255,255))
        self.fill = self.image.copy()
        self.dragging = False
        self.cameradrag = [0] #0:Off, 1:Camera Drag, 2:Camera Resize
        self.select = [False,None, "box"]
        self.drawonion()
    def resize(self, pos, size):
        self.pos = pos
        if size[0] < 1: size[0] = 1
        if size[1] < 1: size[1] = 1
        self.size = size
        self.image = pygame.Surface(self.size)
        self.draw()
    def mwheelup(self):
        if self.hover:
            self.zoom(1.2, self.mousepos)
            self.drawonion()
            self.draw()

    def mwheeldown(self):
        if self.hover:
            self.zoom(1/1.2, self.mousepos)

    def zoom(self, z, o): # z=Zoom amount, o=Origin
        s = self.size
        h = s / 2
        m = self.data['zoom']
        p = self.data['panning']
        #TODO: NEEDS REWORK!
        self.data['panning'] = p - ((s*z) - s) / m / z / 2
        self.data['zoom'] *= z
        self.drawonion()
        self.draw()

    def lclick(self):
        if self.hover and self.selected and not self.data['playing']:
            tedit = getGrab(self.mousepos, self.data['scene'], self.pos + self.panning(), self.data['zoom'])
            if not tedit == None:
                if self.container.widgets['ExtrudeCheckBox'].checked:
                    extruded = dict(deepcopy(tedit), children=[], pos=KeyFrame(Vector(0,0)), dist=KeyFrame(0))
                    tedit['children'].append(extruded)
                    tedit = extruded
                if not tedit['static'].value or self.container.widgets['ExtrudeCheckBox'].checked:
                    self.data['drag'] = tedit
                    self.dragging = True
                    
                if self.keyboard[pygame.K_RSHIFT] or self.keyboard[pygame.K_LSHIFT]:
                    tedit = getGrab(self.mousepos, self.data['scene'], self.pos + self.panning(), self.data['zoom'])
                    contains = False
                    for limb in self.data['editing']:
                        if limb is tedit:
                            contains = True
                            if len(self.data['editing']) > 1:
                                self.data['editing'] = [l for l in self.data['editing'] if not l is limb]
                                self.container.widgets['KeyFrameEditor'].changekeys(self.data['editing'])
                            break
                    if not contains: self.data['editing'] += [tedit]
                else:
                    contains = False
                    for limb in self.data['editing']:
                        if limb is tedit:
                            contains = True
                            break
                    if not contains: self.data['editing'] = [getGrab(self.mousepos, self.data['scene'], self.pos + self.panning(), self.data['zoom'])]
                self.container.widgets['KeyFrameEditor'].changekeys(self.data['editing'])
                self.draw()
            elif self.cameraresizeover(self.mousepos-self.pos):
                self.cameradrag = [2, deepcopy(self.mousepos), deepcopy(self.data['camera']['zoom'].value)]
            elif self.cameraover(10, self.mousepos-self.pos):
                self.cameradrag = [1, deepcopy(self.mousepos), deepcopy(self.data['camera']['pos'].value)]
            elif self.keyboard[pygame.K_LCTRL] or self.keyboard[pygame.K_RCTRL]:
                self.select = [True, [self.mousepos - self.pos], "lasso"]
            else:
                self.select = [True, self.mousepos, "box"]
        if not self.data['editing'] == [] and self.selected: self.container.widgets['ShapeEditor'].changelimb()
    def lrelease(self):
        if self.select[0]:
            map = pygame.Surface(self.image.get_size())
            map.fill((0,0,0))
            if self.select[2] == "box":
                pygame.draw.rect(map, (255,255,255), pygame.Rect(self.select[1] - self.pos, self.mousepos - self.select[1]))
            elif self.select[2] == "lasso" and len(self.select[1]) > 2:
                pygame.draw.polygon(map, (255,255,255), self.select[1])
                
            if self.keyboard[pygame.K_LSHIFT] or self.keyboard[pygame.K_RSHIFT]:
                self.data['editing'] += getCollide(map, self.data['scene'], self.panning(), self.data['zoom'], 0)
            else:
                self.data['editing'] = getCollide(map, self.data['scene'], self.panning(), self.data['zoom'], 0)
            self.select[0] = False
        self.dragging = False
        self.cameradrag[0] = 0
        if not self.data['editing'] == [] and self.selected: self.container.widgets['ShapeEditor'].changelimb()
        if self.hover and self.selected:
            self.container.widgets['KeyFrameEditor'].changekeys(self.data['editing'])
            self.drawonion()
            self.draw()
    def mousemove(self):
        # If lasso mode is on
        if self.select[0] and self.select[2] == "lasso":
            self.select[1] += [self.mousepos - self.pos]
            if not self.data['playing']: self.draw()
        
        # If the camera is being dragged (1 means panning, 2 means zooming:
        if self.cameradrag[0] == 1:
            self.data['camera']['pos'].value = (Vector(self.cameradrag[2]) - self.cameradrag[1] + self.mousepos)  / self.data['zoom']
        elif self.cameradrag[0] == 2:
            self.data['camera']['zoom'].value = (self.mousepos.y - self.pos.y - self.data['camera']['pos'].value.y - self.panning().y) / float(self.data['camera']['size'].y) / self.data['zoom']
        
        if self.selected: # If the editor was the last widget to be clicked
            if self.mousebut[1] and not self.viewdrag: # Set to view panning mode when the middle mouse is clicked
                self.viewdrag = True
                self.viewdragorig = Vector(self.data['panning'])
                self.viewdragmouse = Vector(self.mousepos)

            elif self.mousebut[1] and self.viewdrag: # Pan the view
                self.data['panning'] = Vector(self.viewdragorig + (self.mousepos - self.viewdragmouse)/self.data['zoom'])

            else:
                self.viewdrag = False

            if not self.data['playing']: 
                self.draw()
        
        # If a vertex is being dragged, move it around
        if self.mousebut[0] and not self.data['drag'] == None and self.dragging:
            doGrab(self.mousepos, self.data['scene'], self.data['drag'], self.container.widgets['StretchCheckBox'].checked or self.container.widgets['ExtrudeCheckBox'].checked, self.pos + self.panning(), self.data['zoom'])
            if not self.data['playing']: self.draw()
        
        # Set the mouse over comment
        tover = getGrab(self.mousepos, self.data['scene'], self.pos + self.panning(), self.data['zoom'])
        if not tover == None:
            self.comment = ("Static, " if tover['static'].value else "") + ("Cartesian offset" if tover['cartesian'].value else "Polar offset")
        else:
            self.comment = ""

    def mrelease(self):
        self.drawonion()
        self.draw()

    def camerarect(self):
        return pygame.Rect(Vector(self.data['camera']['pos'].value) *self.data['zoom'] + self.panning(), self.data['camera']['size'] *self.data['camera']['zoom'].value *self.data['zoom'])

    def cameraover(self, thickness, pos):
        pygame.Rect(Vector(self.data['camera']['pos'].value) + self.panning()+[thickness/2,thickness/2], self.data['camera']['size'] *self.data['camera']['zoom'].value *self.data['zoom']-[thickness,thickness])
        outrect = self.camerarect()
        outrect.left -= thickness/2
        outrect.top -= thickness/2
        outrect.width += thickness
        outrect.height += thickness
        inrect = self.camerarect()
        inrect.left += thickness/2
        inrect.top += thickness/2
        inrect.width -= thickness
        inrect.height -= thickness
        return True if (not inrect.collidepoint(pos)
                    and outrect.collidepoint(pos)) else False

    def cameraresizeover(self, pos):
        camrect = self.camerarect()
        return True if pygame.Rect(Vector(camrect.left+camrect.width, camrect.top+camrect.height), Vector(10,10)).collidepoint(pos) else False

    def rrelease(self):
        tedit = getGrab(self.mousepos, self.data['scene'], self.pos + self.panning(), self.data['zoom'])
        if not tedit == None:
            newsel = True
            for limb in self.data['editing']:
                if limb is tedit: newsel = False
            if newsel: self.data['editing'] = [tedit]
            self.draw()
            self.container.window.menu.showmenu([("Insert keyframe", "insertkey"), ("Edit keyframes", "editkeys"), ("Edit limb shape", "editshape"), ("Delete", "delete"), ("Copy", "copy"), ("Paste", "paste"), ("Store Selection", "selstore"), ("Recall Selection", "selrecall")], self.mousepos, self, 20)
        elif self.cameraover(10, self.mousepos-self.pos):
            self.container.window.menu.showmenu([("Insert keyframe", "insertcamkey"), ("Edit keyframes", "editcamkeys"), ("Edit camera shape", "editcamshape")], self.mousepos, self, 20)

    def always(self):
        if self.data['playing']: self.draw()

    def menuaction(self, selection):
        if selection == "editkeys":
            self.container.widgets['KeyFrameEditor'].visible = True
            self.container.widgets['KeyFrameEditor'].changekeys(self.data['editing'])
        elif selection == "editshape":
            self.container.widgets['ShapeEditor'].visible = True
            self.container.widgets['ShapeEditor'].changelimb()
            self.container.organise()
        elif selection == "insertkey":
            for limb in self.data['editing']:
                for val in limb.values():
                    if isinstance(val, KeyFrame):
                        val.insertkey(deepcopy([self.data['frame'], val.value]))
                    if isinstance(val, Texture):
                        val.insertkey()
        elif selection == "delete":
            deleteVerts(self.data['editing'], self.data['scene'])
        elif selection == "copy":
            self.data['limbcopy'] = deepcopy(self.data['editing'][-1])
        elif selection == "paste":
            self.data['editing'][-1]['children'].append(deepcopy(self.data['limbcopy']))
        elif selection == "selstore":
            self.data['StoredSelection'] = self.data['editing']
        elif selection == "selrecall":
            self.data['editing'] = self.data['StoredSelection']
        
        elif selection == "insertcamkey":
            for val in self.data['camera'].values():
                if isinstance(val, KeyFrame):
                    val.insertkey(deepcopy([self.data['frame'], val.value]))

    def drawonion(self):
        if self.data['OnionSkinning']:
            onionscene = deepcopy(self.data['scene'])
            self.onion = pygame.Surface(self.image.get_size())
            self.onion.fill((255,255,255))
            fill = pygame.Surface(self.onion.get_size())
            fill.fill((255,255,255))
            for i in range(-2,0):

                changeFrame(onionscene, int(self.data['frame']+i))

                surface = fill.copy()
                drawStick(surface, onionscene, self.panning(), False, self.data['zoom'], self.data['editing']) #, 0, [0,0,0])

                surface.set_alpha(255/8*(i+5))
                self.onion.blit(surface, (0,0))

    def panning(self): 
        return self.data['panning'] * self.data['zoom']#+self.size/2

    def draw(self):
        #half = self.halfoffset()
        self.image.fill((255,255,255))
        if self.data['OnionSkinning'] and not self.mousebut[1]:
            self.image.blit(self.onion, (0,0))
        drawStick(self.image, self.data['scene'], self.panning(), False, self.data['zoom'], self.data['editing'])
        #thread.start_new_thread(drawStick, (self.image, self.data['scene'], self.panning(), False, self.data['zoom'], self.data['editing']))
        if not self.data['playing']: drawStick(self.image, self.data['scene'], self.panning(), True, self.data['zoom'], self.data['editing'])
        
        camrect = self.camerarect()
        pygame.draw.rect(self.image, (100,100,255), camrect, 1)
        pygame.draw.rect(self.image, (100,100,0), pygame.Rect(Vector(camrect.left+camrect.width, camrect.top+camrect.height), Vector(10,10)), 1)
        pygame.draw.rect(self.image, (100,100,0), pygame.Rect(Vector(camrect.left-10, camrect.top-10), Vector(10,10)), 1)
        
        if self.selected and self.select[0]:
            if self.select[2] == "box":
                pygame.draw.rect(self.image, (0,0,0), pygame.Rect(self.select[1] - self.pos, self.mousepos - self.select[1]), 2)
            elif self.select[2] == "lasso" and len(self.select[1]) > 2:
                pygame.draw.polygon(self.image, (0,0,0), self.select[1], 2)
        
        self.redraw = True
    def threaddraw(self):

        image = self.image

        if self.data['OnionSkinning'] and not self.mousebut[1]:
            image.blit(self.onion, (0,0))

        drawStick(image, self.data['scene'], self.panning(), False, self.data['zoom'], self.data['editing'])

        if not self.data['playing']: 
            drawStick(image, self.data['scene'], self.panning(), True, self.data['zoom'], self.data['editing'])
        
        camrect = self.camerarect()
        pygame.draw.rect(image, (100,100,255), camrect, 1)
        pygame.draw.rect(image, (100,100,0), pygame.Rect(Vector(camrect.left+camrect.width, camrect.top+camrect.height), Vector(10,10)), 1)
        pygame.draw.rect(image, (100,100,0), pygame.Rect(Vector(camrect.left-10, camrect.top-10), Vector(10,10)), 1)
        
        if self.selected and self.select[0]:
            if self.select[2] == "box":
                pygame.draw.rect(image, (0,0,0), pygame.Rect(self.select[1] - self.pos, self.mousepos - self.select[1]), 2)
            elif self.select[2] == "lasso" and len(self.select[1]) > 2:
                pygame.draw.polygon(image, (0,0,0), self.select[1], 2)
        
        self.image = image
        
        self.redraw = True
