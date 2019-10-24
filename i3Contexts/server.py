import rpyc
from rpyc.utils.server import ThreadedServer
from i3Contexts import serverConfig
from i3Contexts import config
from i3Contexts.session import Session
from i3Contexts.workspace import Workspace
from i3Contexts import i3Utils

import i3

import logging

def isProperWorkspace(i3workspace):
    return ":" in i3workspace["name"]

def getWorkspacesString(workspaces):
    return ", ".join(str(w) for w in workspaces)

def initialConfigurationFromI3Workspaces():
    currentWorkspace = getFocusedWorkspace()
    session = Session(currentWorkspace)
    session.workspaces = [Workspace.fromI3Workspace(ws) for ws in i3.get_workspaces()]
    print("Reading initial workspaces: {}".format(getWorkspacesString(session.workspaces)))
    return session

def getFocusedWorkspace():
    currentWorkspace = next(ws for ws in i3.get_workspaces() if ws["focused"])
    if not isProperWorkspace(currentWorkspace): # We are on a non-i3context-managed workspace.
        return Workspace.fromContextAndName(0, config.defaultWorkspaceOnNewContext)
    else:
        return Workspace.fromI3Workspace(currentWorkspace)

def updateFromI3(session):
    currentWorkspace = getFocusedWorkspace()
    session.switch(currentWorkspace)
    i3Workspaces = [ws["name"] for ws in i3.get_workspaces()]
    session.workspaces = [workspace for workspace in session.workspaces if workspace.name in i3Workspaces]
    assert len(session.workspaces) == len(set(ws.name for ws in session.workspaces))

def changeToPreferredOutput(session, targetWorkspace):
    availableOutputs = [output["name"] for output in i3.get_outputs()]
    for (output, workspaces) in config.outputMap.items():
        if output in availableOutputs and targetWorkspace.rawName in workspaces:
            print("Changing to {}".format(output))
            i3Utils.i3ChangeOutput(output)

class i3ContextServer(rpyc.Service):
    def exposed_switchWorkspace(self, targetStr, moveWindow):
        print("Switching to workspace with name {}".format(targetStr))
        self.switch(session.getSwitchWorkspaceTarget, targetStr, moveWindow)

    def exposed_switchContext(self, targetStr, moveWindow):
        print("Switching to context with name {}".format(targetStr))
        self.switch(session.getSwitchContextTarget, targetStr, moveWindow)

    def switch(self, targetFunction, targetStr, moveWindow):
        print("State before i3 update: {}".format(getWorkspacesString(session.workspaces)))
        updateFromI3(session)
        print("State after  i3 update: {}".format(getWorkspacesString(session.workspaces)))
        target = targetFunction(targetStr)
        wasAlreadyOpen = target in session.workspaces
        session.switch(target)
        i3Utils.switchOrMove(target, moveWindow)
        print("Target workspace: {}".format(target))
        print("This workspaces was {} already open".format("" if wasAlreadyOpen else "not"))
        if not wasAlreadyOpen:
            print("Since this workspace was not opened yet: switch to preferred output")
            changeToPreferredOutput(session, target)

session = initialConfigurationFromI3Workspaces()

server = ThreadedServer(i3ContextServer, port=serverConfig.port)
server.start()
