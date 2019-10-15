from i3Contexts import config

class Context:
    def __init__(self, id_):
        self.id_ = id_

    @property
    def shared(self):
        return self.id_ == config.SHARED_CONTEXT

    @property
    def name(self):
        if self.shared:
            return "Shared"
        return config.contextNames[self.id_]

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.id_ == other.id_

    def fromName(name):
        if name == "Shared":
            return Context(config.SHARED_CONTEXT)
        return Context(config.contextNames.index(name))
