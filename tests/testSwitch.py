import unittest
from i3Contexts import switch
from i3Contexts.workspace import Workspace
from i3Contexts.context import Context
from i3Contexts.session import Session
from i3Contexts import config

class TestSwitch(unittest.TestCase):
    def workspaceNames(self, contextId):
        for name in config.workspaceNames:
            yield Workspace.fromContextAndName(contextId, name)

    def sharedWorkspaces(self):
        for name in config.sharedWorkspaceNames:
            yield Workspace.fromSharedName(name)

    @property
    def contexts(self):
        for targetNumber in range(0, len(config.contextNames)):
            yield Context(targetNumber)

    def testSwitchWorkspace(self):
        for context in self.contexts:
            for workspace1 in self.workspaceNames(context.id_):
                for workspace2 in self.workspaceNames(context.id_):
                    session = Session(workspace1)
                    target = session.getSwitchWorkspaceTarget(workspace2.rawName)
                    self.assertEqual(target.number, workspace2.number)
                    self.assertEqual(target.context, workspace1.context)
                    self.assertEqual(target.context, context)

    def testSwitchNonSharedToSharedWorkspace(self):
        for context in self.contexts:
            for workspace1 in self.workspaceNames(context.id_):
                for workspace2 in self.sharedWorkspaces():
                    session = Session(workspace1)
                    # Switch to the shared workspace
                    target = session.getSwitchWorkspaceTarget(workspace2.rawName)
                    session.switch(target)
                    self.assertEqual(target.id_, workspace2.id_)
                    self.assertEqual(target.context.id_, config.SHARED_CONTEXT)
                    # Switch back. Check that the context is the previous one
                    target = session.getSwitchWorkspaceTarget(workspace1.rawName)
                    self.assertEqual(target.number, workspace1.number)
                    self.assertEqual(target.context, context)

    def testSwitchSharedToShared(self):
        for context in self.contexts:
            for workspace1 in self.sharedWorkspaces():
                for workspace2 in self.sharedWorkspaces():
                    session = Session(workspace1)
                    target = session.getSwitchWorkspaceTarget(workspace2.rawName)
                    self.assertEqual(target.name, workspace2.name)
                    self.assertEqual(target.context.id_, config.SHARED_CONTEXT)

    def testSwitchToEmptyContext(self):
        for context1 in self.contexts:
            for workspace in self.workspaceNames(context1.id_):
                for context2 in self.contexts:
                    if context2 == workspace.context:
                        continue
                    session = Session(workspace)
                    target = session.getSwitchContextTarget(context2.name)
                    self.assertEqual(target.rawName, config.defaultWorkspaceOnNewContext)
                    self.assertEqual(target.context, context2)

    def testSwitchBackToContext(self):
        for context1 in self.contexts:
            for workspace in self.workspaceNames(context1.id_):
                for context2 in self.contexts:
                    session = Session(workspace)
                    target = session.getSwitchContextTarget(context2.name)
                    session.switch(target)
                    target = session.getSwitchContextTarget(context1.name)
                    assert target == workspace

    def testSwitchBackToContextWithMultipleWorkspaces(self):
        for context1 in self.contexts:
            # amazing hack to loop over workspaces in pairs of two
            workspaces=self.workspaceNames(context1.id_)
            for (workspace1, workspace2) in zip(workspaces, workspaces):
                for context2 in self.contexts:
                    session = Session(workspace1)
                    session.switch(session.getSwitchWorkspaceTarget(workspace2.rawName))
                    session.switch(session.getSwitchContextTarget(context2.name))
                    target = session.getSwitchContextTarget(context1.name)
                    assert target == workspace2

