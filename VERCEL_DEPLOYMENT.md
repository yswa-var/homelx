# Vercel Frontend Deployment Guide

This guide will help you deploy the Homelx frontend to Vercel.

## Prerequisites

1. A Vercel account (free tier available)
2. Your backend already deployed on Render
3. Your code pushed to a Git repository (GitHub, GitLab, etc.)

## Step 1: Prepare Your Backend URL

First, make sure your backend is deployed on Render and you have the URL. It should look like:
`https://your-app-name.onrender.com`

## Step 2: Update Frontend Configuration

1. Open `frontend/src/config.js`
2. Replace the production URL with your actual Render backend URL:

```javascript
// Configuration for API endpoints
const config = {
  // Development - local backend
  development: {
    baseURL: "http://localhost:8000",
  },
  // Production - Render backend
  production: {
    baseURL: "https://your-actual-render-url.onrender.com", // ← Update this
  },
};
```

## Step 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. Configure the project:

   - **Framework Preset**: Vite
   - **Root Directory**: `./` (root of your repo)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: Leave empty (will use the build command)

5. Click "Deploy"

### Option B: Deploy via Vercel CLI

1. Install Vercel CLI:

```bash
npm i -g vercel
```

2. Login to Vercel:

```bash
vercel login
```

3. Deploy from your project root:

```bash
vercel
```

4. Follow the prompts:
   - Link to existing project or create new
   - Confirm settings
   - Deploy

## Step 4: Environment Variables (Optional)

If you want to make the backend URL configurable via environment variables:

1. In Vercel dashboard, go to your project settings
2. Add environment variable:

   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-render-backend-url.onrender.com`

3. Update `frontend/src/config.js`:

```javascript
const config = {
  development: {
    baseURL: "http://localhost:8000",
  },
  production: {
    baseURL:
      import.meta.env.VITE_API_URL || "https://your-fallback-url.onrender.com",
  },
};
```

## Step 5: Test Your Deployment

1. Visit your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Test the chat functionality
3. Verify that API calls are going to your Render backend

## Troubleshooting

### Common Issues

1. **Build Fails**:

   - Check that `frontend/package.json` exists
   - Verify all dependencies are listed
   - Check Vercel build logs for errors

2. **API Calls Fail**:

   - Verify your backend URL is correct in `config.js`
   - Check that your Render backend is running
   - Test the backend URL directly in browser

3. **CORS Errors**:

   - Your backend should already have CORS configured
   - If issues persist, check the CORS settings in `backend/main.py`

4. **404 Errors**:
   - The `vercel.json` should handle SPA routing
   - If not working, check the rewrites configuration

### Vercel-specific Issues

1. **Function Timeout**:

   - Vercel has a 10-second timeout for serverless functions
   - Your API calls should be fast enough, but streaming might be affected

2. **Cold Starts**:
   - Vercel functions have cold starts
   - First request might be slower

## Custom Domain (Optional)

1. In Vercel dashboard, go to your project
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Follow the DNS configuration instructions

## Monitoring

1. **Vercel Analytics**: Built-in analytics in Vercel dashboard
2. **Function Logs**: Check function execution logs
3. **Performance**: Monitor Core Web Vitals

## Next Steps

After successful deployment:

1. **Update Documentation**: Add your Vercel URL to your project README
2. **Set Up Monitoring**: Configure alerts and monitoring
3. **Custom Domain**: Add a custom domain if desired
4. **Environment Variables**: Move sensitive config to environment variables

## File Structure for Vercel

Your repository should look like this for Vercel deployment:

```
homelx/
├── backend/
│   └── main.py
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── vercel.json          ← Vercel configuration
├── requirements.txt
└── README.md
```

The `vercel.json` file tells Vercel:

- How to build the frontend
- Where to find the built files
- How to handle routing for the SPA
- How to cache static assets
