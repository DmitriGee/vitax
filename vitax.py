from __future__ import annotations

import pygame
from display import Display
from activity import Activity
from systemUI.home import HomeActivity # FIXME: Find an alternative default activity.

class Vitax:
    activityStorage: dict = {}
    activity: Activity | None = None
    display: Display
    def __init__(self) -> None:
        self.display = Display(self)
    def loop(self) -> None:
        if self.activity:
            self.activity.loop(self)
            self.display.drawActivity(self.activity)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                else:
                    self.activity.event(event)
            if self.activity.shouldExit:
                self.setActivity(HomeActivity()) # FIXME: Find an alternative default activity 
            

    def setActivity(self, activity: Activity) -> None:
        if self.activity:
            self.activity.quit()
        self.activity = activity
        self.activity.init(self)

    def handleCriticalException(self, e: Exception) -> bool:
        print("No methods found for handling this exception!")
        return False
