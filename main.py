"""
main.py - Entry point for the Minesweeper AI application.
Author: Group Students (CO3061) - HCMUT
Course: Introduction to Artificial Intelligence (CO3061) - HCMUT
"""

import sys
import os

# Add src directory to python module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import tkinter as tk
from gui import MinesweeperGUI


def main():
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
