from i3Contexts import config
from i3Contexts.workspace import Workspace
from i3Contexts.context import Context

class Session:
    def __init__(self, currentWorkspace):
        self.workspaces = []
        self.currentWorkspace = currentWorkspace
        self.numSwitch = 0
        self.switch(currentWorkspace)

    @property
    def lastSharedContext(self):
        print("not implemented")
        return 0

    def changeToPreferredOutput(self, targetWorkspace):
        availableOutputs = [output["name"] for output in i3.get_outputs()]
        for (output, workspaces) in outputMap.items():
            if output in availableOutputs and targetWorkspace.rawName in workspaces:
                i3ChangeOutput(output)


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
                return Workspace.fromContextAndName(self.lastSharedContext, targetStr)
            else: 
                # We come from a non-shared context. Just switch via the numbers
                return Workspace.fromContextAndName(self.currentWorkspace.context.id_, targetStr)
        else: # Shared workspace
            return Workspace.fromSharedName(targetStr)

    def getMostRecentWorkspaceInContext(self, context):
        workspacesInThisContext = [workspace for workspace in self.workspaces if workspace.context == context]
        if len(workspacesInThisContext) == 0:
            return Workspace.fromContextAndName(context.id_, config.defaultWorkspaceOnNewContext)
        else:
            sortedByVisitTime = sorted(workspacesInThisContext, key=lambda ws: -ws.lastVisit)
            return sortedByVisitTime[0]

    def getSwitchContextTarget(self, targetStr):
        return self.getMostRecentWorkspaceInContext(Context.fromName(targetStr))

    def switch(self, workspace):
        if not workspace in self.workspaces:
            self.workspaces.append(workspace)
        self.currentWorkspace.lastVisit = self.numSwitch
        self.numSwitch += 1
        self.currentWorkspace = workspace
