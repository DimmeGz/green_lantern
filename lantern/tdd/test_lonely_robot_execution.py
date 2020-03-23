import pytest
from lonely_robot import Robot, Asteroid, MissAsteroidError, RobotCrashError, \
    Obstacle, ObstacleCrashError, LowBatteryError


class TestRobotCreation:

    def setup(self):
        self.asteroid = Asteroid(15, 15)
        self.obstacle = Obstacle(10, 10, self.asteroid)

    def test_parameters(self):
        x, y = 10, 15
        direction = 'E'
        robot = Robot(x, y, self.asteroid, direction, self.obstacle)
        assert robot.x == 10
        assert robot.y == 15
        assert robot.direction == direction
        assert robot.asteroid == self.asteroid
        assert robot.obstacle == self.obstacle

    @pytest.mark.parametrize(
        "robot_coordinates",
        (
                (26, 30),
                (26, 24),
                (15, 27),
        )
    )
    def test_check_if_robot_on_asteroid(self, robot_coordinates):
        with pytest.raises(MissAsteroidError):
            Robot(*robot_coordinates, self.asteroid, 'W', self.obstacle)

    @pytest.mark.parametrize(
        "robot_coordinates,obstacle_coordinates",
        (
                ((5, 8), (5, 8)),
                ((9, 12), (9, 12)),
        )
    )
    def test_check_if_robot_on_obstacle(self, robot_coordinates, obstacle_coordinates):
        with pytest.raises(ObstacleCrashError):
            obstacle = Obstacle(*obstacle_coordinates, self.asteroid)
            Robot(*robot_coordinates, self.asteroid, 'W', obstacle)

    def test_self_destroy(self):
        with pytest.raises(RobotCrashError):
            asteroid = Asteroid(15, 20)
            obstacle = Obstacle(10, 10, asteroid)
            robot = Robot(5, 5, asteroid, 'W', obstacle)
            robot.self_destroy()


class TestMovement:

    def setup(self):
        self.x = 10
        self.y = 15
        self.asteroid = Asteroid(self.x, self.y)
        self.obstacle = Obstacle(8, 8, self.asteroid)

    @pytest.mark.parametrize(
        "current_direction,expected_direction",
        (
                ('E', 'N'),
                ('N', 'W'),
                ('W', 'S'),
                ('S', 'E')
        )
    )
    def test_turn_left(self, current_direction, expected_direction):
        robot = Robot(5, 10, self.asteroid, current_direction, self.obstacle)
        robot.turn_left()
        assert robot.direction == expected_direction

    @pytest.mark.parametrize(
        "current_direction,expected_direction",
        (
                ('E', 'S'),
                ('S', 'W'),
                ('W', 'N'),
                ('N', 'E')
        )
    )
    def test_turn_right(self, current_direction, expected_direction):
        robot = Robot(5, 10, self.asteroid, current_direction, self.obstacle)
        robot.turn_right()
        assert robot.direction == expected_direction

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,expected_coordinates",
        (
                ('E', (5, 5), (6, 5)),
                ('W', (5, 5), (4, 5)),
                ('N', (5, 5), (5, 6)),
                ('S', (5, 5), (5, 4))
        )
    )
    def test_move_forward(self, current_direction, robot_coordinates, expected_coordinates):
        robot = Robot(*robot_coordinates, self.asteroid, current_direction, self.obstacle)
        robot.move_forward()
        assert (robot.x, robot.y) == expected_coordinates

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,expected_coordinates",
        (
                ('E', (0, 0), (2, 0)),
                ('W', (10, 15), (8, 15)),
                ('N', (0, 0), (0, 2)),
                ('S', (10, 15), (10, 13))
        )
    )
    def test_forward_detour(self, current_direction, robot_coordinates, expected_coordinates):
        robot = Robot(*robot_coordinates, self.asteroid, current_direction, self.obstacle)
        robot.forward_detour()
        assert (robot.x, robot.y) == expected_coordinates

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,expected_coordinates",
        (
                ('E', (10, 15), (8, 15)),
                ('W', (0, 0), (2, 0)),
                ('N', (10, 15), (10, 13)),
                ('S', (0, 0), (0, 2))
        )
    )
    def test_backward_detour(self, current_direction, robot_coordinates, expected_coordinates):
        robot = Robot(*robot_coordinates, self.asteroid, current_direction, self.obstacle)
        robot.backward_detour()
        assert (robot.x, robot.y) == expected_coordinates

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,expected_coordinates",
        (
                ('E', (5, 5), (4, 5)),
                ('W', (5, 5), (6, 5)),
                ('N', (5, 5), (5, 4)),
                ('S', (5, 5), (5, 6))
        )
    )
    def test_move_backward(self, current_direction, robot_coordinates, expected_coordinates):
        robot = Robot(*robot_coordinates, self.asteroid, current_direction, self.obstacle)
        robot.move_backward()
        assert (robot.x, robot.y) == expected_coordinates

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,asteroid_size",
        (
                ('W', (0, 5), (10, 10)),
                ('E', (10, 5), (10, 10)),
                ('N', (5, 10), (10, 10)),
                ('S', (5, 0), (10, 10))
        )
    )
    def test_robot_fall_forward(self, current_direction, robot_coordinates, asteroid_size):
        with pytest.raises(RobotCrashError):
            asteroid = Asteroid(*asteroid_size)
            robot = Robot(*robot_coordinates, asteroid, *current_direction, self.obstacle)
            robot.move_forward()

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,asteroid_size",
        (
                ('W', (10, 5), (10, 10)),
                ('E', (0, 5), (10, 10)),
                ('N', (5, 0), (10, 10)),
                ('S', (5, 10), (10, 10))
        )
    )
    def test_robot_fall_backward(self, current_direction, robot_coordinates, asteroid_size):
        with pytest.raises(RobotCrashError):
            asteroid = Asteroid(*asteroid_size)
            robot = Robot(*robot_coordinates, asteroid, *current_direction, self.obstacle)
            robot.move_backward()

    def test_robot_battery_empty(self):
        with pytest.raises(LowBatteryError):
            robot = Robot(4, 4, self.asteroid, 'W', self.obstacle)
            robot.battery -= 100
            robot.battery_check()

    def test_battery_level(self):
        robot = Robot(4, 4, self.asteroid, 'W', self.obstacle)
        for _ in range(33):
            robot.move_forward()
            robot.turn_right()
            robot.turn_right()
        assert robot.battery == 1

    def test_robot_battery_empty_by_moving(self):
        with pytest.raises(LowBatteryError):
            robot = Robot(4, 4, self.asteroid, 'W', self.obstacle)
            for _ in range(50):
                robot.move_forward()
                robot.move_backward()


class TestObstacleCreation:
    def test_parameters(self):
        x, y = 10, 15
        asteroid = Asteroid(x, y)
        obstacle = Obstacle(x, y, asteroid)
        assert obstacle.x == 10
        assert obstacle.y == 15
        assert obstacle.asteroid == asteroid

    @pytest.mark.parametrize(
        "asteroid_size,obstacle_coordinates",
        (
                ((15, 25), (26, 30)),
                ((15, 25), (26, 24)),
                ((15, 25), (15, 27)),
        )
    )
    def test_check_if_obstacle_on_asteroid(self, asteroid_size, obstacle_coordinates):
        with pytest.raises(MissAsteroidError):
            asteroid = Asteroid(*asteroid_size)
            Obstacle(*obstacle_coordinates, asteroid)


class TestObstaclesMovement:

    def setup(self):
        self.asteroid = Asteroid(20, 20)
        self.obstacle = Obstacle(10, 10, self.asteroid)

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,expected_coordinates",
        (
                ('W', (11, 10), (9, 10)),
                ('E', (9, 10), (11, 10)),
                ('N', (10, 9), (10, 11)),
                ('S', (10, 11), (10, 9))
        )
    )
    def test_robot_forward_obstacle_movement(self, current_direction, robot_coordinates,
                                             expected_coordinates):
        robot = Robot(*robot_coordinates, self.asteroid, current_direction, self.obstacle)
        robot.move_forward()
        assert (robot.x, robot.y) == expected_coordinates and robot.direction == current_direction

    @pytest.mark.parametrize(
        "current_direction,robot_coordinates,expected_coordinates",
        (
                ('W', (9, 10), (11, 10)),
                ('E', (11, 10), (9, 10)),
                ('N', (10, 11), (10, 9)),
                ('S', (10, 9), (10, 11))
        )
    )
    def test_robot_backward_obstacle_movement(self, current_direction, robot_coordinates,
                                              expected_coordinates):
        robot = Robot(*robot_coordinates, self.asteroid, current_direction, self.obstacle)
        robot.move_backward()
        assert (robot.x, robot.y) == expected_coordinates and robot.direction == current_direction

    def test_robot_destroy_forward(self):
        with pytest.raises(RobotCrashError):
            robot = Robot(9, 10, self.asteroid, 'E', self.obstacle)
            for _ in range(5):
                robot.move_forward()
                robot.move_backward()
