# 🚀 Railway Deployment Manual - Cash Pot V5

## 📋 Pași pentru Deployment pe Railway

### 1. Pregătire Repository
✅ **COMPLETAT** - Codul a fost pus pe GitHub la: `https://github.com/jeka7ro/cashpot-v5`

### 2. Accesare Railway
1. Mergi la: https://railway.app/
2. Login cu GitHub account
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Selectează repository-ul: `jeka7ro/cashpot-v5`

### 3. Configurare Backend Service
1. Railway va detecta automat `server.py` și `requirements.txt`
2. Va crea un service Python automat
3. Va instala dependențele din `requirements.txt`

### 4. Adăugare MongoDB Service
1. În dashboard-ul Railway, click "New Service"
2. Select "Database" → "MongoDB"
3. Railway va crea un cluster MongoDB automat

### 5. Configurare Environment Variables
Adaugă următoarele variabile în Railway dashboard:

```bash
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here-12345-67890
JWT_ALGORITHM=HS256
SECRET_KEY=your-app-secret-key-67890-12345

# Environment
ENVIRONMENT=production
DEBUG=false

# Database
DB_NAME=cashpot_v5

# CORS (va fi setat automat când frontend-ul va fi pe GitHub Pages)
CORS_ORIGINS=["https://jeka7ro.github.io"]

# Admin User
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@cashpot.com
ADMIN_PASSWORD=admin123
```

### 6. Setare MongoDB URL
1. În dashboard-ul Railway, click pe MongoDB service
2. Copiază connection string-ul
3. Adaugă variabila: `MONGO_URL=mongodb+srv://...`

### 7. Deploy
1. Railway va face deploy automat când detectează schimbări
2. Sau click "Deploy" manual în dashboard

### 8. Verificare Deployment
- Backend URL: `https://your-app-name.up.railway.app`
- Health check: `https://your-app-name.up.railway.app/health`
- API docs: `https://your-app-name.up.railway.app/docs`

### 9. Configurare Frontend (GitHub Pages)
1. Mergi la repository pe GitHub
2. Settings → Pages
3. Source: "GitHub Actions"
4. Va fi configurat automat prin workflow

### 10. Configurare CORS
După ce frontend-ul este live pe GitHub Pages, actualizează:
```bash
CORS_ORIGINS=["https://jeka7ro.github.io/cashpot-v5"]
```

## 🎯 URL-uri Finale
- **Backend API**: `https://cashpot-v5-production.up.railway.app`
- **Frontend**: `https://jeka7ro.github.io/cashpot-v5`
- **API Documentation**: `https://cashpot-v5-production.up.railway.app/docs`

## 🔧 Verificări Post-Deployment
1. ✅ Backend health check: `/health`
2. ✅ MongoDB connection funcționează
3. ✅ API endpoints răspund
4. ✅ Frontend se conectează la backend
5. ✅ Login funcționează

## 📞 Suport
Dacă întâmpini probleme:
1. Verifică logs în Railway dashboard
2. Verifică environment variables
3. Verifică MongoDB connection
4. Verifică CORS settings

---
**Status**: ✅ Cod pus pe GitHub
**Următorul pas**: Configurare Railway dashboard manual
