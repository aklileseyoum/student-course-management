"""Reusable Functions"""

import os

def wipe():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

