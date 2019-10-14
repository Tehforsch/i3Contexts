from pathlib import Path
import os

# Custom settings
contextNames = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
}
sharedWorkspaceNames = ["chat", "music", "todo", "mail"]
# Maximum number of workspaces available for use 
workspacesPerContext = 100

contextFile = Path(os.path.expanduser("~"), ".context")
