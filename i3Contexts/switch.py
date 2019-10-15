import rpyc
import argparse
from math import ceil
import i3
from i3Contexts import i3Utils
from i3Contexts.workspace import Workspace
from i3Contexts.context import Context
from i3Contexts import serverConfig

def setupArgs():
    parser = argparse.ArgumentParser(description='Switch i3 workspaces and move windows between them based on contexts.')
    parser.add_argument('type', type=str, choices=["context", "workspace"], help="Whether to change context or workspace")
    parser.add_argument('target', type=str, help="Name of target context or workspace.")
    parser.add_argument('--move', action='store_true', help="Take the currently focused window with you while switching to new context/workspace")
    parser.add_argument('--firstNonEmptyWorkspace', action='store_true', help="If this flag is true, a context switch will automatically go to the first (that is: lowest number) workspace on the given context if the first workspace that it switches to is empty.")
    args = parser.parse_args()
    return args

def main():
    args = setupArgs()
    server = rpyc.connect("localhost", serverConfig.port).root
    if args.type == "workspace":
        server.switchWorkspace(args.target, args.move)
    else:
        server.switchContext(args.target, args.move)
