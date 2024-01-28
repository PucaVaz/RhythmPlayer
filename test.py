from ForzaFake import get_speed
from ForzaData import get_speed_data
import time

while True:
    print("Testando, fake: ")
    print(get_speed())
    print("Testando, real: ")
    print(get_speed_data())
    print("tipo real, ", type(get_speed_data()))
    time.sleep(1)


