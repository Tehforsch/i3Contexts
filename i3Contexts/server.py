import rpyc
from rpyc.utils.server import ThreadedServer
from i3Contexts import serverConfig
from i3Contexts import config
from i3Contexts.session import Session
from i3Contexts.workspace import Workspace
from i3Contexts import i3Utils

import i3

def initialConfigurationFromI3Workspaces(session):
    for ws in i3.get_workspaces():
        workspace = Workspace.fromI3Workspace(ws)
        if ws["focused"]:
            session.currentWorkspace = workspace
            session.currentWorkspace.lastVisit=1
        session.workspaces.append(workspace)

class i3ContextServer(rpyc.Service):
    def exposed_switchWorkspace(self, targetStr, moveWindow):
        target = session.getSwitchWorkspaceTarget(targetStr)
        session.switch(target)
        i3Utils.switchOrMove(target, moveWindow)

    def exposed_switchContext(self, targetStr, moveWindow):
        target = session.getSwitchContextTarget(targetStr)
        session.switch(target)
        i3Utils.switchOrMove(target, moveWindow)

session = Session()
initialConfigurationFromI3Workspaces(session)

server = ThreadedServer(i3ContextServer, port=serverConfig.port)
server.start()
