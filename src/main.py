from userInterface import userInterface
import time

def main():
    userInterface.displayLogo()
    print("test")
    time.sleep(3)
    userInterface.clearScreen()

if __name__ == '__main__':
    main()