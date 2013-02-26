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

import pygame
from math import pi, sqrt, cos, sin, atan
from objs import *

def deg2rad(deg):
    return deg * pi / 180

def rad2deg(rad):
    return rad * 180 / pi

def polar2cart(ang, dist = None):
    if dist == None:
        dist = ang[1]
        ang = ang[0]
    ang = 90 - ang
    ang = deg2rad(ang)
    x = dist * cos(ang)
    y = dist * sin(ang)
    return [x,-y]

def cart2polar(x, y = None):
    if y == None:
        y = x[1]
        x = x[0]
    x = float(x)
    y = -float(y)
    dist = sqrt(x**2 + y**2)
    if x == 0: return [0,0]
    if (x >= 0):
        ang = atan(y / x)
    else:
        ang = pi + atan(y / x)
    ang = rad2deg(ang)
    ang = 90 - ang
    ang = ang % 360
    return [ang, dist]

def direction(pos1, pos2):
    val = 0
    quad = 0
    w = float(pos2[0] - pos1[0])
    h = float(pos2[1] - pos1[1])
    
    if w >= 0 and h < 0: val, quad = 0, 1
    elif w > 0 and h >= 0: val, quad = 90, 0
    elif w <= 0 and h > 0: val, quad = 180, 1
    elif w < 0 and h <= 0: val, quad = 270, 0
    
    if w == 0 and h == 0: quad = -1
    
    if quad == 0:
        a = atan(abs(h) / abs(w))
    elif quad == 1:
        a = atan(abs(w) / abs(h))
    else:
        a = 0
    
    val += a / (2*pi) * 360
    return val

def distance(pos1, pos2):
    w = abs(pos1[0] - pos2[0])
    h = abs(pos1[1] - pos2[1])
    return sqrt(( w ** 2) + ( h ** 2))

def translate(point, off):
    return [point[0] + off[0], point[1] + off[1]]

def addvectors(vec1, vec2 = None):
    if vec2 == None:
        vec2 = vec1[1]
        vec1 = vec1[0]
    c1 = polar2cart(vec1[0], vec1[1])
    c2 = polar2cart(vec2[0], vec2[1])
    x = c1[0] + c2[0]
    y = c1[1] + c2[1]
    return cart2polar(x, y)

def intlist(list):
    newlist = []
    for item in list:
        newlist.append(int(item))
    return newlist

def drawline(image, colour, start, end, width, endcircles = False):
    pygame.draw.polygon(image, colour, [translate(start, polar2cart(direction(start, end) + 90, width/2)),
                     translate(start, polar2cart(direction(start, end) - 90, width/2)),
                     translate(end, polar2cart(direction(end, start) + 90, width/2)),
                     translate(end, polar2cart(direction(end, start) - 90, width/2))])
    if endcircles:
        pygame.draw.circle(image, colour, intlist(start), abs(int(width/2+.5)))
        pygame.draw.circle(image, colour, intlist(end), abs(int(width/2+.5)))
    return image

def drawaaline(image, colour, start, end, width, endcircles = False):
    pygame.draw.polygon(image, colour, [translate(start, polar2cart(direction(start, end) + 90, width/2)),
                     translate(start, polar2cart(direction(start, end) - 90, width/2)),
                     translate(end, polar2cart(direction(end, start) + 90, width/2)),
                     translate(end, polar2cart(direction(end, start) - 90, width/2))])
    pygame.draw.aalines(image, colour, True, [intlist(translate(start, polar2cart(direction(start, end) + 90, width/2))),
                     intlist(translate(start, polar2cart(direction(start, end) - 90, width/2))),
                     intlist(translate(end, polar2cart(direction(end, start) + 90, width/2))),
                     intlist(translate(end, polar2cart(direction(end, start) - 90, width/2)))])
    if endcircles:
        pygame.draw.circle(image, colour, intlist(start), abs(int(width/2+.5)))
        pygame.draw.circle(image, colour, intlist(end), abs(int(width/2+.5)))
    return image

def drawcircle(image, colour, origin, radius, width=0):
    if width == 0:
        pygame.draw.circle(image,colour,intlist(origin),int(radius))
    else:
        if radius > 65534/5: radius = 65534/5
        if radius < 0: radius = -radius
        if width < 0: width = -width
        circle = pygame.Surface([radius*2+width,radius*2+width]).convert_alpha()
        circle.fill([0,0,0,0])
        pygame.draw.circle(circle, colour, intlist([circle.get_width()/2, circle.get_height()/2]), int(radius+(width/2)))
        if int(radius-(width/2)) > 0: pygame.draw.circle(circle, [0,0,0,0], intlist([circle.get_width()/2, circle.get_height()/2]), abs(int(radius-(width/2))))
        image.blit(circle, [origin[0] - (circle.get_width()/2), origin[1] - (circle.get_height()/2)])

#def drawaacircle(image, colour, origin, radius, width=0):
#    if width == 0:
#        aacircle(image,colour,origin,radius)
#        pygame.draw.circle(image,colour,origin,radius)
#    else:
#        for i in range(width*3):
#            aacircle(image, colour, origin, radius + (i/3) - (width/3))

#def aacircle(image, colour, origin, radius):
#    poly = []
#    circ = int(2 * pi * radius*2)
#    for i in range(circ):
#        poly.append(translate(polar2cart(i/float(circ)*360,float(radius)), origin))
#    pygame.draw.aalines(image, colour, True, poly)

def drawaacircle(image, colour, origin, radius, width=0):
    radius = 2*radius
    if radius > 65535/2: radius = 65535/2
    width = 2*width-1
    if width <= 0:
        circle = pygame.Surface([radius*2,radius*2]).convert_alpha()
        circle.fill([0,0,0,0])
        pygame.draw.circle(circle,colour,intlist(origin),int(radius))
        pygame.draw.circle(circle, colour, intlist([circle.get_width()/2, circle.get_height()/2]), int(radius+(width/2)))
        pygame.draw.circle(circle, [0,0,0,0], intlist([circle.get_width()/2, circle.get_height()/2]), abs(int(radius-(width/2))))
        circle = pygame.transform.smoothscale(circle, (circle.get_width() / 2, circle.get_height() / 2))
        image.blit(circle, [origin[0] - (circle.get_width()/2), origin[1] - (circle.get_height()/2)])
    else:
        circle = pygame.Surface([radius*2+width,radius*2+width]).convert_alpha()
        circle.fill([0,0,0,0])
        pygame.draw.circle(circle, colour, intlist([circle.get_width()/2, circle.get_height()/2]), int(radius+(width/2)))
        if int(radius-(width/2)) > 0: pygame.draw.circle(circle, [0,0,0,0], intlist([circle.get_width()/2, circle.get_height()/2]), abs(int(radius-(width/2))))
        circle = pygame.transform.smoothscale(circle, (circle.get_width() / 2, circle.get_height() / 2))
        image.blit(circle, [origin[0] - (circle.get_width()/2), origin[1] - (circle.get_height()/2)])

# Stick stuff:

def drawStick(Surface, Stick, Offset, DrawVertices = False, SizeRatio = 1, SelectedVerts = [], AngOff = 0, ForceColour=-1):
    if ForceColour == -1:
        Colour = Stick['colour'].value
    else:
        Colour = ForceColour
    
    if DrawVertices:
        selected = False
        for vert in SelectedVerts:
            if Stick is vert: selected = True
    
    if Stick['cartesian'].value:
        NewOffset = Vector(Offset) + Vector(Stick['pos'].value) * SizeRatio
        if DrawVertices:
            if selected:
                pygame.draw.circle(Surface, (255, 136, 0), intlist(NewOffset), abs(int((Stick['width'].value/2+2)*SizeRatio)))
            else:
                pygame.draw.circle(Surface, (0, 136, 255), intlist(NewOffset), abs(int((Stick['width'].value/2+2)*SizeRatio)))
    else:
        Off = polar2cart(Stick['ang'].value + AngOff, Stick['dist'].value * SizeRatio)
        NewOffset = [Offset[0] + Off[0], Offset[1] + Off[1]]
        if DrawVertices:
            if selected:
                pygame.draw.circle(Surface, (255, 0, 0), intlist(NewOffset), abs(int((Stick['width'].value/2+2)*SizeRatio)))
            else:
                pygame.draw.circle(Surface, (0, 255, 0), intlist(NewOffset), abs(int((Stick['width'].value/2+2)*SizeRatio)))
    if not Stick['hidden'].value and not DrawVertices:
        #if Stick['shape'].value == 0:
        #    drawline(Surface, Colour, Offset, NewOffset, Stick['width'].value * SizeRatio, True)
        #elif Stick['shape'].value == 1:
        #    drawcircle(Surface, Colour, Vector((Offset[0] + NewOffset[0]) / 2, (Offset[1] + NewOffset[1]) / 2), Stick['dist'].value * SizeRatio / 2, Stick['width'].value * SizeRatio)
        #else:
        Stick['shape'].draw(Surface, Vector(Offset), Vector(NewOffset), Stick, SizeRatio)
    
    Offset = NewOffset
    
    for seg in Stick['children']:
        Surface = drawStick(Surface, seg, deepcopy(Offset), DrawVertices, SizeRatio, SelectedVerts, Stick['ang'].value + AngOff, ForceColour)
        #thread.start_new_thread(drawStick, (Surface, seg, deepcopy(Offset), DrawVertices, SizeRatio, SelectedVerts, Stick['ang'].value + AngOff, ForceColour))
    #threads -= 1
    
    #while not threads == 0: pass
    
    return Surface

def gather(limbs, Stick, Offset, SizeRatio = 1, AngOff = 0):
    if ForceColour == -1:
        Colour = Stick['colour'].value
    else:
        Colour = ForceColour
    
    if DrawVertices:
        selected = False
        for vert in SelectedVerts:
            if Stick is vert: selected = True
    
    if Stick['cartesian'].value:
        NewOffset = Vector(Offset) + Vector(Stick['pos'].value) * SizeRatio
        if DrawVertices:
            if selected:
                pygame.draw.circle(Surface, (255, 136, 0), intlist(NewOffset), abs(int((Stick['width'].value/2+2)*SizeRatio)))
            else:
                pygame.draw.circle(Surface, (0, 136, 255), intlist(NewOffset), abs(int((Stick['width'].value/2+2)*SizeRatio)))
    else:
        Off = polar2cart(Stick['ang'].value + AngOff, Stick['dist'].value * SizeRatio)
        NewOffset = [Offset[0] + Off[0], Offset[1] + Off[1]]
        if DrawVertices:
            if selected:
                pygame.draw.circle(Surface, (255, 0, 0), intlist(NewOffset), abs(int((Stick['width'].value/2+2)*SizeRatio)))
            else:
                pygame.draw.circle(Surface, (0, 255, 0), intlist(NewOffset), abs(int((Stick['width'].value/2+2)*SizeRatio)))
    if not Stick['hidden'].value and not DrawVertices:
        Stick['shape'].draw(Surface, Vector(Offset), Vector(NewOffset), Stick, SizeRatio)
    
    Offset = NewOffset
    
    for seg in Stick['children']:
        Surface = drawStick(Surface, seg, deepcopy(Offset), DrawVertices, SizeRatio, SelectedVerts, Stick['ang'].value + AngOff, ForceColour)
    
    return Surface

# Find what vertex the mouse is hovering over
def getGrab(mousepos, Stick, Offset = Vector(0, 0), SizeRatio = 1, AngOff = 0):
    if Stick['cartesian'].value:
        Offset += Vector(Stick['pos'].value) * SizeRatio
    else:
        Off = polar2cart(Stick['ang'].value + AngOff, Stick['dist'].value * SizeRatio)
        Offset += Vector(Off[0], Off[1])
    
    grab = None
    if sqrt((mousepos[0] - Offset[0]) ** 2 + (mousepos[1] - Offset[1]) ** 2) < (Stick['width'].value/2+2)*SizeRatio:
        grab = Stick
        #print grab
    elif len(Stick['children']) > 0:
        for seg in Stick['children']:
            tgrab = getGrab(mousepos, seg, Offset, SizeRatio, Stick['ang'].value + AngOff)
            if not tgrab == None:
                grab = tgrab
    
    return grab

# Perform the vertex grabbing action, like rotating and moving
def doGrab(mousepos, Stick, drag, stretchmode = False, Offset = Vector(0,0), SizeRatio = 1, AngOff = 0):
    if Stick['cartesian'].value:
        if drag is Stick:
            Stick['pos'].value = Vector(mousepos - Offset) * (1/SizeRatio)
        Offset += Vector(Stick['pos'].value) * SizeRatio
    else:
        if drag is Stick:
            dir = (direction(Offset, mousepos) - (AngOff % 360))
            dirdiff = dir - (Stick['ang'].value % 360)
            if dirdiff > 180:
                dirdiff = dirdiff - 360
            elif dirdiff < -180:
                dirdiff = dirdiff + 360
            Stick['ang'].value += dirdiff
            if stretchmode:
                dist = distance(Offset, mousepos)/SizeRatio
                Stick['dist'].value = dist
        Off = Vector(polar2cart(Stick['ang'].value + AngOff, Stick['dist'].value * SizeRatio))
        Offset = Offset + Off
        
    if len(Stick['children']) > 0:
        for seg in Stick['children']:
            doGrab(mousepos, seg, drag, stretchmode, Offset, SizeRatio, Stick['ang'].value + AngOff)

def getCollide(map, Stick, Offset = Vector(0, 0), SizeRatio = 1, AngOff = 0):
    list = []
    if Stick['cartesian'].value:
        Offset += Vector(Stick['pos'].value) * SizeRatio
    else:
        Off = polar2cart(Stick['ang'].value + AngOff, Stick['dist'].value * SizeRatio)
        Offset += Vector(Off[0], Off[1])
    
    if map.get_rect().collidepoint(Offset) and map.get_at(intlist(Offset))[0] > 150:
        list += [Stick]
    for seg in Stick['children']:
        list += getCollide(map, seg, Offset, SizeRatio, Stick['ang'].value + AngOff)
    
    return list

def deleteVerts(verts, scene):
    for vert in verts:
        scene['children'] = [c for c in scene['children'] if not c is vert]
    for i in range(len(scene['children'])):
        deleteVerts(verts, scene['children'][i])

def deleteFigure(item, Stick, drag, Offset = Vector(0,0), SizeRatio = 1, AngOff = 0):
    if Stick['cartesian']:
        if drag is Stick:
            Stick['pos'] = Vector(mousepos - Offset) * (1/SizeRatio)
        Offset += Vector(Stick['pos']) * SizeRatio
    else:
        if drag is Stick:
            Stick['ang'] = direction(Offset, mousepos)-AngOff
        Off = Vector(polar2cart(Stick['ang'] + AngOff, Stick['dist'] * SizeRatio))
        Offset = Offset + Off
        
    if len(Stick['children']) > 0:
        for seg in Stick['children']:
            doGrab(mousepos, seg, drag, Offset, SizeRatio, Stick['ang'] + AngOff)

def changeFrame(figure, frame=1):
    for child in figure['children']:
        changeFrame(child, frame)
    for val in figure.values():
        if isinstance(val, KeyFrame): val.setframe(frame)
        elif isinstance(val, Texture): val.setframe(frame)

def interpolateConst(frame, keys):
    val = keys[0][1]
    for key in keys:
        if key[0] > frame:
            break
        else:
            val = key[1]
    return val

def interpolateLinear(frame, keys):
    prevkey = keys[0]
    inter = True
    if len(keys) == 1:
        val = keys[0][1]
    else:
        try:
            for key in keys:
                if key[0] > frame:
                    break
                elif key[0] == frame:
                    inter = False
                    val = key[1]
                    break
                else:
                    prevkey = key
            if key == prevkey:
                val = key[1]
                inter = False
            if inter:
                if type(key[1]) == type([]) or type(key[1]) == type(Vector(0,0)) or type(key[1]) == type(()):
                    val = []
                    for i in range(len(key[1])):
                        d = (float(prevkey[1][i]) - float(key[1][i])) / (float(prevkey[0]) - float(key[0]))
                        m = frame - prevkey[0]
                        val.append(d*m+prevkey[1][i])
                else:
                    d = (float(prevkey[1]) - float(key[1])) / (float(prevkey[0]) - float(key[0]))
                    m = frame - prevkey[0]
                    val = d*m+prevkey[1]
        except:
            val = interpolateConst(frame, keys)
    return val

indentWidth = 2
def indentLines(textToIndent, levels):
    lines = textToIndent.split("\n")
    newlines = [(" " * (indentWidth * levels)) + x for x in lines]
    return "\n".join(newlines)

def Export(scene, depth=0):
    
    depthStr = " " * (indentWidth * depth)
    indentStr = " " * (indentWidth * (depth + 1))

    exp = depthStr + "<limb>\n"

    def ExportAttr(attr):
        ret = indentStr + "<" + attr + ">\n"
        ret += indentLines(str(scene[attr]), depth+2) + "\n"
        ret += indentStr + "</" + attr + ">\n"
        return ret

    exp += ExportAttr('ang');
    exp += ExportAttr('dist');
    exp += ExportAttr('pos');
    exp += ExportAttr('shape');
    exp += ExportAttr('width');
    exp += ExportAttr('colour');
    exp += ExportAttr('static');
    exp += ExportAttr('hidden');
    exp += ExportAttr('cartesian');
    
    exp += indentStr + "<children>\n"
    for limb in scene['children']:
        exp += Export(limb, depth + 2) + "\n"
    if exp[-2:] == ", ": exp = exp[:-2]
    exp += indentStr + "</children>\n"
    exp += depthStr + "</limb>"
    
    return exp

def Import(exp):
    pass

def gatherKeyFrames(Stick):
    keys = []
    for key in Stick.values():
        if isinstance(key, KeyFrame):
            keys.append(key)
    for child in Stick['children']:
        keys += gatherKeyFrames(child)
    return keys

def insertKey(keyframe, key, interpol="linear"):
    if isinstance(keyframe, KeyFrame):
        keyframe.keys.append(key)
        keyframe.clean()
    else:
        keyframe = KeyFrame([key], interpol)

def concatDict(dict1, dict2):
    for item in dict2.items():
        dict1[item[0]] = item[1]
