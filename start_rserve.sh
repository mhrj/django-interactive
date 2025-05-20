#!/bin/sh

echo "Starting Rserve..."
R CMD Rserve --RS-port 6312 --vanilla --RS-enable-remote

# Keep container alive
tail -f /dev/null
