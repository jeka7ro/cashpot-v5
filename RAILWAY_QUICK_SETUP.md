# 🚀 RAILWAY SETUP RAPID - 5 MINUTE

## ✅ Backend-ul funcționează deja pe Railway!
**URL:** https://cashpot-v5-production.up.railway.app/health

## 🔧 ULTIMELE 3 PAȘI (5 minute):

### 1. Adaugă MongoDB (2 minute)
1. Mergi pe: https://railway.app/dashboard
2. Click pe proiectul `cashpot-v5`
3. Click "New" → "Database" → "MongoDB"
4. Copiază connection string-ul (va arăta ca `mongodb+srv://...`)

### 2. Setează variabilele de mediu (2 minute)
1. În același proiect, click pe "Variables"
2. Adaugă aceste variabile:

```
MONGO_URL = [connection string-ul de la MongoDB]
JWT_SECRET_KEY = your-super-secret-jwt-key-here-12345-67890
JWT_ALGORITHM = HS256
SECRET_KEY = your-app-secret-key-67890-12345
ENVIRONMENT = production
DEBUG = false
CORS_ORIGINS = ["https://jeka7ro.github.io"]
```

### 3. Redeploy (1 minut)
1. Click "Deploy" sau "Redeploy"
2. Așteaptă 2-3 minute
3. Testează: https://cashpot-v5-production.up.railway.app/health

## 🎉 GATA! Aplicația va fi complet funcțională!

**Backend-ul este deja LIVE și funcționează!** Doar MongoDB-ul lipsește.
