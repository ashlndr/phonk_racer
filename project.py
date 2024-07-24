import os
import random
from typing import Optional, Tuple

import pygame

from constants import *


class MovableObject:
    """Base class for a movable game object.
    :param x: x coordinate of an object.
    :param y: y coordinate of an object.
    :param speed: value, by which object y coordinate will be changing.
    """

    def __init__(self, x: int, y: int, speed: int) -> None:
        self.obj = None
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self, screen: pygame.surface.Surface) -> None:
        """Draw an object at the current position on a screen.
        :param screen: an object of game screen.
        :type screen: Surface type, a pygame object for representing images.
        """
        screen.blit(self.obj, (self.x, self.y))

    def move(self) -> None:
        """Change position of an object by incrementing y coordinate by its speed."""
        self.y += self.speed


class Car(MovableObject):
    """Class representing a moving car object.
    :param x: x coordinated of a car.
    :param y: y coordinate of a car.
    :param color: name of a car color asset.
    :param speed: car speed.
    :param rotate: indicates if a car image should be rotated by 180 degrees for enemy cars.
    """

    def __init__(self, x: int, y: int, color: str, speed=0, rotate=False) -> None:
        super().__init__(x, y, speed)
        self.skin = pygame.image.load(os.path.join(CAR_SKINS_DIR, color))
        if rotate:
            self.skin = pygame.transform.rotate(self.skin, 180)
        self.obj = pygame.transform.scale(self.skin, CAR_SIZE)


class RoadObjects(MovableObject):
    """Class for representing moving objects along the road, such as trees and pavement cracks.
    :param x: x coordinate of an object.
    :param y: y coordinate of an object.
    :param obj_img: loaded image of an object.
    :type obj_img: Surface type, a pygame object for representing images.
    :param speed: value, by which object y coordinate will be changing.
    """

    def __init__(self, x: int, y: int, obj_img: pygame.surface.Surface, speed=OBJ_SPEED) -> None:
        super().__init__(x, y, speed)
        self.obj_img = obj_img
        self.obj = pygame.transform.scale(self.obj_img, OBJ_SIZE)

    def respawn(
        self,
        x_range: Optional[Tuple[int, int, int]],
        y_range: Optional[Tuple[int, int, int]],
    ) -> None:
        """Renew object coordinates.
        :param x_range: a tuple with start, stop and step values for x random.randrange.
        :param y_range: a tuple with start, stop and step values for y random.randrange.
        """
        if x_range:
            self.x = random.randrange(*x_range)
        if y_range:
            self.y = random.randrange(*y_range)


class Game:
    """Main class for running game."""

    def __init__(self) -> None:
        """Initialize all game assets and objects."""
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(SOUNDS_DIR, "soundtrack.mp3"))
        pygame.mixer.music.play(loops=-1, fade_ms=200)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.road_img = pygame.image.load(os.path.join(ROAD_SKINS_DIR, "road.png"))
        self.player_car = Car(
            SCREEN_WIDTH // 2 - CAR_WIDTH // 2,
            SCREEN_HEIGHT - 2 * CAR_HEIGHT,
            PLAYER_CAR,
        )
        self.enemy_cars = []
        self.trees = []
        self.cracks = []
        self.score = 0
        self.fps = 60
        self.running = True
        self.game_over = False

    def play(self) -> None:
        """Play game."""
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()
                self.draw()
            else:
                self.handle_game_over()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

    def handle_events(self) -> None:
        """Handle events occurred during game session."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()

    def reset_game(self) -> None:
        """Reset score and cars at initial values."""
        self.player_car = Car(
            SCREEN_WIDTH // 2 - CAR_WIDTH // 2,
            SCREEN_HEIGHT - 2 * CAR_HEIGHT,
            PLAYER_CAR,
        )
        self.enemy_cars = []
        self.score = 0
        self.game_over = False

    def update(self) -> None:
        """Generate and update objects on screen."""
        self.generate_enemy_cars()
        self.generate_trees()
        self.generate_cracks()
        self.update_objects()

    def draw(self) -> None:
        """Draw game objects, such as cars, trees and pavement cracks on screen."""
        self.screen.blit(pygame.transform.scale(self.road_img, SCREEN_SIZE), (0, 0))
        for tree in self.trees:
            tree.draw(self.screen)
        for crack in self.cracks:
            crack.draw(self.screen)
        self.player_car.draw(self.screen)
        for enemy_car in self.enemy_cars:
            enemy_car.draw(self.screen)

    def handle_game_over(self) -> None:
        """Paint game over text with current score in case of cars collision."""
        game_over_font = pygame.font.SysFont(GAME_OVER_FONT, 60)
        game_over_text = game_over_font.render(f"GAME OVER: {self.score}", True, WHITE_COLOR)
        game_over_rect = game_over_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(game_over_text, game_over_rect)
        restart_font = pygame.font.SysFont(GAME_OVER_FONT, 40)
        restart_text = restart_font.render("Press R to restart", True, WHITE_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def generate_trees(self) -> None:
        """Populate a list of trees to paint on screen."""
        while len(self.trees) < N_TREES * 2:
            obj_img = pygame.image.load(os.path.join(TREES_DIR, "tree.png"))
            rand_x_range = (0, random.randrange(-100, SCREEN_HEIGHT, 2 * OBJ_HEIGHT))
            rand_y_rang = (
                SCREEN_WIDTH - 50,
                random.randrange(-100, SCREEN_HEIGHT, 2 * OBJ_HEIGHT),
            )
            positions = [rand_x_range, rand_y_rang]
            for pos in positions:
                self.trees.append(RoadObjects(pos[0], pos[1], obj_img))

    def generate_cracks(self) -> None:
        """Populate a list of pavement cracks to paint on screen."""
        while len(self.cracks) < N_CRACKS:
            obj_img = pygame.image.load(get_random_asset(CRACKS_SKINS_DIR))
            rand_x = random.randrange(40, 400, 20)
            rand_y = random.randrange(-100, SCREEN_HEIGHT, 2 * OBJ_HEIGHT)
            self.cracks.append(RoadObjects(rand_x, rand_y, obj_img))

    def generate_enemy_cars(self) -> None:
        """Populate a list of enemy cars to paint on screen."""
        while len(self.enemy_cars) < N_CARS:
            x = generate_car_random_x(self.enemy_cars)
            speed = random.randint(6, 10)
            enemy_car = Car(x, -100, get_random_asset(CAR_SKINS_DIR), speed, rotate=True)
            enemy_car.obj = pygame.transform.scale(enemy_car.skin, CAR_SIZE)
            self.enemy_cars.append(enemy_car)

    def update_objects(self) -> None:
        """Move road object on screen. Respawn them if they move outside of screen."""
        for tree in self.trees:
            tree.move()
            if tree.y > SCREEN_HEIGHT:
                tree.respawn(x_range=None, y_range=(-100, -40, 10))

        for crack in self.cracks:
            crack.move()
            if crack.y > SCREEN_HEIGHT:
                crack.respawn(x_range=(40, 400, 20), y_range=(-100, -10, 20))
                crack.obj = pygame.transform.scale(pygame.image.load(get_random_asset(CRACKS_SKINS_DIR)), OBJ_SIZE)

        for enemy_car in self.enemy_cars:
            enemy_car.move()
            if cars_collided(self.player_car, enemy_car):
                self.game_over = True
            elif enemy_car.y > SCREEN_HEIGHT:
                enemy_car.x = generate_car_random_x(self.enemy_cars)
                enemy_car.y = -100
                enemy_car.speed = random.randint(6, 10)
                enemy_car.skin = pygame.transform.rotate(pygame.image.load(get_random_asset(CAR_SKINS_DIR)), 180)
                enemy_car.obj = pygame.transform.scale(enemy_car.skin, CAR_SIZE)
                self.score += 1

        steer(self.player_car)


def generate_car_random_x(enemy_cars: list[Car]) -> int:
    """Return a random, unique x coordinate for car. Uniqueness is necessary to avoid images overlapping.
    :param enemy_cars: list of Car objects.
    """
    available_positions = list(range(round(CAR_WIDTH / 2), SCREEN_WIDTH - round(1.5 * CAR_WIDTH), CAR_WIDTH))
    random.shuffle(available_positions)
    for x in available_positions:
        if all(abs(car.x - x) >= CAR_WIDTH for car in enemy_cars):
            return x


def get_random_asset(assets_dir: str) -> str:
    """Return a random asset from a given directory."""
    return os.path.join(assets_dir, random.choice(os.listdir(assets_dir)))


def cars_collided(player_car: Car, enemy_car: Car) -> bool:
    """Check for cars collision.
    :param player_car: Car object.
    :param enemy_car: Car object.
    """
    min_y = player_car.y - CAR_HEIGHT
    max_y = player_car.y + CAR_HEIGHT
    return min_y <= enemy_car.y <= max_y and abs(enemy_car.x - player_car.x) <= CAR_WIDTH / 2


def steer(player_car: Car) -> None:
    """Navigate a car by changing its x coordinate.
    :param player_car: Car object.
    """
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_car.x - CAR_WIDTH / 2 > 0:
        player_car.x -= PLAYER_SPEED
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_car.x + CAR_WIDTH * 1.5 < SCREEN_WIDTH:
        player_car.x += PLAYER_SPEED


def main() -> None:
    Game().play()


if __name__ == "__main__":
    main()
