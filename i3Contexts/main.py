import argparse
from math import ceil
import i3
from i3Contexts.config import *
from i3Contexts import watchContext
from i3Contexts import i3Utils
from i3Contexts.workspace import Workspace
from i3Contexts.context import Context

def maybeInt(x):
    try:
        return int(x)
    except ValueError:
        return x

def setupArgs():
    parser = argparse.ArgumentParser(description='Switch i3 workspaces and move windows between them based on contexts.')
    parser.add_argument('type', type=str, choices=["context", "workspace"], help="Whether to change context or workspace")
    parser.add_argument('target', type=maybeInt, help="Number of target context or workspace.")
    parser.add_argument('--move', action='store_true', help="Take the currently focused window with you while switching to new context/workspace")
    parser.add_argument('--firstNonEmptyWorkspace', action='store_true', help="If this flag is true, a context switch will automatically go to the first (that is: lowest number) workspace on the given context if the first workspace that it switches to is empty.")
    args = parser.parse_args()
    return args

def switchOrMove(sourceWorkspace, targetWorkspace, move):
    if move:
        i3MoveWindow(targetWorkspace)
    i3Utils.i3SwitchWorkspace(targetWorkspace)

def changeToPreferredOutput(targetWorkspace):
    availableOutputs = [output["name"] for output in i3.get_outputs()]
    for (output, workspaces) in outputMap.items():
        if output in availableOutputs and targetWorkspace.rawName in workspaces:
            print("Changing to {}".format(output))
            i3ChangeOutput(output)

def handleEmptyWorkspace(args, source, target):
    if (source == target and doublePressToNonEmpty) or args.firstNonEmptyWorkspace:
        return Workspace.fromFirstNonEmptyOnSameContext(target)
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
            if args.firstNonEmptyWorkspace:
                target = handleEmptyWorkspace(args, source, Workspace.fromNumbers(args.target, lowestWorkspaceNumber))
                if target is not None:
                    return target
            else:
                return source
        assert type(args.target) == int
        target = Workspace.fromNumbers(args.target, source.number)
        if target.empty:
            target = handleEmptyWorkspace(args, source, target)
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
