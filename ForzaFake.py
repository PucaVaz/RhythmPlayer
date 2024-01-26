from os import times


def main():
    for i in range(0, 101, 5):
        times.sleep(2)
        yield i
    
if __name__ == "__main__":
    main()