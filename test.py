import unittest
import switch
from switch import Workspace, Context
import config
import watchContext

class Args:
    def __init__(self, type_, target, firstNonEmptyWorkspace=False):
        self.type = type_
        self.target = target
        self.firstNonEmptyWorkspace = firstNonEmptyWorkspace

class TestSwitch(unittest.TestCase):
    def nonSharedWorkspaces(self, contextId):
        for workspaceNumber in range(0, config.workspacesPerContext):
            yield Workspace.fromNumbers(contextId, workspaceNumber)

    def sharedWorkspaces(self):
        for name in config.sharedWorkspaceNames:
            yield Workspace.fromSharedName(name)

    @property
    def contexts(self):
        for targetNumber in range(0, len(config.contextNames)):
            yield Context(targetNumber)

    def testSwitchWorkspace(self):
        for context in self.contexts:
            for workspace1 in self.nonSharedWorkspaces(context.id_):
                for workspace2 in self.nonSharedWorkspaces(context.id_):
                    args = Args("workspace", workspace2.number)
                    target = switch.getTargetWorkspace(args, workspace1, context.id_)
                    self.assertEqual(target.number, workspace2.number)
                    self.assertEqual(target.context, workspace1.context)
                    self.assertEqual(target.context, context)

    def testSwitchContext(self):
        for context1 in self.contexts:
            for workspace in self.nonSharedWorkspaces(context1.id_):
                for context2 in self.contexts:
                    args = Args("context", context2.id_)
                    target = switch.getTargetWorkspace(args, workspace, context1.id_)
                    self.assertEqual(target.number, workspace.number)
                    self.assertEqual(target.context, context2)

    def testSwitchNonSharedToSharedWorkspace(self):
        for context in self.contexts:
            for workspace1 in self.nonSharedWorkspaces(context.id_):
                for workspace2 in self.sharedWorkspaces():
                    args = Args("workspace", workspace2.name)
                    # Switch to the shared workspace
                    target = switch.getTargetWorkspace(args, workspace1, context.id_)
                    self.assertEqual(target.id_, workspace2.id_)
                    self.assertEqual(target.context.id_, switch.SHARED_CONTEXT)
                    # Switch back. Check that the context is the previous one
                    args = Args("workspace", workspace1.number)
                    target = switch.getTargetWorkspace(args, workspace2, context.id_)
                    self.assertEqual(target.number, workspace1.number)
                    self.assertEqual(target.context, context)

    def testSwitchSharedToShared(self):
        for context in self.contexts:
            for workspace1 in self.sharedWorkspaces():
                for workspace2 in self.sharedWorkspaces():
                    args = Args("workspace", workspace2.name)
                    target = switch.getTargetWorkspace(args, workspace1, context.id_)
                    self.assertEqual(target.name, workspace2.name)
                    self.assertEqual(target.context.id_, switch.SHARED_CONTEXT)

    def testSwitchingContextWhenOnSharedWorkspace(self):
        for context in self.contexts:
            for workspace in self.sharedWorkspaces():
                args = Args("context", context.id_, firstNonEmptyWorkspace=False)
                target = switch.getTargetWorkspace(args, workspace, context.id_)
                self.assertEqual(target, workspace)
                self.assertEqual(target.context.id_, switch.SHARED_CONTEXT)

if __name__ == '__main__':
    switch.doublePressToNonEmpty = False
    unittest.main()

