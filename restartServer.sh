#!/bin/bash
for id in $(pgrep -f "python3 server.py" | grep -v nvim); do
    kill $id
done
python3 ~/projects/i3Contexts/server.py
