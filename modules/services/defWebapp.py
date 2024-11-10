import os

import modules.globalVariables as gVar

# Create default index.json use this shit
def create_index_file(path: str):
    default_index = """{
        "Man!": {
            "What can i say!": "Mamba, Out!"
        }
    }"""
    filename = os.path.join(path, "index.json")
    print(filename)
    with open(filename, 'w') as configfile:
        configfile.write(default_index)

class WebApp:
    def __init__(self):
        self._webDir = gVar.webDir

        # If web this folder not exist, it will create this folder
        if not os.path.exists(self._webDir):
            os.makedirs(self._webDir)
            create_index_file(self._webDir)