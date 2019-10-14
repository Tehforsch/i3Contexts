from pathlib import Path
import os
import yaml
import string

contextFile = Path(os.path.expanduser("~"), ".context")
configFile = Path(os.path.expanduser("~"), ".i3Context")

def makeSureContextFileExists():
    if not contextFile.is_file():
        with contextFile.open("w") as f:
            f.write("0")

def readConfigFile():
    with configFile.open("r") as f:
        config = yaml.unsafe_load(f)
        return config

config = readConfigFile()
contextNames = config.get("contextNames", list(string.ascii_lowercase))
sharedWorkspaceNames = config.get("sharedWorkspaceNames", [])
workspacesPerContext = config.get("workspacesPerContext", 100)
outputMap = config.get("outputMap", {})
doublePressToNonEmpty = config.get("doublePressToNonEmpty", False)
makeSureContextFileExists()
