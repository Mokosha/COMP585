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
import copy
from utils import *
from gameobject import *
from collider import *
from colorvortex import *
from player import *

class Zone:

    # The size of a zone in world space units
    ZONE_SIZE_X = 10
    ZONE_SIZE_Y = 10

    def __init__(self, levelDir, zone):
        basename = levelDir + os.sep + str(zone)
        tree = ET.parse(basename + ".lvl")
        root = tree.getroot()
        assert root.tag == "zone"

        self.zone = zone
        self.objects = []
        self.playerStart = None
        hasPlayerStart = False
        for child in root:
            o = self.loadObject(child)
            o.zone = zone
            self.objects.append( o )
            if isinstance(o, PlayerStartGizmo):
                hasPlayerStart = True

        if not hasPlayerStart:
            print "WARNING: Zone " + str(zone) + " has no player start gizmo!"

        self.background = pygame.image.load(basename + ".png")

    def loadCollider(self, node):
        children = list(node)
        assert len(children) == 1

        child = children[0]
        if child.tag == "box":
            x = float(child.attrib["x"])
            y = float(child.attrib["y"])

            width = float(child.attrib["width"])
            height = float(child.attrib["height"])

            angle = 0.0
            if "angle" in child.attrib.iterkeys():
                angle = float(child.attrib["angle"])
            
            collider = Collider(Vector2(x, y), width, height, angle)
            return collider
        else:
            raise NameError(child.tag + ": Undefined collider")

    def loadColorVortex(self, node):
        assert len(list(node)) == 0

        wx = float(node.attrib["x"])
        wy = float(node.attrib["y"])

        colors = map(lambda x: int(255.0 * float(x)), node.attrib["color"].split(" "))

        return ColorVortex(Vector2(wx, wy), pygame.Color(colors[0], colors[1], colors[2], 255))

    def loadPlayer(self, node):

        if self.playerStart != None:
            print "WARNING: Zone " + str(self.zone) + " has multiple player start gizmos!"

        p = PlayerStartGizmo()
        x = float(node.attrib["x"])
        y = float(node.attrib["y"])
        p.pos = Vector2(x, y)
        self.playerStart = p
        return p

    def getPlayerStartGizmo(self):
        return self.playerStart

    def loadObject(self, node):
        if node.tag == "collider":
            return self.loadCollider(node)
        elif node.tag == "colorvortex":
            return self.loadColorVortex(node)
        elif node.tag == "playerstart":
            return self.loadPlayer(node)
        else:
            raise NameError(node.tag + ": Undefined object")

class World:

    def __init__(self, levelname, startZone = None):
        self.startZone = startZone
        self.loadLevel(levelname)

    def loadLevel(self, levelname):
        levelDir = getRootPath() + os.sep + os.sep.join(["assets", "levels", levelname])

        zone=0
        self.zones = []
        self.player = None

        while True:
            try:
                self.zones.append(Zone(levelDir, zone))
                zone = zone + 1
            except IOError:
                break;

        if self.startZone != None:
            if self.startZone < 0 or self.startZone >= len(self.zones):
                print "ERROR: No such zone number"
                sys.exit(1)

            zone = self.zones[self.startZone]
            ps = zone.getPlayerStartGizmo()
            if ps == None:
                print "ERROR: Zone " + str(self.startZone) + " has no player start gizmo!"
                sys.exit(1)

            self.player = Player()
            self.player.pos = copy.deepcopy(ps.pos)
            zone.objects.append(self.player)
        else:
            for zone in self.zones:
                ps = zone.getPlayerStartGizmo()
                if ps != None:
                    self.player = Player()
                    self.player.pos = copy.deepcopy(ps.pos)
                    zone.objects.append(self.player)
                    break

        if self.player == None:
            print "ERROR: Level " + levelname + " has no player start gizmos!"
            exit(1)

    def getPlayer(self):
        return self.player

    def queryObjects(self, zone):
        if zone < 0 or zone >= len(self.zones): return []
        return self.zones[zone].objects

    def getVisibleZones(self, campos):
        camSizeX = screen2world(screenSizeX())
        camSizeY = screen2world(screenSizeY())

        visibleStart = int(campos.x / Zone.ZONE_SIZE_X)
        visibleEnd = int( (campos.x + camSizeX) / Zone.ZONE_SIZE_X )

        return range(visibleStart, visibleEnd + 1)

    def changezone(self, obj, zone):
        if zone != obj.zone:
            zoneObjs = self.queryObjects(obj.zone)
            self.zones[obj.zone].objects = [x for x in zoneObjs if not x is obj]
            self.zones[zone].objects.append(obj)
            obj.zone = zone

    def process(self, campos, dt):

        objs = set()
        for zone in self.getVisibleZones(campos):
            objs = objs | set(self.queryObjects(zone))

        for obj in objs:
            obj.process(dt)

            # Make sure that all objects return to their proper zones...
            objz = int(obj.pos.x / 10)
            self.changezone(obj, objz)

        # Do collision detection for dynamic objects
        dynamicObjs = filter(lambda x: x.dynamic, objs)
        collisions = [(x, y) for x in dynamicObjs for y in objs if not x is y]
        for collision in collisions:
            a, b = collision
            a.collide(b)

        # !HACK! If the player goes below the level then reset him to his zone's
        # starting position..
        if self.player.pos.y < 0:

            search = max(0, self.player.zone - 1)
            numzones = len(self.zones)

            ps = None
            for i in range(numzones):
                zone = ((search - i) + numzones) % numzones
                ps = self.zones[zone].getPlayerStartGizmo()
                if ps != None:
                    self.player.pos = copy.deepcopy(ps.pos)
                    self.changezone(self.player, zone)
                    break

            if ps == None:
                print "ERROR: No player start gizmo to place dead player"
                sys.exit(1)

    # !FIXME! This returns all of the objects in the visible zones. It doesn't check
    # to see whether or not the objects are actually visible...
    #
    # !FIXME! This function also assumes that we have no vertically spaced zones.
    def render(self, surface, campos):

        inzone = lambda x: x >= 0 and x < len(self.zones)
        visibleZones = filter(inzone, self.getVisibleZones(campos))

        # Render zone backgrounds
        for zone in visibleZones:

            zoneSize = Vector2(Zone.ZONE_SIZE_X, Zone.ZONE_SIZE_Y)
            zonePos = Vector2(zone * Zone.ZONE_SIZE_X, Zone.ZONE_SIZE_Y )

            screenZonePos = world2screenPos(campos, zonePos)
            screenZoneSize = world2screen(zoneSize)

            zoneRect = pygame.Rect(
                screenZonePos.x,
                screenZonePos.y,
                screenZoneSize.x,
                screenZoneSize.y)

            surface.blit( self.zones[zone].background, zoneRect )

        # Render zone objects
        for zone in visibleZones:

            for obj in self.queryObjects(zone):
                obj.render(surface, campos)
