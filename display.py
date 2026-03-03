from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from pygame import _sdl2 as sdl2
from pygame._sdl2 import video
from pygame._sdl2.video import Texture
from animation import AnimationPlayer

if TYPE_CHECKING:
    from vitax import Vitax
    from activity import Activity

from systemUI import home

class Display:
    window: video.Window
    renderer: sdl2.Renderer
    display_size = (800,480)

    def __init__(self, vitax: "Vitax"):
        pygame.font.init()
        sdl2.init_subsystem(sdl2.INIT_VIDEO)
        self.vitax = vitax
        self.window = sdl2.Window(title="Vitax", size=self.display_size, position=(1,33))
        self.renderer = sdl2.Renderer(self.window, -1, 1, True, False)
        self.sysFont = pygame.font.SysFont(None, 16)
        self.clock = pygame.time.Clock()

    def drawActivity(self, activity: Activity):
        deltaTime = self.clock.tick(60)

        activity.draw(self)

        text = video.Texture.from_surface(self.renderer, self.sysFont.render(f"{self.clock.get_fps():.0f}", 1, (255,255,255,255), (0,0,0,127)))
        self.renderer.blit(text, text.get_rect())


        self.renderer.present()
