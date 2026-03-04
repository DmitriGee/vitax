from __future__ import annotations
from typing import TYPE_CHECKING
import math
import pygame
from pygame import font, Surface, Rect
from pygame._sdl2 import video
from pygame._sdl2.video import Texture
from pygame.event import Event
import interpolate
import datetime
from animation import Animation, AnimationPlayer

from activity import Activity

if TYPE_CHECKING:
    from vitax import Vitax
    from display import Display

def get_point_on_circle(center_x, center_y, radius, angle_degrees):
    x = center_x + radius * math.cos(math.radians(angle_degrees))
    y = center_y + radius * math.sin(math.radians(angle_degrees))
    return (int(x), int(y))

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
    activeJoystick: pygame.joystick.JoystickType | None
    J_a: bool = False
    rmblTime = 0

    def init(self, vitax: Vitax):
        pygame.joystick.init()
        self.vitax = vitax
        self.vitax.activityStorage["alreadyPlayedAnimation"] = True
        self.timeFormat = "%I:%M %p"
        self.dateFormat = "%A, %B %d"
        self.timeFont = font.Font("assets/fonts/JosefinSans-Regular.ttf", 32)
        self.dateFont = font.Font("assets/fonts/JosefinSans-Regular.ttf", 16)
        self.lastTime = datetime.datetime.now().astimezone().strftime(self.timeFormat)
        self.lastDate = datetime.datetime.now().astimezone().strftime(self.dateFormat)
        self.timeSurface = self.timeFont.render(self.lastTime, 1, (255,255,255))
        self.dateSurface = self.dateFont.render(self.lastDate, 1, (255,255,255))
        self.animation = StartupAnimation()
        self.animationPlayer = AnimationPlayer[Surface]()
        self.animationPlayer.load(self.animation)
        joycount = pygame.joystick.get_count()
        if joycount > 0:
            self.activeJoystick = pygame.joystick.Joystick(0)
            self.activeJoystick.init()
        else:
            self.activeJoystick = None
    
    def loop(self, vitax: Vitax) -> None:
        if datetime.datetime.now().astimezone().strftime(self.timeFormat) != self.lastTime:
            self.lastTime = datetime.datetime.now().astimezone().strftime(self.timeFormat)
            self.timeSurface = self.timeFont.render(self.lastTime, 1, (255,255,255))
        if datetime.datetime.now().astimezone().strftime(self.dateFormat) != self.lastDate:
            self.lastDate = datetime.datetime.now().astimezone().strftime(self.dateFormat)
            self.dateSurface = self.dateFont.render("Wednesday, September 31", 1, (255,255,255))
        
        if self.activeJoystick:
            if self.activeJoystick.get_button(pygame.CONTROLLER_BUTTON_A):
                if not self.J_a:
                    self.J_a = True
            else:
                self.J_a = False

    def draw(self, display: Display, deltaTime: float):
        display.renderer.draw_color = (15,15,60,255)
        display.renderer.fill_rect((0,0,800,480))
        
        display.renderer.blit(
            Texture.from_surface(display.renderer, self.timeSurface),
            Rect(
                90-(self.timeSurface.get_width()/2),
                30-(self.timeSurface.get_height()/2),
                self.timeSurface.get_width(),
                self.timeSurface.get_height()
            )
        )
        display.renderer.blit(
            Texture.from_surface(display.renderer, self.dateSurface),
            Rect(
                90-(self.dateSurface.get_width()/2),
                65-(self.dateSurface.get_height()/2),
                self.dateSurface.get_width(),
                self.dateSurface.get_height()
            )
        )
        
        if self.activeJoystick:
            ljx = round(self.activeJoystick.get_axis(0),3)
            ljy = round(self.activeJoystick.get_axis(1),3)
            rjx = round(self.activeJoystick.get_axis(2),3)
            rjy = round(self.activeJoystick.get_axis(3),3)
        else:
            ljx = 0
            ljy = 0
            rjx = 0
            rjy = 0
        
        display.renderer.draw_color = (255,255,255,255)
        count = 64
        for i in range(count):
            step = 360 / count
            start_angle = i * step
            end_angle = (i + 1) * step

            start_point = get_point_on_circle(48,128,32,start_angle)
            end_point = get_point_on_circle(48,128,32,end_angle)
            display.renderer.draw_line(start_point, end_point)

            start_point = (start_point[0]+86,start_point[1])
            end_point = (end_point[0]+86,end_point[1])
            display.renderer.draw_line(start_point, end_point)
        display.renderer.draw_line((48,128),(int(48+(ljx*32)),int(128+(ljy*32))))
        display.renderer.fill_rect(Rect(
            int(48+(ljx*32))-2,
            int(128+(ljy*32))-2,
            4,
            4
        ))
        display.renderer.draw_line((48+86,128),(int(48+86+(rjx*32)),int(128+(rjy*32))))
        display.renderer.fill_rect(Rect(
            int(48+86+(rjx*32))-2,
            int(128+(rjy*32))-2,
            4,
            4
        ))
            
        if self.animationPlayer.frame < self.animation.duration:
            cel = self.animationPlayer.tick()
            texture = Texture.from_surface(display.renderer, cel)
            display.renderer.blit(texture, texture.get_rect())

