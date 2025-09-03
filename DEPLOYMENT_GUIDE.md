# 🎰 CASHPOT Gaming Management System - Deployment Guide

## 🚀 Quick Start

Pentru a face aplicația accesibilă online cu baza de date comună, rulează:

```bash
python3 deploy_online.py
```

Acest script va te ghida prin întregul proces de deployment.

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm sau yarn
- MongoDB local (pentru exportul datelor)
- Conturi pe platformele de deployment (Railway, Netlify, etc.)

## 🗄️ Database Setup (MongoDB Atlas)

### 1. Creează un cluster MongoDB Atlas
1. Mergi la [MongoDB Atlas](https://cloud.mongodb.com/)
2. Creează un cont gratuit
3. Creează un cluster nou (alege FREE tier)
4. Așteaptă ca cluster-ul să fie gata

### 2. Configurează securitatea
1. **Database User:**
   - Username: `cashpot_admin`
   - Password: [generează o parolă puternică]
   - Database User Privileges: `Read and write to any database`

2. **Network Access:**
   - Adaugă IP-ul tău sau folosește `0.0.0.0/0` pentru toate IP-urile

### 3. Obține connection string-ul
1. Click pe "Connect" pe cluster-ul tău
2. Alege "Connect your application"
3. Copiază connection string-ul
4. Înlocuiește `<password>` cu parola ta
5. Înlocuiește `<dbname>` cu `casino_management`

## 🔧 Backend Deployment

### Opțiunea 1: Railway (Recomandat)

1. **Creează cont Railway:**
   - Mergi la [Railway](https://railway.app/)
   - Sign up cu GitHub

2. **Deploy:**
   - Create new project from GitHub repository
   - Selectează repository-ul tău
   - Railway va detecta automat că este o aplicație Python

3. **Environment Variables:**
   - Adaugă toate variabilele din `backend/.env`
   - Setează `MONGO_URL` cu connection string-ul tău Atlas

4. **Deploy:**
   - Railway va face deploy automat
   - Notează URL-ul backend-ului

### Opțiunea 2: Render

1. **Creează cont Render:**
   - Mergi la [Render](https://render.com/)
   - Sign up cu GitHub

2. **Deploy:**
   - Create new Web Service
   - Connect repository-ul tău
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python server.py`

3. **Environment Variables:**
   - Adaugă toate variabilele din `backend/render.env`

### Opțiunea 3: Heroku

1. **Creează cont Heroku:**
   - Mergi la [Heroku](https://heroku.com/)
   - Creează o aplicație nouă

2. **Deploy:**
   - Connect GitHub repository
   - Enable automatic deploys
   - Add environment variables

## 🌐 Frontend Deployment

### Opțiunea 1: Netlify (Recomandat)

1. **Creează cont Netlify:**
   - Mergi la [Netlify](https://netlify.com/)
   - Sign up cu GitHub

2. **Deploy:**
   - Create new site from Git
   - Selectează repository-ul tău
   - Set build command: `cd frontend && npm install && npm run build`
   - Set publish directory: `frontend/build`

3. **Custom Domain (opțional):**
   - Adaugă un domeniu personalizat

### Opțiunea 2: Vercel

1. **Creează cont Vercel:**
   - Mergi la [Vercel](https://vercel.com/)
   - Sign up cu GitHub

2. **Deploy:**
   - Import repository-ul tău
   - Vercel va detecta automat configurația
   - Deploy automat

### Opțiunea 3: GitHub Pages

1. **Enable GitHub Pages:**
   - Mergi la repository settings
   - Scroll la GitHub Pages
   - Set source to GitHub Actions

2. **Create workflow:**
   - Creează `.github/workflows/deploy.yml`
   - Configurează pentru React build

## 🔐 Security Configuration

### 1. Update CORS Settings
În backend, actualizează CORS origins cu URL-ul frontend-ului tău:

```python
CORS_ORIGINS = [
    "https://your-app.netlify.app",
    "https://your-app.vercel.app"
]
```

### 2. Change Default Passwords
După primul login, schimbă:
- Parola admin-ului
- Parolele utilizatorilor de bază de date

### 3. Environment Variables
Asigură-te că toate variabilele de mediu sunt setate corect:
- `MONGO_URL`: Connection string MongoDB Atlas
- `JWT_SECRET_KEY`: Cheie secretă pentru JWT
- `SECRET_KEY`: Cheie secretă generală

## 📊 Data Migration

### Export Local Data
```bash
cd backend
python3 export_data.py
```

### Import to Atlas
```bash
cd backend
export MONGO_URL="your_atlas_connection_string"
python3 import_data.py
```

## 🧪 Testing

### 1. Test Backend
```bash
curl https://your-backend-url.railway.app/api/health
```

### 2. Test Frontend
- Deschide URL-ul frontend-ului
- Încearcă să te loghezi
- Testează funcționalitățile principale

### 3. Test Multi-User
- Creează mai mulți utilizatori
- Testează accesul simultan
- Verifică că datele sunt sincronizate

## 🔧 Troubleshooting

### Backend Issues
- **Connection refused:** Verifică că backend-ul rulează
- **Database connection failed:** Verifică MONGO_URL
- **CORS errors:** Actualizează CORS origins

### Frontend Issues
- **API calls failing:** Verifică BACKEND_URL în frontend
- **Build errors:** Verifică dependențele Node.js
- **Routing issues:** Verifică configurația SPA

### Database Issues
- **Connection timeout:** Verifică network access în Atlas
- **Authentication failed:** Verifică credentials-urile
- **Data not syncing:** Verifică că import-ul a fost făcut corect

## 📈 Monitoring

### 1. Application Logs
- **Railway:** Dashboard → Logs
- **Render:** Dashboard → Logs
- **Netlify:** Dashboard → Functions → Logs

### 2. Database Monitoring
- **MongoDB Atlas:** Dashboard → Monitoring
- **Metrics:** CPU, Memory, Connections

### 3. Performance
- **Frontend:** Lighthouse audit
- **Backend:** Response times
- **Database:** Query performance

## 🔄 Updates

### 1. Code Updates
1. Push changes to GitHub
2. Platformele vor face auto-deploy
3. Testează înainte de a anunța utilizatorii

### 2. Database Updates
1. Backup datele existente
2. Aplică migrațiile
3. Testează înainte de a face live

## 📞 Support

Dacă întâmpini probleme:
1. Verifică logs-urile
2. Consultă documentația platformei
3. Verifică configurația environment variables
4. Testează local înainte de a face deploy

## 🎯 Best Practices

1. **Security:**
   - Folosește HTTPS
   - Actualizează parolele default
   - Monitorizează accesul

2. **Performance:**
   - Optimizează query-urile
   - Folosește caching
   - Monitorizează resursele

3. **Reliability:**
   - Fă backup-uri regulate
   - Testează înainte de deploy
   - Monitorizează uptime-ul

---

**🎉 Felicitări! Aplicația ta CASHPOT este acum accesibilă online cu baza de date comună!**
