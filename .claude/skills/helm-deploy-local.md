# Helm Deploy Local

## Description
Deploys the Helm chart forcing localhost URLs to prevent CORS errors.

## Command
export $(grep -v '^#' backend/.env | xargs) && helm upgrade --install todo-app ./k8s/todo-chart --set env.databaseUrl="$DATABASE_URL" --set env.cohereApiKey="$COHERE_API_KEY" --set env.betterAuthSecret="$BETTER_AUTH_SECRET" --set env.BETTER_AUTH_URL="http://localhost:3000" --set env.HOSTNAME="0.0.0.0" --set env.HOST="0.0.0.0"