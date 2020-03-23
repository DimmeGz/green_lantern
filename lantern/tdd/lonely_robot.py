class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Robot:

    def __init__(self, x, y, asteroid, direction, obstacle):
        self.x = x
        self.y = y
        self.asteroid = asteroid
        self.direction = direction
        self.obstacle = obstacle
        self.compass = ['N', 'E', 'S', 'W']
        self.health = 100
        self.battery = 100
        if self.x > self.asteroid.x or self.y > self.asteroid.y or self.x < 0 or self.y < 0:
            raise MissAsteroidError('The robot flew beside asteroid')
        if self.x == obstacle.x and self.y == obstacle.y:
            raise ObstacleCrashError('The robot crashed into an obstacle')

    def turn_left(self):
        if self.direction in self.compass:
            self.battery -= 1
            self.battery_check()
            self.direction = self.compass[self.compass.index(self.direction) - 1 \
                if self.compass.index(self.direction) - 1 != -1 else 3]

    def turn_right(self):
        if self.direction in self.compass:
            self.battery -= 1
            self.battery_check()
            self.direction = self.compass[self.compass.index(self.direction) + 1 \
                if self.compass.index(self.direction) + 1 != 4 else 0]

    def battery_check(self):
        if self.battery == 0:
            raise LowBatteryError('Battery is empty')

    def move_forward(self):
        move_ffwd_dict = {'W': (self.x - 1, self.y), 'E': (self.x + 1, self.y),
                          'S': (self.x, self.y - 1), 'N': (self.x, self.y + 1)}
        self.x, self.y = move_ffwd_dict[self.direction]
        self.battery -= 1
        self.battery_check()
        if self.x > self.asteroid.x or self.y > self.asteroid.y or self.x < 0 or self.y < 0:
            raise RobotCrashError('The robot fell down from the asteroid')
        if self.x == self.obstacle.x and self.y == self.obstacle.y:
            self.health -= 10
            if self.health == 0:
                raise RobotCrashError('Robot is destroyed')
            self.move_backward()
            self.forward_detour()

    def forward_detour(self):
        if (self.direction == 'N' and self.x != self.asteroid.x) or \
                (self.direction == 'E' and self.y != 0) or \
                (self.direction == 'S' and self.x != 0) or \
                (self.direction == 'W' and self.y != self.asteroid.y):
            self.turn_right()
            self.move_forward()
            self.turn_left()
            for _ in range(2):
                self.move_forward()
            self.turn_left()
            self.move_forward()
            self.turn_right()
        else:
            self.turn_left()
            self.move_forward()
            self.turn_right()
            for _ in range(2):
                self.move_forward()
            self.turn_right()
            self.move_forward()
            self.turn_left()

    def move_backward(self):
        move_back_dict = {'W': (self.x + 1, self.y), 'E': (self.x - 1, self.y),
                          'S': (self.x, self.y + 1), 'N': (self.x, self.y - 1)}
        self.x, self.y = move_back_dict[self.direction]
        self.battery -= 1
        self.battery_check()
        if self.x > self.asteroid.x or self.y > self.asteroid.y or self.x < 0 or self.y < 0:
            raise RobotCrashError('The robot fell down from the asteroid')
        if self.x == self.obstacle.x and self.y == self.obstacle.y:
            self.health -= 10
            if self.health == 0:
                raise RobotCrashError('Robot is destroyed')
            self.move_forward()
            self.backward_detour()

    def backward_detour(self):
        if (self.direction == 'N' and self.x != 0) or \
                (self.direction == 'E' and self.y != self.asteroid.y) or \
                (self.direction == 'S' and self.x != self.asteroid.x) or \
                (self.direction == 'W' and self.y != 0):
            self.turn_right()
            self.move_backward()
            self.turn_left()
            for _ in range(2):
                self.move_backward()
            self.turn_left()
            self.move_backward()
            self.turn_right()
        else:
            self.turn_left()
            self.move_backward()
            self.turn_right()
            for _ in range(2):
                self.move_backward()
            self.turn_right()
            self.move_backward()
            self.turn_left()

    def self_destroy(self):
        del self
        try:
            self
        except NameError:
            raise RobotCrashError


class Obstacle:
    def __init__(self, x, y, asteroid):
        self.x = x
        self.y = y
        self.asteroid = asteroid
        if self.x > self.asteroid.x or self.y > self.asteroid.y or self.x < 0 or self.y < 0:
            raise MissAsteroidError()


class MissAsteroidError(Exception):
    pass


class RobotCrashError(Exception):
    pass


class ObstacleCrashError(Exception):
    pass


class LowBatteryError(Exception):
    pass
