from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from vitax import Vitax
    from display import Display

class Activity:
    shouldExit = False
    def __init__(self):
        pass
    def init(self, vitax: Vitax) -> None:
        pass
    def draw(self, display: Display) -> None:
        pass
    def event(self, event: pygame.event.Event) -> None:
        pass
    def loop(self, vitax: Vitax) -> None:
        pass
    def quit(self) -> None:
        pass
