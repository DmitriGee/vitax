from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from pygame import Rect
import random
import math

from activity import Activity
import interpolate

if TYPE_CHECKING:
    from vitax import Vitax
    from display import Display

def random_point_in_circle(cx, cy, max_radius):
    theta = random.uniform(0, 2 * math.pi)

    r = max_radius * (random.random() ** 2)

    x = cx + r * math.cos(theta)
    y = cy + r * math.sin(theta)

    return (x, y)

class BirdsActivity(Activity):
    seeds: list[list[int]]
    movingSeeds: list[list[int]]
    birds: list[list[int]]
    def init(self, vitax: Vitax):
        self.vitax = vitax
        self.seeds = []
        self.fallingSeeds = []
        self.birds = []

    def loop(self, vitax: Vitax) -> None:
        if len(self.seeds) + len(self.fallingSeeds) < 10:
            if random.randint(0,120):
                point = random_point_in_circle(240,400,200)
                self.fallingSeeds.append([int(point[0]),int(point[1]*0.5),0.0])
        for i, seed in enumerate(self.fallingSeeds):
            interpolate.interpolate(seed[2], interpolate.Method.BOUNCE, interpolate.Direction.OUT)
            seed[2] += 0.05
            if seed[2] >= 1.0:
                self.seeds.append([seed[0],seed[1]])
                self.fallingSeeds.pop(i)
                print("Move Seed",self.fallingSeeds,self.seeds)


    def draw(self, display: Display):
        display.renderer.draw_color = (255,255,255,255)
        for seed in self.seeds:
            display.renderer.fill_rect(Rect(seed[0]-2,seed[1]-2,4,4))
        

    
    def event(self, event: pygame.event.Event) -> None:
        pass # FIXME: Implement this!

        
