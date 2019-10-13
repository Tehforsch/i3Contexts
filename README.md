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
1. Switch to workspace number n:

`switch.py workspace n`

2. Switch to shared workspace name:

`switch.py workspace name`

3. Switch to workspace number n and take the currently focused window with you (this works the same way for shared workspaces)

`switch.py context n --move`

4. Switch to context number n:

`switch.py context n`

5. Switch to context number n and take the currently focused window with you

`switch.py context n --move`

## Example configuration
```
set $i3contexs python3 PATH/TO/SWITCH.PY
# Context switching
bindsym $mod+1 exec $i3contexts context 0
bindsym $mod+2 exec $i3contexts context 1
bindsym $mod+3 exec $i3contexts context 2

bindsym $mod+Shift+1 exec $i3contexts context --move 0
bindsym $mod+Shift+2 exec $i3contexts context --move 1
bindsym $mod+Shift+3 exec $i3contexts context --move 2

# Workspace switching
bindsym $mod+a exec $i3contexts workspace 1
bindsym $mod+s exec $i3contexts workspace 2
bindsym $mod+d exec $i3contexts workspace 3

bindsym $mod+Shift+a exec $i3contexts workspace --move 1
bindsym $mod+Shift+s exec $i3contexts workspace --move 2
bindsym $mod+Shift+d exec $i3contexts workspace --move 3

# Shared workspaces
bindsym $mod+v exec $i3contexts workspace music
bindsym $mod+c exec $i3contexts workspace chat

bindsym $mod+Shift+v exec $i3contexts workspace --move music
bindsym $mod+Shift+c exec $i3contexts workspace --move chat
```


## Todo
1. Currently the last context we were on before we switched to a shared workspace is tracked by writing to a file in the home folder. This is about as hacky as it gets and should probably be replaced by having some daemon run in the background that keeps track of the context but this also comes with its own problems
2. Currently there is no good system implemented for assigning default outputs to certain workspace numbers but that should not be hard to solve.
