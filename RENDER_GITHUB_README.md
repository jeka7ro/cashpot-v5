# 🚀 CASHPOT - Render Backend + GitHub Pages Frontend

## 📋 Overview

This setup deploys your CASHPOT Gaming Management System with:
- **Backend**: Render (Free tier)
- **Frontend**: GitHub Pages (Free)
- **Database**: MongoDB Atlas (Free tier)

## 🎯 Quick Start

Run the setup script:
```bash
python3 setup_render_github.py
```

This will guide you through the entire process.

## 📊 Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- GitHub account
- MongoDB Atlas account (free)

## 🗄️ Database Setup

### 1. MongoDB Atlas
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Create free cluster
3. Create database user
4. Get connection string
5. Whitelist IP addresses

## 🔧 Backend Deployment (Render)

### 1. Deploy to Render
1. Go to [Render](https://render.com/)
2. Sign up with GitHub
3. Create new Web Service
4. Connect your repository
5. Configure:
   - **Name**: cashpot-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server.py`
   - **Plan**: Free

### 2. Environment Variables
Add these in Render dashboard:
```
MONGO_URL=your_mongodb_atlas_connection_string
DB_NAME=casino_management
JWT_SECRET_KEY=generate_random_string
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["https://your-username.github.io", "https://your-username.github.io/cash-pot-v5-copy"]
SECRET_KEY=generate_random_string
ENVIRONMENT=production
DEBUG=false
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@cashpot.com
ADMIN_PASSWORD=admin123
API_V1_STR=/api
PROJECT_NAME=CASHPOT Gaming Management System
```

### 3. Deploy
Click "Create Web Service" and wait for deployment.

## 🌐 Frontend Deployment (GitHub Pages)

### 1. Enable GitHub Pages
1. Go to repository Settings
2. Scroll to Pages section
3. Set source to "GitHub Actions"

### 2. Add Repository Secret
1. Go to Settings → Secrets and variables → Actions
2. Add new secret:
   - **Name**: `BACKEND_URL`
   - **Value**: Your Render backend URL

### 3. Deploy
1. Push code to main/master branch
2. GitHub Actions will auto-deploy
3. Site available at: `https://your-username.github.io/cash-pot-v5-copy`

## 🧪 Testing

### Test Backend
```bash
curl https://your-backend-url.onrender.com/api/health
```

### Test Frontend
Visit your GitHub Pages URL

### Full Test
```bash
python3 test_render_github.py
```

## 🔧 Troubleshooting

### Backend Issues
- **Service not starting**: Check Render logs
- **Database connection failed**: Verify MONGO_URL
- **CORS errors**: Update CORS_ORIGINS with correct frontend URL

### Frontend Issues
- **Build failing**: Check GitHub Actions logs
- **API calls failing**: Verify BACKEND_URL secret
- **404 errors**: Check GitHub Pages settings

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
│   ├── update_backend_url.js # Update backend URL
│   └── package.json         # Updated with homepage
├── .github/workflows/
│   └── deploy.yml           # GitHub Actions workflow
├── setup_render_github.py   # Main setup script
├── test_render_github.py    # Test deployment
└── RENDER_GITHUB_README.md  # This file
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
- **Frontend**: `https://your-username.github.io/cash-pot-v5-copy`
- **Backend**: `https://your-backend-url.onrender.com`

Multiple users can now access your application with shared data stored in MongoDB Atlas!

---

**🚀 Ready to deploy? Run: `python3 setup_render_github.py`**
