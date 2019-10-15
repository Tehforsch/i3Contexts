from pathlib import Path
import os
import yaml
import string
from math import ceil

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
workspacesPerContext = config.get("workspacesPerContext", 100)
sharedWorkspaceNames = config.get("sharedWorkspaceNames", [])
workspaceNames = config.get("workspaceNames", ["non"+str(x) for x in range(workspacesPerContext)])
outputMap = config.get("outputMap", {})
doublePressToNonEmpty = config.get("doublePressToNonEmpty", False)
lowestWorkspaceNumber = config.get("lowestWorkspaceNumber", 2)
defaultWorkspaceOnNewContext = config.get("defaultWorkspaceOnNewContext", workspaceNames[0])

makeSureContextFileExists()
SHARED_CONTEXT = -1

workspaceNameFormat = "{workspaceId}:{contextName}{workspaceName}"
sharedWorkspaceNameFormat = "{workspaceId}:{workspaceName}"

numSharedWorkspaces = len(sharedWorkspaceNames)
offsetPerContext = workspacesPerContext
minContextOffset = ceil(numSharedWorkspaces / offsetPerContext) * offsetPerContext

