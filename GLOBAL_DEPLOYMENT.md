# 🌍 Global Deployment Guide

## Current Situation

- `http://192.168.96.121:3000/` only works on your local network
- To share globally, you need a public URL

## Option 1: Ngrok (Quick & Easy) ⭐

### Prerequisites

- ngrok installed: `brew install ngrok`
- ngrok account (free at https://ngrok.com/)

### Steps

1. **Start your app locally:**

   ```bash
   ./run_local.sh
   ```

2. **In a new terminal, create public tunnel:**

   ```bash
   ngrok http 3000
   ```

3. **Share the ngrok URL** (e.g., `https://abc123.ngrok.io`) with anyone worldwide!

### Pros

- ✅ Instant global access
- ✅ No server setup required
- ✅ Works immediately

### Cons

- ❌ URL changes each time you restart
- ❌ Free tier has limitations
- ❌ Requires your computer to stay on

---

## Option 2: Cloud Hosting (Permanent) 🚀

### Render.com (Recommended)

1. **Create account** at render.com
2. **Connect your GitHub** repository
3. **Deploy as Web Service**
4. **Get permanent URL** like `https://your-app.onrender.com`

### Vercel (Frontend Only)

1. **Create account** at vercel.com
2. **Import your frontend** folder
3. **Deploy** with one click

### Railway

1. **Create account** at railway.app
2. **Connect GitHub** repository
3. **Auto-deploy** from your code

---

## Option 3: VPS/Cloud Server 💻

### AWS EC2 / DigitalOcean / Linode

1. **Rent a server** ($5-20/month)
2. **Deploy your app** using Docker
3. **Get permanent domain** (optional)

---

## Quick Start with Ngrok

```bash
# 1. Make sure you have ngrok
which ngrok || brew install ngrok

# 2. Start your app
./run_local.sh

# 3. In new terminal, create tunnel
ngrok http 3000

# 4. Share the https://xxx.ngrok.io URL!
```

## Environment Variables for Production

Create `.env.production` in frontend folder:

```
REACT_APP_API_BASE=https://your-backend-url.com
```

## Security Considerations

1. **API Keys**: Never expose in frontend code
2. **CORS**: Configure properly for production
3. **Rate Limiting**: Add to prevent abuse
4. **HTTPS**: Always use in production

## Troubleshooting

### Ngrok Issues

- **"Tunnel not found"**: Restart ngrok
- **"Connection refused"**: Check if local servers are running
- **"Invalid host header"**: Add `--host-header=rewrite` to ngrok command

### CORS Issues

- Update `main.py` CORS settings for production domains
- Add your domain to `allow_origins`

### Port Issues

- Make sure ports 3000 and 8000 are available
- Check firewall settings

## Next Steps

1. **Try ngrok first** for quick testing
2. **Choose cloud hosting** for permanent deployment
3. **Add custom domain** for professional look
4. **Set up monitoring** and analytics

---

**Need help?** Check the deployment logs or ask for assistance!
