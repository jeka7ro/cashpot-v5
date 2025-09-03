# 🔧 Fix 404 Error - GitHub Pages Setup

## 🚨 Problem
You're seeing: "404 - There isn't a GitHub Pages site here"

## ✅ Solution

### 1. Enable GitHub Pages in Repository Settings

1. Go to your GitHub repository: **https://github.com/jeka7ro/cashpot-v5**
2. Click on **"Settings"** tab
3. Scroll down to **"Pages"** section (in the left sidebar)
4. Under **"Source"**, select **"GitHub Actions"**
5. Click **"Save"**

### 2. Add Repository Secret

1. In your repository, go to **"Settings"** → **"Secrets and variables"** → **"Actions"**
2. Click **"New repository secret"**
3. Name: `BACKEND_URL`
4. Value: Your Render backend URL (e.g., `https://cashpot-backend.onrender.com`)
5. Click **"Add secret"**

### 3. Push Code to Trigger Deployment

```bash
git add .
git commit -m "Setup GitHub Pages deployment"
git push origin main
```

### 4. Check Deployment

1. Go to **"Actions"** tab in your repository
2. Watch the **"Deploy to GitHub Pages"** workflow run
3. Wait for it to complete successfully
4. Your site will be available at: **https://jeka7ro.github.io/cashpot-v5**

## 🔍 Troubleshooting

### If deployment fails:
- Check the **Actions** tab for error logs
- Verify that `BACKEND_URL` secret is set correctly
- Make sure the workflow file is in `.github/workflows/deploy.yml`

### If site still shows 404:
- Wait 5-10 minutes for GitHub Pages to propagate
- Check that the deployment workflow completed successfully
- Verify the repository is **public** (required for free GitHub Pages)

### If API calls fail:
- Verify `BACKEND_URL` secret is set correctly
- Check that your Render backend is running
- Verify CORS settings in your backend

## 📋 Quick Checklist

- [ ] Repository is public
- [ ] GitHub Pages is enabled with "GitHub Actions" source
- [ ] `BACKEND_URL` secret is added
- [ ] Code is pushed to main branch
- [ ] Deployment workflow completed successfully
- [ ] Waited 5-10 minutes for propagation

## 🎉 Success!

Once everything is set up correctly, your CASHPOT app will be live at:
**https://jeka7ro.github.io/cashpot-v5**

---

**Need help? Check the Actions tab for detailed error logs!**
