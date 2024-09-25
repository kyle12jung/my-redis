#!/bin/bash
set -e

# Run the Python server script in the background
exec python3 -m app.main "$@" &

# Give the server a little time to start
sleep 2

# Send two PING messages to the server
echo "PING\r\n" | nc localhost 6379

# Wait a second before sending the next PING
sleep 1

# Send another PING message
echo "ECHO hey" | nc localhost 6379
