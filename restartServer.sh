#!/bin/bash
for id in $(pgrep -f "i3Contexts/server.py" | grep -v nvim); do
    kill $id
done
python3 ~/projects/config/i3Contexts/server.py
