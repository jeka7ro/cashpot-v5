
# 🌐 GitHub Pages Setup Instructions

## 1. Enable GitHub Pages in Repository Settings

1. Go to your GitHub repository
2. Click on "Settings" tab
3. Scroll down to "Pages" section (in the left sidebar)
4. Under "Source", select "GitHub Actions"
5. Click "Save"

## 2. Add Repository Secret

1. In your repository, go to "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret"
3. Name: `BACKEND_URL`
4. Value: Your Render backend URL (e.g., https://cashpot-backend.onrender.com)
5. Click "Add secret"

## 3. Push Code to Trigger Deployment

1. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Setup GitHub Pages deployment"
   git push origin main
   ```

2. Go to "Actions" tab in your repository
3. Watch the deployment workflow run
4. Once complete, your site will be available at: https://jeka7ro.github.io/cashpot-v5

## 4. Troubleshooting

### If deployment fails:
- Check the Actions tab for error logs
- Verify that BACKEND_URL secret is set correctly
- Make sure the workflow file is in `.github/workflows/deploy.yml`

### If site shows 404:
- Wait a few minutes for GitHub Pages to propagate
- Check that the deployment workflow completed successfully
- Verify the repository is public (required for free GitHub Pages)

### If API calls fail:
- Verify BACKEND_URL secret is set correctly
- Check that your Render backend is running
- Verify CORS settings in your backend

## 5. Custom Domain (Optional)

If you want to use a custom domain:
1. Add a CNAME file in frontend/public/ with your domain
2. Update DNS settings to point to jeka7ro.github.io
3. Enable "Enforce HTTPS" in Pages settings

---
**🎉 Once setup is complete, your CASHPOT app will be live at:**
**https://jeka7ro.github.io/cashpot-v5**
