# i3Contexts
## Concept
This introduces simple "context"-based workspace management for i3.

A context is a set of workspaces that all belong to the same general project that you're working on (examples: work, personal, writing, ...)
Switching context effectively "remaps" all the usual workspace hotkeys to different workspaces.

For example: We have set up 10 workspaces called 1-10 and they all have hotkeys set up to switch/move to them.
If we are in context a, the actual workspace names are a1-a10
If we now switch contexts to context b, the workspace names that are accessed via the same hotkeys become b1-b10.

It is also possible to configure shared workspaces which are accessed via the same hotkey no matter the current context (music player, chat client, ...).
When moving from a shared workspace back to a normal, context-based workspace the script remembers the last context we were on.

## Commands
Switch to workspace number n:
`switch.py workspace n`
Switch to shared workspace name:
`switch.py workspace name`
Switch to workspace number n and take the currently focused window with you (this works the same way for shared workspaces)
`switch.py context n --move`

Switch to context number n:
`switch.py context n`
Switch to context number n and take the currently focused window with you
`switch.py context n --move`

## Todo
1. Currently the last context we were on before we switched to a shared workspace is tracked by writing to a file in the home folder. This is about as hacky as it gets and should probably be replaced by having some daemon run in the background that keeps track of the context but this also comes with its own problems
2. Currently there is no good system implemented for assigning default outputs to certain workspace numbers but that should not be hard to solve.
