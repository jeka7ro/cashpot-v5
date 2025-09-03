
# 🚀 CASHPOT V5 - Render Deployment Instructions

## ✅ AUTOMATIC STEPS COMPLETED:
- ✅ render.yaml configuration created
- ✅ requirements.txt created
- ✅ All files ready for deployment

## 📋 MANUAL STEPS REQUIRED:

### 1. Deploy to Render
1. Go to: https://render.com/
2. Sign in with your account (jeka7ro@gmail.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository: jeka7ro/cashpot-v5
5. Configure:
   - **Name:** cashpot-backend
   - **Environment:** Python 3
   - **Build Command:** pip install -r requirements.txt
   - **Start Command:** python server.py
   - **Root Directory:** backend

### 2. Environment Variables
Add these environment variables in Render:
- **MONGO_URL:** Your MongoDB Atlas connection string
- **JWT_SECRET_KEY:** (auto-generated)
- **JWT_ALGORITHM:** HS256
- **JWT_ACCESS_TOKEN_EXPIRE_MINUTES:** 30
- **CORS_ORIGINS:** ["https://jeka7ro.github.io", "https://jeka7ro.github.io/cashpot-v5"]
- **SECRET_KEY:** (auto-generated)
- **ENVIRONMENT:** production
- **DEBUG:** False

### 3. MongoDB Atlas Setup
1. Go to: https://cloud.mongodb.com/
2. Create a new cluster (FREE tier)
3. Create database user: cashpot_admin
4. Whitelist IP: 0.0.0.0/0 (all IPs)
5. Get connection string
6. Use it as MONGO_URL in Render

### 4. Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Copy the backend URL
4. Use it as BACKEND_URL secret in GitHub

## 🎉 RESULT:
- **Backend:** https://cashpot-backend.onrender.com (or your custom name)
- **Frontend:** https://jeka7ro.github.io/cashpot-v5

---
**🎰 CASHPOT V5 - Ready for Render deployment! 🚀**
