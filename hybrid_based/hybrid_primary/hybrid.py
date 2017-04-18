from subprocess import Popen

Popen(['gnome-terminal', '-e', "python primary_hybrid.py"])
Popen(['gnome-terminal', '-e', "python API_Frontend.py"])
Popen(['gnome-terminal', '-e', "python WebFrontend.py"])
