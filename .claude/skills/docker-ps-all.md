# Docker PS All

## Description
Lists ALL containers (running and stopped) to find crashed services.

## Command
docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"