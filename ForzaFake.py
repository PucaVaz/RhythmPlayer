import time

def get_speed():
    for i in reversed(range(0, 101, 5)):
        time.sleep(2)
        yield i

