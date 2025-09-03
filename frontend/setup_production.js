#!/usr/bin/env node
/**
 * Script to setup frontend for production deployment
 * This will help configure the frontend for online deployment
 */

const fs = require('fs');
const path = require('path');

function updateApiUrl(backendUrl) {
    console.log('🔧 Updating API URL in frontend...');
    
    const appJsPath = path.join(__dirname, 'src', 'app.js');
    
    if (!fs.existsSync(appJsPath)) {
        console.error('❌ app.js not found!');
        return false;
    }
    
    // Read the file
    let content = fs.readFileSync(appJsPath, 'utf8');
    
    // Update BACKEND_URL
    const backendUrlRegex = /const BACKEND_URL = ['"`][^'"`]*['"`];/;
    const newBackendUrl = `const BACKEND_URL = '${backendUrl}';`;
    
    if (backendUrlRegex.test(content)) {
        content = content.replace(backendUrlRegex, newBackendUrl);
        console.log('✅ Updated BACKEND_URL');
    } else {
        console.log('⚠️  BACKEND_URL not found, adding it...');
        // Add at the top after imports
        const importEnd = content.indexOf(';', content.indexOf('import')) + 1;
        content = content.slice(0, importEnd) + '\n' + newBackendUrl + '\n' + content.slice(importEnd);
    }
    
    // Update API constant
    const apiRegex = /const API = ['"`][^'"`]*['"`];/;
    const newApi = `const API = '${backendUrl}/api';`;
    
    if (apiRegex.test(content)) {
        content = content.replace(apiRegex, newApi);
        console.log('✅ Updated API constant');
    } else {
        console.log('⚠️  API constant not found, adding it...');
        const backendUrlEnd = content.indexOf(';', content.indexOf('BACKEND_URL')) + 1;
        content = content.slice(0, backendUrlEnd) + '\n' + newApi + '\n' + content.slice(backendUrlEnd);
    }
    
    // Write back to file
    fs.writeFileSync(appJsPath, content);
    console.log('✅ Frontend API configuration updated');
    
    return true;
}

function createNetlifyConfig() {
    console.log('🔧 Creating Netlify configuration...');
    
    const netlifyConfig = `[build]
  publish = "build"
  command = "npm install && npm run build"

[build.environment]
  NODE_VERSION = "18"

# Redirect all routes to index.html for SPA
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

# API routes (if you have serverless functions)
[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200

# Static files
[[redirects]]
  from = "/favicon.ico"
  to = "/favicon.ico"
  status = 200

[[redirects]]
  from = "/manifest.json"
  to = "/manifest.json"
  status = 200

[[redirects]]
  from = "/static/*"
  to = "/static/:splat"
  status = 200

# Security headers
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

# Cache static files
[[headers]]
  for = "/static/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"`;

    fs.writeFileSync(path.join(__dirname, 'netlify.toml'), netlifyConfig);
    console.log('✅ Created netlify.toml');
}

function createVercelConfig() {
    console.log('🔧 Creating Vercel configuration...');
    
    const vercelConfig = {
        "version": 2,
        "builds": [
            {
                "src": "package.json",
                "use": "@vercel/static-build",
                "config": {
                    "distDir": "build"
                }
            }
        ],
        "routes": [
            {
                "src": "/favicon.ico",
                "dest": "/favicon.ico"
            },
            {
                "src": "/manifest.json",
                "dest": "/manifest.json"
            },
            {
                "src": "/static/(.*)",
                "dest": "/static/$1"
            },
            {
                "handle": "filesystem"
            },
            {
                "src": "/(.*)",
                "dest": "/index.html"
            }
        ],
        "buildCommand": "npm install && npm run build",
        "outputDirectory": "build"
    };

    fs.writeFileSync(path.join(__dirname, 'vercel.json'), JSON.stringify(vercelConfig, null, 2));
    console.log('✅ Created vercel.json');
}

function createDeploymentScript() {
    console.log('🔧 Creating deployment script...');
    
    const deployScript = `#!/bin/bash
# CASHPOT Frontend Deployment Script

echo "🚀 Starting CASHPOT Frontend Deployment..."

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Build for production
echo "🔨 Building for production..."
npm run build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo "📁 Build files are in the 'build' directory"
    echo "🌐 Ready for deployment to Netlify or Vercel"
else
    echo "❌ Build failed!"
    exit 1
fi

echo "🎉 Deployment preparation completed!"`;

    fs.writeFileSync(path.join(__dirname, 'deploy.sh'), deployScript);
    
    // Make it executable
    fs.chmodSync(path.join(__dirname, 'deploy.sh'), '755');
    console.log('✅ Created deploy.sh script');
}

function main() {
    console.log('🚀 CASHPOT Frontend Production Setup');
    console.log('=' * 50);
    
    // Get backend URL from user
    const backendUrl = process.argv[2];
    
    if (!backendUrl) {
        console.log('❌ Please provide backend URL as argument');
        console.log('Usage: node setup_production.js <backend-url>');
        console.log('Example: node setup_production.js https://your-backend.railway.app');
        process.exit(1);
    }
    
    // Update API configuration
    if (!updateApiUrl(backendUrl)) {
        process.exit(1);
    }
    
    // Create deployment configurations
    createNetlifyConfig();
    createVercelConfig();
    createDeploymentScript();
    
    console.log('\n🎉 Frontend production setup completed!');
    console.log('\n📋 Next steps:');
    console.log('1. Deploy to Netlify:');
    console.log('   - Connect your GitHub repository to Netlify');
    console.log('   - Set build command: npm install && npm run build');
    console.log('   - Set publish directory: build');
    console.log('');
    console.log('2. Deploy to Vercel:');
    console.log('   - Connect your GitHub repository to Vercel');
    console.log('   - Vercel will auto-detect the configuration');
    console.log('');
    console.log('3. Update CORS settings in backend to include your frontend domain');
    
    console.log('\n📁 Files created/updated:');
    console.log('- src/app.js (updated API URLs)');
    console.log('- netlify.toml (Netlify configuration)');
    console.log('- vercel.json (Vercel configuration)');
    console.log('- deploy.sh (deployment script)');
}

if (require.main === module) {
    main();
}

module.exports = { updateApiUrl, createNetlifyConfig, createVercelConfig };
