import numpy as np
import mss

_sct = mss.mss()


def capture_screen(region=None):
    if region:
        monitor = region
    else:
        monitor = _sct.monitors[1]  # Ana monitör

    screenshot = _sct.grab(monitor)
    return np.array(screenshot)[:, :, :3]  # BGRA -> BGR
