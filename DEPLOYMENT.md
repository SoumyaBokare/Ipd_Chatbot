# 🚀 Deploying to Render.com

This guide will help you deploy your Ollama chatbot to Render.com for free/low-cost hosting.

## 📋 Prerequisites

1. **GitHub Account** - Your code is already on GitHub ✅
2. **Render Account** - Sign up at https://render.com (free)

---

## 🎯 Step-by-Step Deployment

### **Step 1: Push Deployment Files to GitHub**

Make sure you've committed the new files:
```powershell
git add Dockerfile render.yaml .dockerignore DEPLOYMENT.md
git commit -m "Add Render deployment configuration"
git push
```

### **Step 2: Create Render Account**

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account (recommended)

### **Step 3: Connect Your Repository**

1. In Render dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository: **`Ipd_Chatbot`**
5. Click **"Connect"**

### **Step 4: Configure the Service**

Render will auto-detect your `render.yaml` file, but verify these settings:

**Basic Settings:**
- **Name:** `ollama-chatbot` (or your preferred name)
- **Runtime:** Docker
- **Region:** Oregon (or closest to you)
- **Branch:** `main`

**Plan:**
- **Free Plan:** Limited resources but free
- **Starter Plan ($7/month):** Recommended for better performance
  - 512MB RAM minimum
  - Better for running Ollama models

**Advanced Settings:**
- **Health Check Path:** `/api/health`
- **Auto-Deploy:** Yes (deploys automatically on git push)

**Disk (Important for Ollama!):**
- **Name:** `ollama-models`
- **Mount Path:** `/root/.ollama`
- **Size:** 10 GB (needed for model storage)

### **Step 5: Deploy!**

1. Click **"Create Web Service"**
2. Render will start building your Docker container
3. **This will take 10-20 minutes** for the first deployment:
   - Installing dependencies
   - Downloading Ollama
   - Pulling the llama3.1:8b model (~4.7GB)

### **Step 6: Monitor Deployment**

Watch the logs in Render dashboard:
- ✅ "Starting Ollama service..."
- ✅ "Pulling llama3.1:8b model..."
- ✅ "Starting Flask application..."
- ✅ "Web server ready!"

### **Step 7: Access Your Chatbot**

Once deployed, Render will give you a URL like:
```
https://ollama-chatbot.onrender.com
```

Visit this URL to use your chatbot online! 🎉

---

## ⚙️ Configuration Options

### **Change the Model**

Edit `Dockerfile` line that says `ollama pull llama3.1:8b` to use a different model:

```dockerfile
# For faster/smaller model:
ollama pull gemma:2b

# For coding model:
ollama pull codellama
```

### **Environment Variables**

In Render dashboard → Environment:
- No environment variables needed for Ollama!
- Already configured in `render.yaml`

---

## 💰 Cost Estimate

### **Free Tier:**
- ✅ 750 hours/month free
- ✅ Good for testing
- ⚠️ May be slow with large models
- ⚠️ Spins down after 15 min of inactivity

### **Starter Plan ($7/month):**
- ✅ Always running
- ✅ Better performance
- ✅ 512MB RAM
- ✅ Recommended for production

### **Standard Plan ($25/month):**
- ✅ 2GB RAM
- ✅ Best performance for larger models
- ✅ Multiple concurrent users

---

## 🔧 Troubleshooting

### **Deployment Takes Too Long**
- First deployment downloads ~5GB model - this is normal
- Wait up to 30 minutes for first deployment
- Subsequent deploys are faster (model is cached on disk)

### **Service Fails to Start**
Check Render logs for:
- Memory issues → Upgrade to Starter plan
- Ollama download failed → Rebuild service
- Port binding errors → Make sure Flask uses port 5000

### **Model Not Loading**
- Verify disk is mounted at `/root/.ollama`
- Check disk has at least 10GB space
- Try pulling a smaller model (gemma:2b)

### **"This service is currently unavailable"**
- Free tier spins down after inactivity
- First request after idle takes 30-60 seconds to wake up
- Upgrade to paid plan for always-on service

### **Slow Responses**
- Free tier has limited CPU/RAM
- Try smaller model: `ollama pull gemma:2b`
- Upgrade to Starter ($7) or Standard ($25) plan

---

## 🚀 Making Updates

After deployment, any changes you push to GitHub will auto-deploy:

```powershell
# Make your changes
git add .
git commit -m "Update chatbot"
git push
```

Render automatically rebuilds and redeploys! ✨

---

## 📊 Monitoring

In Render dashboard you can:
- ✅ View real-time logs
- ✅ Monitor resource usage
- ✅ See deployment history
- ✅ Check health status
- ✅ View traffic metrics

---

## 🔒 Security Notes

- ✅ No API keys needed (Ollama is local)
- ✅ HTTPS enabled by default
- ✅ Environment isolated
- ✅ Automatic SSL certificates

---

## 🌐 Custom Domain (Optional)

To use your own domain:
1. Go to Render dashboard → Settings
2. Add custom domain
3. Update DNS records as instructed
4. SSL certificate auto-generates

---

## ⚡ Performance Tips

1. **Use smaller models for free tier:**
   - `gemma:2b` (1.5GB) - Very fast
   - `llama3.2:1b` (1.3GB) - Ultra-fast

2. **Upgrade for better performance:**
   - Starter plan for personal use
   - Standard plan for multiple users

3. **Cache frequently used responses:**
   - Already implemented in the code!

4. **Monitor resource usage:**
   - Check Render metrics
   - Upgrade if hitting limits

---

## 📞 Support

- **Render Support:** https://render.com/docs
- **Ollama Docs:** https://ollama.com/docs
- **Your Repo Issues:** https://github.com/SoumyaBokare/Ipd_Chatbot/issues

---

## ✅ Success Checklist

- [ ] Render account created
- [ ] Repository connected
- [ ] Docker runtime selected
- [ ] Disk configured (10GB)
- [ ] Service deployed successfully
- [ ] Health check passing
- [ ] Chatbot accessible online
- [ ] Models loading correctly

🎉 **Congratulations! Your chatbot is now live!**
