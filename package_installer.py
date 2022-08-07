# This program installs packages, which are listed in
# requirements.txt file. Be careful with outdated packages 
# and packages, that aren't recommended to be upgraded

import os
os.system("pip freeze > requirements.txt")      # Creates Requirements.txt file
os.system("pip install -r requirements.txt")    # Installs all packeges from requirements list
os.system("pip list --outdated")                # Check if there are any outdated packages