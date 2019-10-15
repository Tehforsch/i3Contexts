import os

def i3SwitchWorkspace(workspace):
    os.system("i3-msg workspace {}".format(workspace.name))

def i3MoveWindow(workspace):
    os.system("i3-msg move workspace {}".format(workspace.name))

def i3ChangeOutput(output):
    os.system("i3-msg move workspace to output {}".format(output))

def switchOrMove(targetWorkspace, move):
    if move:
        i3MoveWindow(targetWorkspace)
    i3Utils.i3SwitchWorkspace(targetWorkspace)

