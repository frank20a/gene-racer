from scripts.engine import Engine
import os
import numpy as np


if __name__ == "__main__":
    # Export environmental variables
    os.environ['GAME_DIR'] = os.getcwd()
    os.environ['ANG_VEL'] = "2"
    os.environ['ANG_ACC'] = "0.07"
    os.environ['ANG_DEC'] = "0.05"
    os.environ['LIN_VEL'] = "5"
    os.environ['LIN_ACC'] = "0.1"
    os.environ['LIN_DEC'] = "0.08"

    # Create app and run it
    Engine("track", player='computer', n_cars=10).mainloop()