from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from pygame.event import Event
import interpolate
import datetime
from animation import Animation, AnimationPlayer
from pygame import font, Surface, Rect
from pygame._sdl2.video import Texture

from activity import Activity
from systemUI.birds import BirdsActivity

if TYPE_CHECKING:
    from vitax import Vitax
    from display import Display



class StartupAnimation(Animation[Surface]):

    def init(self):
        self.duration = 150
        self.loop = False
        
        self.surface = Surface((800,480))
        self.logoFont = font.SysFont(None, 42, True)
        self.logo = self.logoFont.render("VITAX alpha", True, (255,255,255))

    def tick(self, frame: int) -> Surface:
        if frame <= 90:
            self.surface.fill((0,0,0))
            x = (800 / 2) - (self.logo.get_width() / 2)
            i = interpolate.interpolate(min(60, frame) / 60, interpolate.Method.BOUNCE, interpolate.Direction.OUT) * 60
            y = (self.logo.get_height() / 2) + i / 60 * (240 - self.logo.get_height())
            self.surface.blit(
                self.logo,
                Rect(
                    x,
                    y,
                    self.logo.get_width(),
                    self.logo.get_height()
                )
            )
        else:
            i = interpolate.interpolate((frame-90)/60, interpolate.Method.SINE, interpolate.Direction.IN)
            colorI = int(i*15)
            self.surface.fill((colorI,colorI,colorI*4))
            self.surface.set_alpha(int(255-i*255))
            self.surface.blit(
                self.logo,
                Rect(
                    (800 / 2) - (self.logo.get_width() / 2),
                    (self.logo.get_height() / 2) + (240 - self.logo.get_height()),
                    self.logo.get_width(),
                    self.logo.get_height()
                )
            )
        return self.surface

class HomeActivity(Activity):
    def init(self, vitax: Vitax):
        self.vitax = vitax
        self.vitax.activityStorage["alreadyPlayedAnimation"] = True
        self.timeFormat = "%I:%M %p"
        self.timeFont = font.Font("assets/fonts/JosefinSans-Regular.ttf", 48)
        self.lastTime = datetime.datetime.now().astimezone().strftime(self.timeFormat)
        self.timeSurface = self.timeFont.render(self.lastTime, 1, (255,255,255))
        self.animation = StartupAnimation()
        self.animationPlayer = AnimationPlayer[Surface]()
        self.animationPlayer.load(self.animation)
        self.inBirds = False
        self.birdsActivity = BirdsActivity()

    def draw(self, display: Display):
        display.renderer.draw_color = (15,15,60,255)
        display.renderer.fill_rect((0,0,800,480))
        
        if datetime.datetime.now().astimezone().strftime(self.timeFormat) != self.lastTime:
            self.lastTime = datetime.datetime.now().astimezone().strftime(self.timeFormat)
            self.timeSurface = self.timeFont.render(self.lastTime, 1, (255,255,255))
        display.renderer.blit(
            Texture.from_surface(display.renderer, self.timeSurface),
            Rect(
                20,
                20,
                self.timeSurface.get_width(),
                self.timeSurface.get_height()
            )
        )
        
        
        if self.animationPlayer.frame < self.animation.duration:
            cel = self.animationPlayer.tick()
            texture = Texture.from_surface(display.renderer, cel)
            display.renderer.blit(texture, texture.get_rect())
        
        if self.inBirds:
            self.birdsActivity.loop(self.vitax)
            self.birdsActivity.draw(self.vitax.display)

    def event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b and not self.inBirds:
            self.inBirds = True
            self.birdsActivity.init(self.vitax)
            print("Activated birds")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.inBirds:
            self.inBirds = False
            self.birdsActivity.quit()
            print("Deactivated birds")
        
