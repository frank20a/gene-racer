from scripts.engine import Engine
import os
import numpy as np


if __name__ == "__main__":
    # Export environmental variables
    os.environ['GAME_DIR'] = os.getcwd()
    os.environ['ANG_VEL'] = "3"
    os.environ['LIN_VEL'] = "4"

    # Create app and run it
    Engine("track").mainloop()