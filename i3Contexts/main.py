import argparse
from math import ceil
import i3
from i3Contexts.config import *
from i3Contexts import watchContext
from i3Contexts import i3Utils
from i3Contexts.workspace import Workspace
from i3Contexts.context import Context

def setupArgs():
    parser = argparse.ArgumentParser(description='Switch i3 workspaces and move windows between them based on contexts.')
    parser.add_argument('type', type=str, choices=["context", "workspace"], help="Whether to change context or workspace")
    parser.add_argument('target', type=str, help="Name of target context or workspace.")
    parser.add_argument('--move', action='store_true', help="Take the currently focused window with you while switching to new context/workspace")
    parser.add_argument('--firstNonEmptyWorkspace', action='store_true', help="If this flag is true, a context switch will automatically go to the first (that is: lowest number) workspace on the given context if the first workspace that it switches to is empty.")
    args = parser.parse_args()
    return args

def main(args):
    session = Session()
    handleArgs(session, args)

def switchWorkspace(session, targetStr, moveWindow):
    target = self.getSwitchWorkspaceTarget(targetStr)
    session.switch(target)
    i3Utils.switchOrMove(target, moveWindow)

def switchContext(session, targetStr, moveWindow):
    target = self.getSwitchContextTarget(targetStr)
    session.switch(target)
    i3Utils.switchOrMove(target, moveWindow)

def handleArgs(session, args):
    if args.type == "workspace":
        switchWorkspace(session, args.target, args.move)
    else:
        switchContext(session, args.target, args.move)

def main(args):
    handleArgs(args)

# def main(args):
#     focusedWorkspace = Workspace.fromFocus()
#     lastNonSharedContext = watchContext.getContext()
#     targetWorkspace = getTargetWorkspace(args, focusedWorkspace, lastNonSharedContext)
#     workspaceExisted = targetWorkspace.isOpenAlready
#     i3Utils.switchOrMove(focusedWorkspace, targetWorkspace, args.move)
#     if not targetWorkspace.context.shared:
#         watchContext.setContext(targetWorkspace.context.id_)
#     if not workspaceExisted:
#         changeToPreferredOutput(targetWorkspace)
