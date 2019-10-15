import i3
from i3Contexts import config
from i3Contexts.context import Context

class Workspace:
    def __init__(self, id_):
        self.id_ = id_
        self.lastVisit = -1

    def __eq__(self, other):
        if self.id_ == other.id_:
            assert self.name == other.name
        return self.id_ == other.id_

    @property
    def contextNumber(self):
        return (self.id_ - config.minContextOffset) // config.offsetPerContext

    @property
    def context(self):
        return Context(self.contextNumber)

    @property
    def rawName(self):
        if self.context.shared:
            return config.sharedWorkspaceNames[self.number]
        else:
            return config.workspaceNames[self.number]

    @property
    def number(self):
        return self.id_ - self.contextNumber * config.offsetPerContext - config.minContextOffset

    @property
    def isOpenAlready(self):
        return any(ws["name"] == self.name for ws in i3.get_workspaces())

    @staticmethod
    def fromContextAndName(contextId, workspaceName):
        if contextId == config.SHARED_CONTEXT:
            workspaceNumber = config.sharedWorkspaceNames.index(workspaceName)
        else:
            workspaceNumber = config.workspaceNames.index(workspaceName)
        return Workspace(config.minContextOffset + config.offsetPerContext * contextId + workspaceNumber)

    @staticmethod
    def fromFocus():
        workspaces = i3.get_workspaces()
        for ws in workspaces:
            if ws["focused"] == True:
                return Workspace.fromI3Workspace(ws)

    @staticmethod
    def fromI3Workspace(i3workspace):
        if i3workspace["name"] in config.sharedWorkspaceNames:
            return Workspace.fromSharedName(i3workspace["name"])
        else:
            return Workspace(i3workspace["num"])

    @staticmethod
    def fromSharedName(name):
        if ":" in name:
            id_, rawName = name.split(":")
            return Workspace(config.sharedWorkspaceNames.index(rawName))
        else:
            return Workspace(config.sharedWorkspaceNames.index(name))

    @staticmethod
    def fromFirstNonEmptyOnSameContext(source):
        nonEmptyWorkspacesInThisContext = []
        for i3workspace in sorted(i3.get_workspaces(), key = lambda ws: ws["num"]):
            workspace = Workspace.fromI3Workspace(i3workspace)
            if workspace.context == source.context and not workspace.empty:
                nonEmptyWorkspacesInThisContext.append(workspace)
        if len(nonEmptyWorkspacesInThisContext) > 0:
            return nonEmptyWorkspacesInThisContext[0]
        return source

    @property
    def empty(self):
        i3TreeNodes = i3.filter(name=self.name)
        # This workspace is not open - it's empty
        if len(i3TreeNodes) == 0:
            return True
        # If it does not have child nodes, it's empty
        return len(i3TreeNodes[0]["nodes"]) == 0

    @property
    def name(self):
        if self.context.shared:
            return config.sharedWorkspaceNameFormat.format(workspaceId=self.id_, workspaceName=self.rawName)
        else:
            return config.workspaceNameFormat.format(contextName=self.context.name, workspaceId=self.id_, workspaceName=self.rawName)

    def __str__(self):
        return self.name + "({})".format(self.lastVisit)

    def __repr__(self):
        return str(self)

