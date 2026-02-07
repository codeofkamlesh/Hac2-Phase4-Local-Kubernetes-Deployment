import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
    // Ye automatic switch karega: Local computer par localhost, aur Vercel par Live URL
    baseURL:  "http://localhost:3000"
})