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

class Zone:

    def __init__(self, levelDir, zone):
        tree = ET.parse(levelDir + os.sep + str(zone) + ".lvl")
        root = tree.getroot()
        assert root.tag == "zone"

        self.objects = []
        for child in root:
            self.objects.append( self.loadObject(child) )

    def loadObject(self, node):
        return GameObject()

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
        pass

    def queryVisibleObjects(self, camera):
        pass

    def render(self, camera):
        pass
