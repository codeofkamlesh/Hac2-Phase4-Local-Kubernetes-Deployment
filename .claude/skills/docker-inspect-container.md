# Docker Inspect Container

## Description
Inspects a container to reveal its Environment Variables (Use this to check for 'BETTER_AUTH_URL').

## Command
docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}'