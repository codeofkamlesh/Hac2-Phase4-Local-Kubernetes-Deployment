# Disk Cleanup (Urgent)

## Description
Aggressively cleans up unused Docker data (dangling images, build cache, stopped containers) to save disk space.

## Command
docker image prune -f && docker builder prune -a -f && docker container prune -f