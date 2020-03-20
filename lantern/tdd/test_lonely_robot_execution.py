from lonely_robot import Robot, Asteroid


class TestRobotCreation:
    def test_parameters(self):
        x, y = 10, 15
        asteroid = Asteroid(x, y)
        robot = Robot(x, y, asteroid)
        assert robot.x == 10
        assert robot.y == 15
        assert robot.asteroid == asteroid
