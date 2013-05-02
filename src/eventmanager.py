################################################################################
################################################################################
#
# eventmanager.py
#
# This class contains all of the information needed for getting the currently fired
# events in our game. It also maintains the mapping from input controls to the
# various events that we need to handle from input.
#
################################################################################

import pygame

class Events:
    MOVE_LEFT=1
    MOVE_RIGHT=2
    JUMP=3
    CHANGE_COLOR_1 = 4
    CHANGE_COLOR_2 = 5
    CHANGE_COLOR_3 = 6
    RESET_COLOR = 7
    PAUSE = 8
    QUIT = 9

keyboardMapping = {
    pygame.K_p : Events.PAUSE,
    pygame.K_ESCAPE : Events.QUIT,
    pygame.K_SPACE : Events.JUMP,
    pygame.K_RIGHT : Events.MOVE_RIGHT,
    pygame.K_LEFT : Events.MOVE_LEFT,
    pygame.K_r : Events.RESET_COLOR,
    pygame.K_q : Events.CHANGE_COLOR_1,
    pygame.K_w : Events.CHANGE_COLOR_2,
    pygame.K_e : Events.CHANGE_COLOR_3,
}

nameMapping = {
    "Pause" : Events.PAUSE,
    "Quit" : Events.QUIT,
    "Jump" : Events.JUMP,
    "Right" : Events.MOVE_RIGHT,
    "Left" : Events.MOVE_LEFT,
    "Reset Color" : Events.RESET_COLOR,
    "Use Color 1" : Events.CHANGE_COLOR_1,
    "Use Color 2" : Events.CHANGE_COLOR_2,
    "Use Color 3" : Events.CHANGE_COLOR_3
}

cheesyReverseMapping = {
    Events.PAUSE : pygame.K_p,
    Events.QUIT : pygame.K_ESCAPE,
    Events.JUMP : pygame.K_SPACE,
    Events.MOVE_RIGHT : pygame.K_RIGHT,
    Events.MOVE_LEFT : pygame.K_LEFT,
    Events.RESET_COLOR : pygame.K_r,
    Events.CHANGE_COLOR_1 : pygame.K_q,
    Events.CHANGE_COLOR_2 : pygame.K_w,
    Events.CHANGE_COLOR_3 : pygame.K_e
}

def changeMappings(key, event):
    oldKey = cheesyReverseMapping[event]
    keyboardMapping[key] = event
    keyboardMapping[oldKey] = 0
    cheesyReverseMapping[event] = key

class InputManager:

    def __init__(self):
        self.currentEvents = []

    def handleEvents(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN and event.key in keyboardMapping:
                self.currentEvents.append(keyboardMapping[event.key])

            elif event.type == pygame.KEYUP and event.key in keyboardMapping:
                self.removeCurrentEvent(keyboardMapping[event.key])

            elif event.type == pygame.QUIT:
                self.currentEvents.append(Events.QUIT)

    def getCurrentEvents(self):
        return self.currentEvents

    def isCurrentEvent(self, event):
        return event in self.currentEvents

    def removeCurrentEvent(self, event):
        self.currentEvents = filter(lambda x : x != event, self.currentEvents)

    # returns true if the event is in the list and then removes it
    def debounceEvent(self, event):
        fired = self.isCurrentEvent(event)
        self.removeCurrentEvent(event)
        return fired

    def clearEvents(self):
        self.currentEvents = []
