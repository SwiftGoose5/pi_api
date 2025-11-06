#!/bin/bash
docker build -t my-fastapi-app .
docker stop fastapi-container 2>/dev/null || true
docker rm fastapi-container 2>/dev/null || true

docker run -d \
  --name fastapi-container \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file ~/Documents/api_project/.env \
  -v ~/Documents/api_project/data.db:/app/data.db \
  my-fastapi-app