from ilkinoapps.ilkino import Ilkino
import sys


if __name__ == "__main__":
    ilkino = Ilkino(sys.argv)
    ilkino.setup()
    ilkino.run()
