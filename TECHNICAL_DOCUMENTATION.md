# CASHPOT V5 - DOCUMENTAȚIE TEHNICĂ COMPLETĂ
## Sistem de Management Gaming Industry

### 📋 PREZENTARE GENERALĂ

**CASHPOT V5** este un sistem complet de management pentru industria gaming, dezvoltat pentru gestionarea operatorilor de slot machines, case de jocuri și furnizori de echipamente gaming.

### 🏗️ ARHITECTURA SISTEMULUI

#### 1.1 Stack Tehnologic
- **Frontend**: React.js 19.0.0 (SPA - Single Page Application)
- **Backend**: FastAPI 0.104.1 (Python)
- **Database**: MongoDB (NoSQL)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **File Storage**: Base64 în database
- **Styling**: CSS custom cu variabile pentru teme (Dark/Light mode)
- **Build Tool**: CRACO (Create React App Configuration Override)
- **Package Manager**: Yarn 1.22.22

#### 1.2 Structura Proiectului
```
cash-pot-v5/
├── backend/
│   └── server.py (FastAPI application - 3627+ linii)
├── frontend/
│   ├── src/
│   │   ├── app.js (React component principal - 22359+ linii)
│   │   ├── app.css (stilizare CSS)
│   │   └── index.js (entry point)
│   ├── public/
│   ├── package.json
│   └── craco.config.js
├── static/ (build files)
├── requirements.txt (Python dependencies)
└── package.json (root dependencies)
```

### 🗄️ BAZA DE DATE - MONGODB

#### 2.1 Conexiune și Configurare
```python
# Configurare MongoDB
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'cashpot_v5')

client = AsyncIOMotorClient(mongo_url)
db = client[DB_NAME]
```

#### 2.2 Colecții Principale
- **users** - Utilizatori și autentificare
- **companies** - Companiile operatori
- **locations** - Locațiile de jocuri
- **providers** - Furnizorii de echipamente
- **cabinets** - Tipurile de cabine
- **game_mixes** - Mixurile de jocuri
- **slot_machines** - Mașinile de slot
- **invoices** - Facturile
- **onjn_reports** - Rapoartele ONJN
- **legal_documents** - Documentele legale
- **metrology** - Datele de metrologie
- **jackpots** - Jackpoturile

### 🔐 AUTENTIFICARE ȘI AUTORIZARE

#### 3.1 Sistem de Roluri
```python
class UserRole(str):
    ADMIN = "admin"      # Acces complet
    MANAGER = "manager"  # Acces limitat
    OPERATOR = "operator" # Acces operator
```

#### 3.2 Permisiuni Granulare
```python
class UserPermissions(BaseModel):
    modules: dict = {
        "dashboard": True,
        "companies": False,
        "locations": False,
        "providers": False,
        "cabinets": False,
        "game_mixes": False,
        "slot_machines": False,
        "invoices": False,
        "onjn_reports": False,
        "legal_documents": False,
        "metrology": False,
        "jackpots": False,
        "users": False
    }
    actions: dict = {
        "companies": {"create": False, "read": False, "update": False, "delete": False}
    }
    accessible_companies: List[str] = []
    accessible_locations: List[str] = []
```

### 🎯 ENTITĂȚI PRINCIPALE

#### 4.1 Company (Companii)
```python
class Company(BaseModel):
    id: str
    name: str                    # Numele companiei
    registration_number: str     # CUI/CIF
    tax_id: str                 # Cod fiscal
    address: str                # Adresa
    phone: str                  # Telefon
    email: str                  # Email
    contact_person: str         # Persoana de contact
    status: str = "active"      # Status
    created_at: datetime
    created_by: str
```

#### 4.2 Location (Locații)
```python
class Location(BaseModel):
    id: str
    name: str                   # Numele locației
    address: str               # Adresa completă
    city: str                  # Orașul
    county: str                # Județul
    country: str = "Romania"   # Țara
    postal_code: str           # Cod poștal
    latitude: Optional[float]  # Latitudine
    longitude: Optional[float] # Longitudine
    company_id: str            # ID-ul companiei
    manager_id: Optional[str]  # Managerul locației
    status: str = "active"
    created_at: datetime
    created_by: str
```

#### 4.3 Provider (Furnizori)
```python
class Provider(BaseModel):
    id: str
    name: str                   # Numele furnizorului
    company_name: str          # Numele companiei
    contact_person: str        # Persoana de contact
    email: str                 # Email
    phone: str                 # Telefon
    address: str               # Adresa
    status: str = "active"
    created_at: datetime
    created_by: str
```

#### 4.4 Cabinet (Cabine)
```python
class Cabinet(BaseModel):
    id: str
    name: str                  # Numele cabinei
    model: Optional[str]       # Modelul
    provider_id: str           # ID-ul furnizorului
    status: str = "active"
    created_at: datetime
    created_by: str
```

#### 4.5 GameMix (Mixuri de Jocuri)
```python
class GameMix(BaseModel):
    id: str
    name: str                  # Numele mix-ului
    description: str           # Descrierea
    provider_id: str           # ID-ul furnizorului
    game_count: int            # Numărul de jocuri
    games: List[str]           # Lista jocurilor
    status: str = "active"
    created_at: datetime
    created_by: str
```

#### 4.6 SlotMachine (Mașini de Slot)
```python
class SlotMachine(BaseModel):
    id: str
    cabinet_id: str            # ID-ul cabinei
    game_mix_id: str           # ID-ul mix-ului
    provider_id: str           # ID-ul furnizorului
    model: str                 # Modelul
    serial_number: str         # Numărul de serie (UNIC)
    denomination: float        # Denominația
    max_bet: float             # Miza maximă
    rtp: float                 # Return to Player %
    gaming_places: int         # Numărul de locuri de joc
    commission_date: Optional[datetime]  # Data comisionării
    invoice_number: Optional[str]        # Numărul facturii
    status: str = "active"     # active/inactive
    location_id: Optional[str] # ID-ul locației
    production_year: Optional[int]       # Anul producției
    ownership_type: Optional[str]        # "property" sau "rent"
    owner_company_id: Optional[str]      # Compania proprietar
    lease_provider_id: Optional[str]     # Furnizorul pentru închiriere
    lease_contract_number: Optional[str] # Numărul contractului
    created_at: datetime
    created_by: str
```

### 🌐 API ENDPOINTS - FASTAPI

#### 5.1 Autentificare
```python
POST /api/auth/login          # Login utilizator
POST /api/auth/register       # Înregistrare utilizator
GET  /api/auth/me             # Informații utilizator curent
POST /api/auth/logout         # Logout
```

#### 5.2 CRUD Operations pentru fiecare entitate
```python
# Pentru fiecare entitate (companies, locations, providers, etc.)
GET    /api/{entity_type}           # Lista tuturor
POST   /api/{entity_type}           # Creare nouă
GET    /api/{entity_type}/{id}      # Detalii specifice
PUT    /api/{entity_type}/{id}      # Actualizare
DELETE /api/{entity_type}/{id}      # Ștergere
```

#### 5.3 Endpoints Specializate
```python
GET /api/dashboard/stats            # Statistici dashboard
POST /api/slot_machines/bulk-update # Actualizare în masă
GET /api/export/{entity_type}       # Export date
POST /api/import/{entity_type}      # Import date
GET /api/reports/onjn              # Rapoarte ONJN
POST /api/files/upload             # Upload fișiere
```

### 🎨 FRONTEND - REACT COMPONENTS

#### 6.1 Structura Principală
```javascript
// app.js - Componenta principală (22359+ linii)
const App = () => {
  // State management pentru întreaga aplicație
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [activeView, setActiveView] = useState('dashboard');
  const [entities, setEntities] = useState({});
  
  return (
    <AuthProvider>
      <div className={`app ${theme}`}>
        {user ? <Dashboard /> : <LoginForm />}
      </div>
    </AuthProvider>
  );
};
```

#### 6.2 Componente Principale
- **Dashboard** - Tabloul de bord principal
- **LoginForm** - Formular de autentificare
- **EntityTable** - Tabel pentru afișarea entităților
- **EntityForm** - Formular pentru creare/editare
- **FileDisplay** - Component pentru afișarea fișierelor
- **BulkOperations** - Operațiuni în masă
- **ExportImport** - Funcționalități de export/import

#### 6.3 Funcționalități UI
- **Dark/Light Theme** - Comutare temă
- **Responsive Design** - Design adaptabil
- **Sidebar Navigation** - Navigare cu sidebar
- **Modal Dialogs** - Dialoguri modale
- **Toast Notifications** - Notificări toast
- **Bulk Selection** - Selecție în masă
- **Advanced Filtering** - Filtrare avansată
- **Export/Import** - Export/import Excel/JSON

### 📊 DASHBOARD ȘI RAPORTARE

#### 7.1 Statistici Dashboard
- Numărul total de companii
- Numărul total de locații
- Numărul total de slot machines
- Statistici pe categorii
- Grafice și diagrame

#### 7.2 Rapoarte ONJN
- Rapoarte pentru Autoritatea Națională de Jocuri de Noroc
- Export în formate standard
- Validare date conform legislației

#### 7.3 Export/Import
- Export Excel pentru toate entitățile
- Import date din Excel/CSV
- Validare date la import
- Mapping automat câmpuri

### 🔧 CONFIGURARE ȘI DEPLOYMENT

#### 8.1 Variabile de Mediu
```bash
# Backend
MONGO_URL=mongodb://localhost:27017
DB_NAME=cashpot_v5
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
CORS_ORIGINS=["http://localhost:3000"]

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

#### 8.2 Instalare și Rulare
```bash
# Backend
pip install -r requirements.txt
python server.py

# Frontend
cd frontend
npm install
npm start
```

#### 8.3 Build pentru Producție
```bash
# Frontend
npm run build

# Backend
# Deploy FastAPI cu uvicorn sau gunicorn
```

### 🎯 FUNCȚIONALITĂȚI SPECIFICE GAMING

#### 9.1 Management Slot Machines
- Tracking complet al mașinilor de slot
- Gestionare proprietate vs închiriere
- Monitorizare status și locații
- Validare numere de serie unice

#### 9.2 Management Furnizori
- Gestionare furnizori de echipamente
- Tracking contracte de închiriere
- Management cabine și mixuri de jocuri

#### 9.3 Compliance și Legal
- Rapoarte ONJN automate
- Tracking documente legale
- Validare conformitate legislație

#### 9.4 Metrologie
- Gestionare certificate metrologice
- Tracking date comisionare
- Validare echipamente

### 🔒 SECURITATE

#### 10.1 Autentificare
- JWT tokens pentru autentificare
- Password hashing cu bcrypt
- Session management
- Auto-logout la expirare token

#### 10.2 Autorizare
- Permisiuni granulare pe module
- Permisiuni granulare pe acțiuni (CRUD)
- Acces restricționat pe companii/locații
- Role-based access control

#### 10.3 Validare Date
- Validare Pydantic pe backend
- Sanitizare input utilizator
- Protecție XSS și CSRF
- Rate limiting pe API

### 📱 RESPONSIVE DESIGN

#### 11.1 Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

#### 11.2 Componente Adaptabile
- Sidebar colapsibil pe mobile
- Tabele cu scroll orizontal
- Modal-uri responsive
- Navigare touch-friendly

### 🚀 PERFORMANȚĂ

#### 12.1 Optimizări Frontend
- Lazy loading componente
- Memoization pentru calculări costisitoare
- Virtual scrolling pentru tabele mari
- Debouncing pentru căutări

#### 12.2 Optimizări Backend
- Pagination pentru liste mari
- Indexuri MongoDB optimizate
- Caching pentru query-uri frecvente
- Async/await pentru I/O operations

### 🧪 TESTARE

#### 13.1 Testare Frontend
- Unit tests cu Jest
- Integration tests
- E2E tests cu Cypress

#### 13.2 Testare Backend
- Unit tests cu pytest
- API tests cu httpx
- Database tests

### 📚 DOCUMENTAȚIE API

#### 14.1 Swagger/OpenAPI
- Documentație API automată
- Interactive API explorer
- Schema validation
- Example requests/responses

### 🔄 CI/CD ȘI DEPLOYMENT

#### 15.1 GitHub Actions
- Build automat
- Test automat
- Deploy automat

#### 15.2 Docker Support
- Dockerfile pentru backend
- Docker Compose pentru development
- Multi-stage builds

### 📈 MONITORING ȘI LOGGING

#### 16.1 Logging
- Structured logging
- Log levels configurabile
- Error tracking

#### 16.2 Monitoring
- Health checks
- Performance metrics
- Error monitoring

---

## 🎯 CONCLUZIE

CASHPOT V5 este un sistem complet și robust pentru managementul industriei gaming, cu o arhitectură modernă, scalabilă și sigură. Sistemul oferă funcționalități complete pentru gestionarea tuturor aspectelor unei operațiuni gaming, de la managementul echipamentelor până la raportarea către autorități.

**Caracteristici cheie:**
- ✅ Arhitectură modernă (React + FastAPI + MongoDB)
- ✅ Securitate avansată (JWT + bcrypt + RBAC)
- ✅ Interface intuitivă și responsive
- ✅ Funcționalități complete pentru gaming industry
- ✅ Rapoarte ONJN automate
- ✅ Export/Import Excel
- ✅ Dark/Light theme
- ✅ Bulk operations
- ✅ Real-time updates
- ✅ Mobile-friendly

**Pentru reproducere completă a aplicației, urmați pașii de configurare și deployment descriși în documentația de deployment inclusă.**
