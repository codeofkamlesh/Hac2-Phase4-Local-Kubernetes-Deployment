# Audit Vercel Leaks

## Description
Scans the codebase for any lingering Vercel production URLs that cause network errors.

## Command
grep -r "vercel.app" ./phase4/frontend ./phase4/backend || echo "No leaks found!"