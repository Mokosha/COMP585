################################################################################
################################################################################
#
# world.py
#
# This file contains the game loop for the game. It serves as a controller for
# hooking all of the pieces (rendering, input, updates) together
#
################################################################################

import xml.etree.ElementTree as ET
from utils import *
from gameobject import *
from collider import *

class Zone:

    # The size of a zone in world space units
    ZONE_SIZE_X = 10
    ZONE_SIZE_Y = 10

    def __init__(self, levelDir, zone):
        tree = ET.parse(levelDir + os.sep + str(zone) + ".lvl")
        root = tree.getroot()
        assert root.tag == "zone"

        self.objects = []
        for child in root:
            self.objects.append( self.loadObject(child) )

    def loadCollider(self, node):
        children = list(node)
        assert len(children) == 1

        child = children[0]
        if child.tag == "box":
            x = float(child.attrib["x"])
            y = float(child.attrib["y"])

            width = float(child.attrib["width"])
            height = float(child.attrib["height"])
            
            collider = Collider(Vector2(x, y), width, height, 0)
            return collider
        else:
            raise NameError(child.tag + ": Undefined collider")

    def loadObject(self, node):
        if node.tag == "collider":
            return self.loadCollider(node)
        else:
            raise NameError(node.tag + ": Undefined object")

class World:

    def __init__(self, levelname):
        self.loadLevel(levelname)

    def loadLevel(self, levelname):
        levelDir = getRootPath() + os.sep + os.sep.join(["assets", "levels", levelname])

        zone=0
        self.zones = []
        while True:
            try:
                self.zones.append(Zone(levelDir, zone))
                zone = zone + 1
            except IOError:
                break;

    def queryObjects(self, zone):
        return self.zones[zone].objects

    # !FIXME! This returns all of the objects in the visible zones. It doesn't check
    # to see whether or not the objects are actually visible...
    #
    # !FIXME! This function also assumes that we have no vertically spaced zones.
    def queryVisibleObjects(self, campos):
        camSizeX = screen2world(screenSizeX())
        camSizeY = screen2world(screenSizeY())

        visibleStart = int(campos.x / Zone.ZONE_SIZE_X)
        visibleEnd = int( (campos.x + camSizeX) / Zone.ZONE_SIZE_X )

        toReturn = []
        for i in range(visibleStart, visibleEnd+1):
            if i >= len(self.zones):
                break

            toReturn = toReturn + self.queryObjects(i)

        return toReturn

    def render(self, time, surface, campos):
        for obj in self.queryVisibleObjects(campos):
            obj.render(time, surface, campos)
