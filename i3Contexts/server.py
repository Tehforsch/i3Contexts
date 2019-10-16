import rpyc
from rpyc.utils.server import ThreadedServer
from i3Contexts import serverConfig
from i3Contexts import config
from i3Contexts.session import Session
from i3Contexts.workspace import Workspace
from i3Contexts import i3Utils

import i3

def initialConfigurationFromI3Workspaces():
    currentWorkspace = next(ws for ws in i3.get_workspaces() if ws["focused"])
    session = Session(Workspace.fromI3Workspace(currentWorkspace))
    for ws in i3.get_workspaces():
        workspace = Workspace.fromI3Workspace(ws)
        session.workspaces.append(workspace)
    return session

def updateFromI3(session):
    i3Workspaces = [ws["name"] for ws in i3.get_workspaces()]
    session.workspaces = [workspace for workspace in session.workspaces if workspace.name in i3Workspaces]

def changeToPreferredOutput(session, targetWorkspace):
    availableOutputs = [output["name"] for output in i3.get_outputs()]
    for (output, workspaces) in config.outputMap.items():
        if output in availableOutputs and targetWorkspace.rawName in workspaces:
            i3Utils.i3ChangeOutput(output)

class i3ContextServer(rpyc.Service):
    def exposed_switchWorkspace(self, targetStr, moveWindow):
        self.switch(session.getSwitchWorkspaceTarget, targetStr, moveWindow)

    def exposed_switchContext(self, targetStr, moveWindow):
        self.switch(session.getSwitchContextTarget, targetStr, moveWindow)

    def switch(self, targetFunction, targetStr, moveWindow):
        updateFromI3(session)
        target = targetFunction(targetStr)
        wasAlreadyOpen = target in session.workspaces
        session.switch(target)
        i3Utils.switchOrMove(target, moveWindow)
        if not wasAlreadyOpen:
            changeToPreferredOutput(session, target)

session = initialConfigurationFromI3Workspaces()

server = ThreadedServer(i3ContextServer, port=serverConfig.port)
server.start()
