#!/bin/bash

echo "Restarting web UI docker container..."
ssh root@192.168.69.3 "cd /media/gitwww/git-scripts/klaus && docker-compose restart"
