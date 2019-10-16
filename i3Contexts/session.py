from i3Contexts import config
from i3Contexts.workspace import Workspace
from i3Contexts.context import Context

class Session:
    def __init__(self, currentWorkspace):
        self.currentWorkspace = currentWorkspace
        self.workspaces = []
        self.numSwitch = 0
        self.switch(self.currentWorkspace)

    @property
    def lastNonSharedContext(self):
        assert len(self.workspaces) > 0
        return self.getWorkspacesByVisitTime()[0].context

    def handleEmptyWorkspace(self, source, target):
        if (source == target and doublePressToNonEmpty) or args.firstNonEmptyWorkspace:
            return Workspace.fromFirstNonEmptyOnSameContext(target)
        else:
            return target

    def getSwitchWorkspaceTarget(self, targetStr):
        if targetStr in config.workspaceNames:
            if self.currentWorkspace.context.shared: 
                # We come from a shared context. Switch to the last context 
                # we had before we came to a shared workspace
                return Workspace.fromContextAndName(self.lastNonSharedContext.id_, targetStr)
            else: 
                # We come from a non-shared context. Just switch via the numbers
                return Workspace.fromContextAndName(self.currentWorkspace.context.id_, targetStr)
        else: # Shared workspace
            return Workspace.fromSharedName(targetStr)

    def getWorkspacesByVisitTime(self):
        return sorted(self.workspaces, key=lambda ws: -ws.lastVisit)    
    
    def getMostRecentWorkspaceInContext(self, context):
        workspacesInThisContext = [workspace for workspace in self.getWorkspacesByVisitTime() if workspace.context == context]
        if len(workspacesInThisContext) == 0:
            return Workspace.fromContextAndName(context.id_, config.defaultWorkspaceOnNewContext)
        else:
            return workspacesInThisContext[0]

    def getSwitchContextTarget(self, targetStr):
        return self.getMostRecentWorkspaceInContext(Context.fromName(targetStr))

    def switch(self, workspace):
        if not workspace in self.workspaces:
            self.workspaces.append(workspace)
        self.currentWorkspace.lastVisit = self.numSwitch
        self.numSwitch += 1
        self.currentWorkspace = workspace
