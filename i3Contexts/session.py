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
        nonSharedByVisitTime = [ws for ws in self.getWorkspacesByVisitTime() if not ws.context.shared]
        if len(nonSharedByVisitTime) == 0:
            return Context(0)
        else:
            return next(ws.context for ws in nonSharedByVisitTime)

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
        if workspace in self.workspaces:
            # Make sure we point to the instance in the list and not to some random instance.
            workspace = next(ws for ws in self.workspaces if ws == workspace)
        else:
            self.workspaces.append(workspace)
        self.numSwitch += 1
        self.currentWorkspace = workspace
        if not self.currentWorkspace.context.shared:
            self.currentWorkspace.lastVisit = self.numSwitch
