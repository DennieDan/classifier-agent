"""Run the NiceGUI interface. Use from project root: python run_ui.py"""

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
_APP = os.path.join(_ROOT, "app")
sys.path.insert(0, _APP)
os.chdir(_APP)

from app.ui import run_ui

if __name__ == "__main__":
    run_ui()
