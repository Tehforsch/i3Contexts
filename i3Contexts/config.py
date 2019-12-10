from pathlib import Path
import os
import yaml
import string
from math import ceil

def readConfigFile(configFile):
    with configFile.open("r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        return config

configFile = Path(os.path.expanduser("~"), ".i3Context")

config = readConfigFile(configFile)

contextNames = config.get("contextNames", list(string.ascii_lowercase))
workspaceNames = config.get("workspaceNames", [str(x) for x in range(100)])
sharedWorkspaceNames = config.get("sharedWorkspaceNames", [])
outputMap = config.get("outputMap", {})
defaultWorkspaceOnNewContext = config.get("defaultWorkspaceOnNewContext", workspaceNames[0])

sharedContext = -1

workspacesPerContext = len(workspaceNames)
workspaceNameFormat = "{workspaceId}:{contextName}{workspaceName}"
sharedWorkspaceNameFormat = "{workspaceId}:{workspaceName}"

numSharedWorkspaces = len(sharedWorkspaceNames)
offsetPerContext = workspacesPerContext
minContextOffset = ceil(numSharedWorkspaces / offsetPerContext) * offsetPerContext
