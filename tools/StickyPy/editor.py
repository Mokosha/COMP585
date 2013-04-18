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

    def getpos(self):
        return Vector(-(self.size[0] * 0.5), -(self.size[1] * 0.5))

    def getmousepos(self):
        mouse_pos_x = self.mousepos[0] - (self.size[0] * 0.5)
        mouse_pos_y = self.mousepos[1] - (self.size[1] * 0.5)
        return Vector(mouse_pos_x, mouse_pos_y) - self.pos

    def getcamerapos(self):
        return 

    def mwheelup(self):
        if self.hover:
            self.zoom(1.2, self.getmousepos())
            self.drawonion()
            self.draw()

    def mwheeldown(self):
        if self.hover:
            self.zoom(1/1.2, self.getmousepos())

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

    def getgrab(self):
        return getGrab(self.getmousepos(), self.data['scene'], self.panning(), self.data['zoom'])

    def lclick(self):
        if self.hover and self.selected and not self.data['playing']:
            tedit = self.getgrab()
            if not tedit == None:

                if self.container.widgets['ExtrudeCheckBox'].checked:
                    extruded = dict(deepcopy(tedit), children=[], pos=KeyFrame(Vector(0,0)), dist=KeyFrame(0))
                    tedit['children'].append(extruded)
                    tedit = extruded

                if not tedit['static'].value or self.container.widgets['ExtrudeCheckBox'].checked:
                    self.data['drag'] = tedit
                    self.dragging = True
                    
                if self.keyboard[pygame.K_RSHIFT] or self.keyboard[pygame.K_LSHIFT]:
                    tedit = self.getgrab()
                    contains = False
                    for limb in self.data['editing']:
                        if limb is tedit:
                            contains = True
                            if len(self.data['editing']) > 1:
                                self.data['editing'] = [l for l in self.data['editing'] if not l is limb]
                                self.container.widgets['KeyFrameEditor'].changelimbs(self.data['editing'])
                            break
                    if not contains: self.data['editing'] += [tedit]

                elif not tedit in self.data['editing']:
                    self.data['editing'] = [self.getgrab()]

                self.container.widgets['KeyFrameEditor'].changelimbs(self.data['editing'])
                self.draw()
            elif self.cameraresizeover(self.getmousepos()-self.getpos()):
                self.cameradrag = [2, deepcopy(self.getmousepos()), deepcopy(self.data['camera']['zoom'].value)]
            elif self.cameraover(10, self.getmousepos()-self.getpos()):
                self.cameradrag = [1, deepcopy(self.getmousepos()), deepcopy(self.data['camera']['pos'].value)]
            elif self.keyboard[pygame.K_LCTRL] or self.keyboard[pygame.K_RCTRL]:
                self.select = [True, [self.getmousepos() - self.getpos()], "lasso"]
            else:
                self.select = [True, self.getmousepos(), "box"]

        if len(self.data['editing']) > 0 and self.selected: 
            self.container.widgets['ShapeEditor'].changelimb()

    def lrelease(self):
        if self.select[0]:
            map = pygame.Surface(self.image.get_size())
            map.fill((0,0,0))

            if self.select[2] == "box":
                self.drawBoxSelection(map, (255, 255, 255), 0)
            elif self.select[2] == "lasso" and len(self.select[1]) > 2:
                self.drawLassoSelection(map, (255, 255, 255), 0)

            if self.keyboard[pygame.K_LSHIFT] or self.keyboard[pygame.K_RSHIFT]:
                self.data['editing'] += getCollide(map, self.data['scene'], (self.size * 0.5) + self.panning(), self.data['zoom'], 0)
            else:
                self.data['editing'] = getCollide(map, self.data['scene'], (self.size * 0.5) + self.panning(), self.data['zoom'], 0)

            self.select[0] = False
        self.dragging = False
        self.cameradrag[0] = 0
        if not self.data['editing'] == [] and self.selected: self.container.widgets['ShapeEditor'].changelimb()
        if self.hover and self.selected:
            self.container.widgets['KeyFrameEditor'].changelimbs(self.data['editing'])
            self.drawonion()
            self.draw()

    def mousemove(self):
        # If lasso mode is on
        if self.select[0] and self.select[2] == "lasso":
            self.select[1] += [self.getmousepos() - self.getpos()]
            if not self.data['playing']: self.draw()
        
        # If the camera is being dragged (1 means panning, 2 means zooming:
        if self.cameradrag[0] == 1:
            self.data['camera']['pos'].value = (Vector(self.cameradrag[2]) - self.cameradrag[1] + self.getmousepos())  / self.data['zoom']
        elif self.cameradrag[0] == 2:
            cam_pos_y = self.data['camera']['pos'].value.y
            mouse_pos_y = self.getmousepos().y
            pos_y = self.getpos().y
            panning_y = self.panning().y
            cam_size_y = float(self.data['camera']['size'].y)
            zoom = self.data['zoom']
            self.data['camera']['zoom'].value = (mouse_pos_y - cam_pos_y - panning_y) / cam_size_y / zoom
        
        if self.selected: # If the editor was the last widget to be clicked
            if self.mousebut[1] and not self.viewdrag: # Set to view panning mode when the middle mouse is clicked
                self.viewdrag = True
                self.viewdragorig = Vector(self.data['panning'])
                self.viewdragmouse = Vector(self.getmousepos())

            elif self.mousebut[1] and self.viewdrag: # Pan the view
                self.data['panning'] = Vector(self.viewdragorig + (self.getmousepos() - self.viewdragmouse)/self.data['zoom'])

            else:
                self.viewdrag = False

            if not self.data['playing']: 
                self.draw()
        
        # If a vertex is being dragged, move it around
        if self.mousebut[0] and self.data['drag'] and self.dragging:
            doGrab(self.getmousepos(), self.data['scene'], self.data['drag'], self.container.widgets['StretchCheckBox'].checked or self.container.widgets['ExtrudeCheckBox'].checked, self.panning(), self.data['zoom'])
            if not self.data['playing']: self.draw()
        
        # Set the mouse over comment
        tover = self.getgrab()
        if not tover == None:
            self.comment = ("Static, " if tover['static'].value else "") + ("Cartesian offset" if tover['cartesian'].value else "Polar offset")
        else:
            self.comment = ""

    def mrelease(self):
        self.drawonion()
        self.draw()

    # Returns the pygame RECT of the camera that is used in the scene...
    def camerarect(self):
        campos = Vector(self.data['camera']['pos'].value) + (self.size * 0.5)
        return pygame.Rect(
            campos * self.data['zoom'] + self.panning(), 
            self.data['camera']['size'] * self.data['camera']['zoom'].value * self.data['zoom']
        )

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
        tedit = self.getgrab()
        if tedit:
            self.draw()
            self.container.window.menu.showmenu([
                    ("Insert keyframe", "insertkey"), 
                    ("Edit keyframes", "editkeys"), 
                    ("Edit limb shape", "editshape"), 
                    ("Delete", "delete"), 
                    ("Copy", "copy"), 
                    ("Paste", "paste"), 
                    ("Store Selection", "selstore"), 
                    ("Recall Selection", "selrecall")
            ], self.mousepos, self, 20)
            
        elif self.cameraover(10, self.getmousepos()-self.getpos()):
            self.container.window.menu.showmenu([
                     ("Insert keyframe", "insertcamkey"), 
                     ("Edit keyframes", "editcamkeys"), 
                     ("Edit camera shape", "editcamshape")
            ], self.getmousepos(), self, 20)

    def always(self):
        if self.data['playing']: self.draw()

    def menuaction(self, selection):
        if selection == "editkeys":
            self.container.widgets['KeyFrameEditor'].visible = True
            self.container.widgets['KeyFrameEditor'].changelimbs(self.data['editing'])
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
                drawStick(surface, onionscene, (self.size * 0.5) + self.panning(), False, self.data['zoom'], self.data['editing'])

                surface.set_alpha(255/8*(i+5))
                self.onion.blit(surface, (0,0))

    def panning(self): 
        return self.data['panning'] * self.data['zoom']

    def drawBoxSelection(self, image, color=(0, 0, 0), width=2):
        pygame.draw.rect(image, color, pygame.Rect(self.select[1] - self.getpos(), self.getmousepos() - self.select[1]), width)

    def drawLassoSelection(self, image, color=(0, 0, 0), width=2):
        pygame.draw.polygon(image, color, self.select[1], width)

    def draw(self):
        self.image.fill((255,255,255))
        self.threaddraw()

    def threaddraw(self):

        image = self.image

        if self.data['OnionSkinning'] and not self.mousebut[1]:
            image.blit(self.onion, (0,0))

        drawStick(image, self.data['scene'], (self.size * 0.5) + self.panning(), False, self.data['zoom'], self.data['editing'])

        if not self.data['playing']: 
            drawStick(image, self.data['scene'], (self.size * 0.5) + self.panning(), True, self.data['zoom'], self.data['editing'])
        
        camrect = self.camerarect()
        pygame.draw.rect(image, (100,100,255), camrect, 1)
        pygame.draw.rect(image, (100,100,0), pygame.Rect(Vector(camrect.left+camrect.width, camrect.top+camrect.height), Vector(10,10)), 1)
        pygame.draw.rect(image, (100,100,0), pygame.Rect(Vector(camrect.left-10, camrect.top-10), Vector(10,10)), 1)
        
        if self.selected and self.select[0]:
            if self.select[2] == "box":
                self.drawBoxSelection(image)
            elif self.select[2] == "lasso" and len(self.select[1]) > 2:
                self.drawLassoSelection(image)                
        
        self.image = image
        
        self.redraw = True
