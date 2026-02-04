# Todo App with AI

## Authentication Setup

### Environment Variables

For proper  authentication setup, ensure the following environment variables are configured correctly:

#### Backend (phase2/backend/.env)
```env
BETTER_AUTH_SECRET=your_secret_key_here
```

#### Frontend (phase2/frontend/.env.local)
```env
BETTER_AUTH_SECRET=your_secret_key_here
BETTER_AUTH_URL=http://localhost:3000
```

**Important**: The `BETTER_AUTH_SECRET` value must be identical in both files for proper authentication to work.

### Verification Steps

1. Check that both environment files have the same `BETTER_AUTH_SECRET` value
2. Restart both frontend (`npm run dev`) and backend (`uvicorn`) servers after making changes
3. Test the authentication route: `http://localhost:3000/api/auth/session`

### Debugging Authentication Issues

If you encounter authentication problems:

1. Check the backend server logs for DEBUG messages showing token verification details
2. Open browser developer tools and check the console for DEBUG messages about tokens being sent
3. Verify that the frontend can reach the backend authentication endpoints