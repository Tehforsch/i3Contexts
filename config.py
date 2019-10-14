from pathlib import Path
import os
import yaml

contextFile = Path(os.path.expanduser("~"), ".context")
configFile = Path(os.path.expanduser("~"), ".i3Context")

def readConfigFile():
    with configFile.open("r") as f:
        config = yaml.unsafe_load(f)
        return config

config = readConfigFile()
sharedWorkspaceNames = config["sharedWorkspaceNames"]
workspacesPerContext = config["workspacesPerContext"]
contextNames = config["contextNames"]
outputMap = config["outputMap"]
