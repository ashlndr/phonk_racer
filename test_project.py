import os
from unittest.mock import patch

import pygame
import pytest

from constants import CAR_WIDTH, PLAYER_SPEED
from project import Car, cars_collided, generate_car_random_x, get_random_asset, steer


@pytest.mark.parametrize(
    ["x1", "x2", "color1", "color2"],
    [
        (50, 100, "blue.png", "red.png"),
        (100, 150, "green.png", "white.png"),
        (200, 250, "yellow.png", "green.png"),
    ],
)
def test_generate_car_random_x(x1, x2, color1, color2):
    car1 = Car(x1, 0, speed=0, color=color1)
    car2 = Car(x2, 0, speed=0, color=color2)
    enemy_cars = [car1, car2]
    x = generate_car_random_x(enemy_cars)
    assert all(abs(car.x - x) >= CAR_WIDTH for car in enemy_cars)


@patch("project.os.listdir")
def test_get_random_asset(mock_listdir):
    mock_listdir.return_value = ["asset1.png", "asset2.png", "asset3.png"]
    assets_dir = "/path/to/assets"
    asset = get_random_asset(assets_dir)
    assert asset in [
        os.path.join(assets_dir, "asset1.png"),
        os.path.join(assets_dir, "asset2.png"),
        os.path.join(assets_dir, "asset3.png"),
    ]


def test_cars_collided(player_car):
    enemy_car = Car(100, 150, speed=0, color="white.png")
    assert cars_collided(player_car, enemy_car)


def test_cars_not_collided(player_car):
    enemy_car = Car(300, 100, speed=0, color="orange.png")
    assert not cars_collided(player_car, enemy_car)


@patch("pygame.key.get_pressed")
def test_steer_no_key(mock_get_pressed, player_car):
    mock_get_pressed.return_value = {
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False,
        pygame.K_a: False,
        pygame.K_d: False,
    }
    steer(player_car)
    assert player_car.x == 100
    assert player_car.y == 100


@patch("pygame.key.get_pressed")
def test_steer_left_key(mock_get_pressed, player_car):
    mock_get_pressed.return_value = {
        pygame.K_LEFT: True,
        pygame.K_RIGHT: False,
        pygame.K_a: False,
        pygame.K_d: False,
    }
    steer(player_car)
    assert player_car.x == 100 - PLAYER_SPEED
    assert player_car.y == 100


@patch("pygame.key.get_pressed")
def test_steer_right_key(mock_get_pressed, player_car):
    mock_get_pressed.return_value = {
        pygame.K_LEFT: False,
        pygame.K_RIGHT: True,
        pygame.K_a: False,
        pygame.K_d: False,
    }
    steer(player_car)
    assert player_car.x == 100 + PLAYER_SPEED
    assert player_car.y == 100


@patch("pygame.key.get_pressed")
def test_steer_a_key(mock_get_pressed, player_car):
    mock_get_pressed.return_value = {
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False,
        pygame.K_a: True,
        pygame.K_d: False,
    }
    steer(player_car)
    assert player_car.x == 100 - PLAYER_SPEED
    assert player_car.y == 100


@patch("pygame.key.get_pressed")
def test_steer_d_key(mock_get_pressed, player_car):
    mock_get_pressed.return_value = {
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False,
        pygame.K_a: False,
        pygame.K_d: True,
    }
    steer(player_car)
    assert player_car.x == 100 + PLAYER_SPEED
    assert player_car.y == 100


@patch("pygame.key.get_pressed")
def test_steer_unexpected_key(mock_get_pressed):
    with pytest.raises(KeyError):
        mock_get_pressed.return_value = {pygame.K_UP: True}
        player_car = Car(50, 70, speed=0, color="red.png")
        steer(player_car)
