# Docker List Heavy Images

## Description
Lists all Docker images sorted by size to identify storage hogs.

## Command
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"