from subprocess import Popen

Popen(['gnome-terminal', '-e', "python secondary_hybrid.py"])
Popen(['gnome-terminal', '-e', "python API_Frontend.py"])
Popen(['gnome-terminal', '-e', "python WebFrontend.py"])
