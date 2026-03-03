class Animation[T]:
    duration: int
    loop: bool
    def __init__(self):
        pass
    
    def init(self):
        raise NotImplementedError()

    def tick(self, frame: int) -> T:
        raise NotImplementedError()

class AnimationPlayer[T]:
    animation: Animation[T]
    frame: int = 0
    finished = False
    def __init__(self):
        pass
    def load(self, animation: Animation[T]):
        self.animation = animation
        self.reset()
    def reset(self):
        self.frame = 0
        self.animation.init()
    def tick(self) -> T:
        if self.frame < self.animation.duration:
            self.frame += 1
        cel = self.animation.tick(self.frame)
        if self.frame > self.animation.duration and self.animation.loop:
            self.reset()
        return cel

