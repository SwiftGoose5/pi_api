#!/bin/bash
docker build -t my-fastapi-app .
docker stop fastapi-container
docker rm fastapi-container
docker run -d \
  --name fastapi-container \
  -p 8000:8000 \
  --env-file ~/Documents/api_project/.env \
  -v /sys/class/thermal:/sys/class/thermal:ro \
  -v ~/Documents/api_project/data.db:/app/data.db \
  my-fastapi-app