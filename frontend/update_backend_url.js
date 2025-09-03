#!/usr/bin/env node
/**
 * Script to update backend URL in frontend for Render deployment
 */

const fs = require('fs');
const path = require('path');

function updateBackendUrl(backendUrl) {
    console.log('🔧 Updating backend URL in frontend...');
    
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
    console.log('✅ Frontend backend URL updated');
    
    return true;
}

function createEnvFile(backendUrl) {
    console.log('🔧 Creating .env file for build...');
    
    const envContent = `REACT_APP_BACKEND_URL=${backendUrl}
GENERATE_SOURCEMAP=false
`;
    
    const envPath = path.join(__dirname, '.env');
    fs.writeFileSync(envPath, envContent);
    console.log('✅ Created .env file');
}

function main() {
    const backendUrl = process.argv[2];
    
    if (!backendUrl) {
        console.log('❌ Please provide backend URL as argument');
        console.log('Usage: node update_backend_url.js <backend-url>');
        console.log('Example: node update_backend_url.js https://cashpot-backend.onrender.com');
        process.exit(1);
    }
    
    console.log('🚀 Updating frontend for Render backend...');
    console.log(`Backend URL: ${backendUrl}`);
    
    if (!updateBackendUrl(backendUrl)) {
        process.exit(1);
    }
    
    createEnvFile(backendUrl);
    
    console.log('\n🎉 Frontend updated successfully!');
    console.log('\n📋 Next steps:');
    console.log('1. Commit and push your changes');
    console.log('2. GitHub Actions will automatically deploy to GitHub Pages');
    console.log('3. Your app will be available at: https://your-username.github.io/cash-pot-v5-copy');
}

if (require.main === module) {
    main();
}

module.exports = { updateBackendUrl, createEnvFile };
