import os

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 700
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
TITLE = "Phonk Racer"
OBJ_WIDTH, OBJ_HEIGHT = 50, 50
OBJ_SIZE = (OBJ_WIDTH, OBJ_HEIGHT)
CAR_WIDTH, CAR_HEIGHT = 70, 80
CAR_SIZE = (CAR_WIDTH, CAR_HEIGHT)
PLAYER_SPEED = 6
OBJ_SPEED = 5
CRACKS_SPEED = 5
N_CARS = 4
N_TREES = 4
N_CRACKS = 3
ASSETS = os.path.join(os.path.dirname(__file__), "assets")
CAR_SKINS_DIR = os.path.join(ASSETS, "cars")
ROAD_SKINS_DIR = os.path.join(ASSETS, "road")
CRACKS_SKINS_DIR = os.path.join(ASSETS, "cracks")
SOUNDS_DIR = os.path.join(ASSETS, "sounds")
TREES_DIR = os.path.join(ASSETS, "trees")
PLAYER_CAR = "red.png"
WHITE_COLOR = (255, 255, 255)
GAME_OVER_FONT = "papyrus"
ROAD_CHANGE_INTERVAL = 500
