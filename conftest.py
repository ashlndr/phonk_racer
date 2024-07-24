import pytest

from project import Car


@pytest.fixture
def player_car():
    """Fixture for returning a default player car object."""
    return Car(100, 100, speed=0, color="red.png")
