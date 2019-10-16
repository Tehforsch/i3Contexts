for id in $(pgrep -f server.py); do
    kill $id
done
python3 server.py
