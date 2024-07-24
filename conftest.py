import pytest

from project import Car


@pytest.fixture
def player_car():
    return Car(100, 100, speed=0, color='red.png')
