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

class i3ContextServer(rpyc.Service):
    def exposed_switchWorkspace(self, targetStr, moveWindow):
        target = session.getSwitchWorkspaceTarget(targetStr)
        session.switch(target)
        i3Utils.switchOrMove(target, moveWindow)

    def exposed_switchContext(self, targetStr, moveWindow):
        target = session.getSwitchContextTarget(targetStr)
        session.switch(target)
        i3Utils.switchOrMove(target, moveWindow)

session = initialConfigurationFromI3Workspaces()

server = ThreadedServer(i3ContextServer, port=serverConfig.port)
server.start()
