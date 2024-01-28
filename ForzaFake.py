import time
import random

def get_speed():
    random_speed = 0

    while True:
        random_speed = random.randint(0, 130)
        return random_speed

