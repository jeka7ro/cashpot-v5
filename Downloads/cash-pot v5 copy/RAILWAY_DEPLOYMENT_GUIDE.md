# 🚂 Railway Deployment Guide

## Deploy CASHPOT V5 Backend pe Railway

### Pasul 1: Pregătire
- ✅ Codul este gata pentru deploy
- ✅ Dockerfile configurat
- ✅ railway.json configurat
- ✅ Environment variables configurate

### Pasul 2: Deploy pe Railway

1. **Accesează Railway Dashboard**
   - Mergi la https://railway.app/
   - Login cu GitHub account

2. **Creează un nou proiect**
   - Click "New Project"
   - Selectează "Deploy from GitHub repo"
   - Alege repository-ul: `jeka7ro/cashpot-v5`

3. **Configurează serviciul**
   - Railway va detecta automat Dockerfile-ul
   - Setează următoarele variabile de mediu:

   ```
   MONGO_URL=mongodb://mongo:szBQQmkgcjGuFGBrAMKtVToeUYrjpY0t@turntable.proxy.rlwy.net:26901
   JWT_SECRET_KEY=CashPot2024-SuperSecret-JWT-Key-12345
   CORS_ORIGINS=["https://jeka7ro.github.io"]
   DB_NAME=cashpot_v5
   DEBUG=false
   ENVIRONMENT=production
   JWT_ALGORITHM=HS256
   SECRET_KEY=your-app-secret-key-67890
   ```

4. **Deploy**
   - Click "Deploy"
   - Așteaptă ca build-ul să se termine
   - Railway va genera un URL pentru aplicația ta

### Pasul 3: Testare

1. **Verifică health check**
   - Accesează `https://your-app.railway.app/api/health`
   - Ar trebui să returneze: `{"status": "healthy", "message": "CASHPOT V5 Backend is running"}`

2. **Testează conexiunea cu frontend-ul**
   - Frontend-ul va folosi automat noul URL
   - Verifică că toate funcționalitățile merg

### Pasul 4: Actualizare GitHub Pages

După ce ai URL-ul de la Railway:

1. **Actualizează frontend-ul**
   - Modifică `frontend/src/app.js`
   - Schimbă `BACKEND_URL` cu noul URL de la Railway

2. **Commit și push**
   ```bash
   git add .
   git commit -m "Update backend URL for Railway deployment"
   git push origin main
   ```

3. **GitHub Actions va face deploy automat**
   - Frontend-ul va fi actualizat pe GitHub Pages
   - Va folosi noul backend de la Railway

### Pasul 5: Monitorizare

- **Railway Dashboard**: Monitorizează logs și performanță
- **GitHub Actions**: Verifică statusul deploy-ului frontend
- **GitHub Pages**: Testează aplicația live

## 🔧 Troubleshooting

### Dacă deploy-ul eșuează:
1. Verifică logs-urile în Railway Dashboard
2. Verifică că toate variabilele de mediu sunt setate corect
3. Verifică că MongoDB URL-ul este valid

### Dacă frontend-ul nu se conectează:
1. Verifică CORS_ORIGINS în Railway
2. Verifică că backend-ul rulează (health check)
3. Verifică că URL-ul este corect în frontend

## 📊 Status Final

- ✅ **Backend**: Deploy pe Railway
- ✅ **Frontend**: Deploy pe GitHub Pages
- ✅ **Database**: MongoDB Atlas
- ✅ **CI/CD**: GitHub Actions

Aplicația va fi complet funcțională cu backend-ul pe Railway și frontend-ul pe GitHub Pages!
