import os
import platform

global pVar
global directory
global destination
global path

def get_directory():
    global directory
    directory = os.path.dirname(os.path.realpath(__file__))
    global pVar
    if platform.system() == "Windows":
        pVar = "\\"
    if platform.system() == "Linux":
            pVar = "/"
    else:
        pVar = "\\"
    return directory
