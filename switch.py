import argparse
import os
from math import ceil
import i3
from config import *
import watchContext

workspaceNameFormat = "{workspaceId}:{contextName}{workspaceNumber}"
sharedWorkspaceNameFormat = "{workspaceId}:{workspaceName}"

numSharedWorkspaces = len(sharedWorkspaceNames)
offsetPerContext = workspacesPerContext
minContextOffset = ceil(numSharedWorkspaces / offsetPerContext) * offsetPerContext

SHARED_CONTEXT = -1

class Context:
    def __init__(self, id_):
        self.id_ = id_

    @property
    def shared(self):
        return self.id_ == SHARED_CONTEXT

    @property
    def name(self):
        if self.shared:
            return "Shared"
        return contextNames[self.id_]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.id_ == other.id_

class Workspace:
    def __init__(self, id_):
        self.id_ = id_

    def __eq__(self, other):
        if self.id_ == other.id_:
            assert self.name == other.name
        return self.id_ == other.id_
    @property
    def contextNumber(self):
        return (self.id_ - minContextOffset) // offsetPerContext

    @property
    def context(self):
        return Context(self.contextNumber)

    @property
    def number(self):
        return self.id_ - self.contextNumber * offsetPerContext - minContextOffset

    @property
    def isOpenAlready(self):
        return any(ws["name"] == self.name for ws in i3.get_workspaces())

    @staticmethod
    def fromNumbers(contextId, workspaceNumber):
        return Workspace(minContextOffset + offsetPerContext * contextId + workspaceNumber)

    @staticmethod
    def fromFocus():
        workspaces = i3.get_workspaces()
        for ws in workspaces:
            if ws["focused"] == True:
                return Workspace.fromI3Workspace(ws)

    @staticmethod
    def fromI3Workspace(i3workspace):
        if i3workspace["name"] in sharedWorkspaceNames:
            return Workspace.fromSharedName(i3workspace["name"])
        else:
            return Workspace(i3workspace["num"])

    @staticmethod
    def fromSharedName(name):
        if ":" in name:
            id_, rawName = name.split(":")
            return Workspace(sharedWorkspaceNames.index(rawName))
        else:
            return Workspace(sharedWorkspaceNames.index(name))

    @staticmethod
    def fromFirstNonEmptyOnSameContext(source):
        for i3workspace in sorted(i3.get_workspaces(), key = lambda ws: ws["num"]):
            workspace = Workspace.fromI3Workspace(i3workspace)
            if workspace.context == source.context:
                return workspace
        return source

    @property
    def rawName(self):
        if self.context.shared:
            return self.name.split(":")[1]
        else:
            return self.number

    @property
    def name(self):
        if self.context.shared:
            return sharedWorkspaceNameFormat.format(workspaceId=self.id_, workspaceName=sharedWorkspaceNames[self.id_])
        return workspaceNameFormat.format(workspaceId=self.id_, contextName=self.context.name, workspaceNumber=self.number)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

def maybeInt(x):
    try:
        return int(x)
    except ValueError:
        return x

def setupArgs():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('type', type=str, choices=["context", "workspace"], help="Whether to change context or workspace")
    parser.add_argument('target', type=maybeInt, help="Number of target context or workspace.")
    parser.add_argument('--move', action='store_true', help="Take the currently focused window with you while switching to new context/workspace")
    args = parser.parse_args()
    return args

def i3SwitchWorkspace(workspace):
    os.system("i3-msg workspace {}".format(workspace.name))

def i3MoveWindow(workspace):
    os.system("i3-msg move workspace {}".format(workspace.name))

def i3ChangeOutput(output):
    os.system("i3-msg move workspace to output {}".format(output))

def switchOrMove(sourceWorkspace, targetWorkspace, move):
    if move:
        i3MoveWindow(targetWorkspace)
    i3SwitchWorkspace(targetWorkspace)

def changeToPreferredOutput(targetWorkspace):
    availableOutputs = [output["name"] for output in i3.get_outputs()]
    for (output, workspaces) in outputMap.items():
        if output in availableOutputs and targetWorkspace.rawName in workspaces:
            print("Changing to {}".format(output))
            i3ChangeOutput(output)

def handleDoublePress(source, target):
    if source == target and doublePressToNonEmpty:
        return Workspace.fromFirstNonEmptyOnSameContext(source)
    else:
        return target

def getTargetWorkspace(args, source, lastNonSharedContext):
    if args.type == "workspace":
        if type(args.target) == int: # Non-shared workspace
            if source.context.shared: 
                # We come from a shared context. Switch to the last context 
                # we had before we came to a shared workspace
                return Workspace.fromNumbers(lastNonSharedContext, args.target)
            else: 
                # We come from a non-shared context. Just switch via the numbers
                return Workspace.fromNumbers(source.context.id_, args.target)
        else: # Shared workspace
            return Workspace.fromSharedName(args.target)
    if args.type == "context":
        if source.context.shared:
            return source
        assert type(args.target) == int
        target = Workspace.fromNumbers(args.target, source.number)
        target = handleDoublePress(source, target)
        return target

def main(args):
    focusedWorkspace = Workspace.fromFocus()
    lastNonSharedContext = watchContext.getContext()
    targetWorkspace = getTargetWorkspace(args, focusedWorkspace, lastNonSharedContext)
    workspaceExisted = targetWorkspace.isOpenAlready
    switchOrMove(focusedWorkspace, targetWorkspace, args.move)
    if not targetWorkspace.context.shared:
        watchContext.setContext(targetWorkspace.context.id_)
    if not workspaceExisted:
        changeToPreferredOutput(targetWorkspace)

if __name__ == "__main__":
    args = setupArgs()
    main(args)
