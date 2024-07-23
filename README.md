# Phonk Racer Game

Video Demo: https://www.youtube.com/watch?v=HvriozEamuo

This is a racing game of the “dodge oncoming cars” type.

TODO:
1) Add current score indication and difficulty system.
2) Add top score dashboard.
3) Draw and upload more assets.

## Features

- Player-controlled car with keyboard navigation.
- Enemy cars with random positions and speeds.
- Dynamic objects such as trees and pavement cracks.
- Continuous background music.
- Game over screen with score display and restart option.

## Installation

### Prerequisites

- Pygame

### Install Pygame

You can install Pygame using pip:

```sh
pip install pygame
```

### Clone repository

```sh
git clone https://github.com/ashlndr/phonk_racer.git
cd phonk_racer
```

## Usage

To start the game, simply run the project.py script:
```sh
python project.py
```

## Game Controls

- **Left Arrow / A**: Move the car to the left.
- **Right Arrow / D**: Move the car to the right.
- **R**: Restart the game after a game over.

## Code Structure

### `MovableObject` Class

A base class for all objects that can move on the screen.

**Attributes:**
- `x` (int): X coordinate.
- `y` (int): Y coordinate.
- `speed` (int): Speed of the object.

**Methods:**
- `draw(screen)`: Draws the object on the screen.
- `move()`: Updates the object's position.

### `Car` Class

Inherits from `MovableObject`, represents a car in the game.

**Attributes:**
- `color` (str): Color of the car.
- `rotate` (bool): If `True`, rotates the car image for enemy cars.

### `RoadObjects` Class

Inherits from `MovableObject`, represents objects on the road such as trees and pavement cracks.

**Attributes:**
- `obj_img` (Surface): Image of the object.

**Methods:**
- `respawn(x_range, y_range)`: Respawns the object at a new position.

### `Game` Class

Main class to run the game.

**Attributes:**
- `screen` (Surface): Game screen.
- `clock` (Clock): Game clock.
- `road_img` (Surface): Background road image.
- `player_car` (Car): The player's car.
- `enemy_cars` (list of Car): List of enemy cars.
- `trees` (list of RoadObjects): List of trees.
- `cracks` (list of RoadObjects): List of pavement cracks.
- `score` (int): Current score.
- `fps` (int): Frames per second.
- `running` (bool): Game loop control.
- `game_over` (bool): Game over state.

**Methods:**
- `play()`: Starts the game loop.
- `handle_events()`: Handles game events.
- `reset_game()`: Resets the game state.
- `update()`: Updates game objects.
- `draw()`: Draws game objects on the screen.
- `handle_game_over()`: Handles the game over state.
- `generate_trees()`: Generates trees.
- `generate_cracks()`: Generates pavement cracks.
- `generate_enemy_cars()`: Generates enemy cars.
- `update_objects()`: Updates the positions of all objects.

### Helper Functions

- `generate_car_random_x(enemy_cars)`: Generates a random, non-overlapping X coordinate for a car.
- `get_random_asset(assets_dir)`: Returns a random asset from a given directory.
- `cars_collided(player_car, enemy_car)`: Checks if two cars have collided.
- `steer(player_car)`: Handles the car's steering.
