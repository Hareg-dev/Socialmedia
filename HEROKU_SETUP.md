# Heroku Deployment Guide

## Step 1: Install Heroku CLI
Download and install from: https://devcenter.heroku.com/articles/heroku-cli
After installation, restart your terminal.

## Step 2: Login to Heroku
```bash
heroku login
```

## Step 3: Create Heroku App
```bash
heroku create your-app-name
```

## Step 4: Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:essential-0
```

## Step 5: Set Environment Variables
```bash
heroku config:set SECRET_KEY="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
heroku config:set ALGORITHM="HS256"
heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

## Step 6: Commit Changes
```bash
git add .
git commit -m "Prepare for Heroku deployment"
```

## Step 7: Deploy to Heroku
```bash
git push heroku main
```

## Step 8: Run Database Migrations
```bash
heroku run alembic upgrade head
```

## Step 9: Open Your App
```bash
heroku open
```

## Useful Commands
- View logs: `heroku logs --tail`
- Check app status: `heroku ps`
- View config: `heroku config`
- Restart app: `heroku restart`
