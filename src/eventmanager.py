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

class InputManager:

    def __init__():
        pass

    def handleEvents():
        self.currentEvents = []
        for event in pygame.event.get():
            self.currentEvents.append(keyboardMapping[event])

    def getCurrentEvents():
        return self.currentEvents
