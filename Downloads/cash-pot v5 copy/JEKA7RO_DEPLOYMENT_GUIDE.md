# 🚀 CASHPOT - Deployment Guide for jeka7ro
## Render Backend + GitHub Pages Frontend

## 📋 Overview

This guide will help you deploy your CASHPOT Gaming Management System with:
- **Backend**: Render (jeka7ro@gmail.com)
- **Frontend**: GitHub Pages (jeka7ro)
- **Database**: MongoDB Atlas (Free tier)

## 🎯 Quick Start

Run the deployment script:
```bash
python3 deploy_to_render.py
```

## 📊 Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- GitHub account (jeka7ro)
- MongoDB Atlas account (free)
- Render account (jeka7ro@gmail.com)

## 🗄️ Database Setup

### 1. MongoDB Atlas
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create free cluster
3. Create database user
4. Get connection string
5. Whitelist IP addresses

## 🔧 Backend Deployment (Render)

### 1. Access Render
1. Go to [Render](https://render.com/)
2. Sign in with: **jeka7ro@gmail.com**
3. Click "New +" → "Web Service"

### 2. Connect Repository
1. Click "Connect a repository"
2. Select your GitHub repository
3. Choose the repository with CASHPOT code

### 3. Configure Service
- **Name**: `cashpot-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python server.py`
- **Plan**: `Free`

### 4. Environment Variables
Add these environment variables in Render dashboard:

```
MONGO_URL=your_mongodb_atlas_connection_string
DB_NAME=casino_management
JWT_SECRET_KEY=your_random_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["https://jeka7ro.github.io", "https://jeka7ro.github.io/cashpot-v5"]
SECRET_KEY=your_random_secret_key_here
ENVIRONMENT=production
DEBUG=false
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@cashpot.com
ADMIN_PASSWORD=admin123
API_V1_STR=/api
PROJECT_NAME=CASHPOT Gaming Management System
```

### 5. Deploy
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Note the service URL (e.g., https://cashpot-backend.onrender.com)

## 🌐 Frontend Deployment (GitHub Pages)

### 1. Enable GitHub Pages
1. Go to your GitHub repository
2. Click "Settings" tab
3. Scroll to "Pages" section
4. Set source to "GitHub Actions"

### 2. Add Repository Secret
1. Go to "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret"
3. Name: `BACKEND_URL`
4. Value: Your Render backend URL (from step 5 above)

### 3. Deploy
1. Push your code to main/master branch
2. GitHub Actions will automatically build and deploy
3. Your site will be available at: **https://jeka7ro.github.io/cashpot-v5**

## 🧪 Testing

### Test Backend
```bash
curl https://your-backend-url.onrender.com/api/health
```

### Test Frontend
Visit: **https://jeka7ro.github.io/cashpot-v5**

### Full Test
```bash
python3 test_render_deployment.py
```

## 🔧 Troubleshooting

### Render Issues
- **Service not starting**: Check Render logs
- **Build failing**: Check build logs in Render dashboard
- **Database connection failed**: Verify MONGO_URL environment variable
- **CORS errors**: Update CORS_ORIGINS with correct frontend URL

### GitHub Pages Issues
- **Build failing**: Check GitHub Actions logs
- **API calls failing**: Verify BACKEND_URL secret is set correctly

### Common Solutions
1. **Render backend sleeping**: Free tier sleeps after 15min inactivity
2. **CORS issues**: Update CORS_ORIGINS in Render
3. **Build failures**: Check Node.js version in workflow

## 📁 File Structure

```
├── backend/
│   ├── render.yaml          # Render configuration
│   ├── export_data.py       # Export local data
│   ├── import_data.py       # Import to Atlas
│   └── backup_data.py       # Backup cloud data
├── frontend/
│   ├── package.json         # Updated with jeka7ro homepage
│   ├── public/CNAME         # GitHub Pages CNAME
│   ├── .env                 # Environment variables
│   └── update_backend_url.js # Update backend URL
├── .github/workflows/
│   └── deploy.yml           # GitHub Actions workflow
├── deploy_to_render.py      # Main deployment script
├── update_frontend_for_render.py # Update frontend
├── test_render_deployment.py # Test deployment
├── check_render_status.py   # Check status
├── backup_cloud_data.py     # Backup data
└── JEKA7RO_DEPLOYMENT_GUIDE.md # This file
```

## 🔐 Security Notes

- Change default admin password after first login
- Use strong passwords for database users
- Regularly backup your data
- Monitor application logs

## 📈 Monitoring

### Render
- Dashboard → Logs
- Monitor CPU, Memory usage
- Check deployment status

### GitHub Pages
- Actions tab → Workflow runs
- Check build logs
- Monitor deployment status

### MongoDB Atlas
- Dashboard → Monitoring
- Check connection metrics
- Monitor database performance

## 🔄 Updates

### Code Updates
1. Push changes to GitHub
2. Render auto-deploys backend
3. GitHub Actions auto-deploys frontend
4. Test before announcing

### Database Updates
1. Backup existing data
2. Apply migrations
3. Test thoroughly

## 💰 Costs

- **Render**: Free tier (512MB RAM, sleeps after 15min)
- **GitHub Pages**: Free
- **MongoDB Atlas**: Free tier (512MB storage)

## 🆘 Support

- **Render**: [Documentation](https://render.com/docs)
- **GitHub Pages**: [Documentation](https://docs.github.com/en/pages)
- **MongoDB Atlas**: [Documentation](https://docs.atlas.mongodb.com/)

## 🎉 Success!

Your CASHPOT application will be live at:
- **Frontend**: **https://jeka7ro.github.io/cashpot-v5**
- **Backend**: **https://your-backend-url.onrender.com**

Multiple users can now access your application with shared data stored in MongoDB Atlas!

---

**🚀 Ready to deploy? Run: `python3 deploy_to_render.py`**

## 📞 Quick Commands

```bash
# Deploy everything
python3 deploy_to_render.py

# Update frontend with backend URL
python3 update_frontend_for_render.py

# Test deployment
python3 test_render_deployment.py

# Check status
python3 check_render_status.py

# Backup data
python3 backup_cloud_data.py
```
