from i3Contexts import config

def getContext():
    with config.contextFile.open("r") as f:
        return int(f.read())

def setContext(context):
    if context < 0:
        return
    with config.contextFile.open("w") as f:
        f.write(str(context))

def createContextFileIfItDoesNotExist():
    if not config.contextFile.is_file():
        with config.contextFile.open("w") as f:
            f.write(str(defaultContext))
