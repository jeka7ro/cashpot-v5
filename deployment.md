# CASHPOT Gaming Industry Management System
## Documentul de Sarcini și Cerințe de Bază

### 📋 **CERINȚE DE BAZĂ OBLIGATORII**

#### 🎨 **1. DESIGN ȘI AVATARE**
- **Avatare**: Toate avatarele trebuie să fie 68x68 pixeli, perfect rotunde (border-radius: 50%)
- **Shadow**: Umbră consistentă pentru toate avatarele (box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3))
- **Inițiale**: Când nu există imagine, se afișează inițialele (primele două litere sau prima literă din fiecare cuvânt)
- **Avatar Header**: Avatar-ul din header are fundal transparent, fără bordură sau umbră
- **Toggle Dark/Light**: Același stil transparent ca avatar-ul din header
- **Contrast Text**: Toate elementele text folosesc var(--text-primary) și var(--text-secondary) pentru vizibilitate bună în ambele teme

#### 🎰 **2. TABELUL SLOT MACHINES - STRUCTURĂ OBLIGATORIE**

**Ordinea coloanelor (FIXĂ):**
1. **Serial Number** (cu Location dedesubt)
2. **Provider** (cu Cabinet dedesubt) 
3. **Game Mix** (cu Cabinet Model dedesubt)
4. **Property** (detalii proprietate)
5. **Technical Specs** (specificații tehnice)

**Afișare în coloana Property:**
- **Pentru "Property"**: "Numele Companiei + Numărul Facturii"
- **Pentru "Rent"**: "Numele Companiei Provider-ului + Numărul Contractului de Închiriere"
- **IMPORTANT**: Se afișează numele companiei, NU numele provider-ului

#### 📝 **3. FORMULARUL CREATE SLOT MACHINE - CERINȚE**

**Ordinea câmpurilor (FIXĂ):**
1. Provider (dropdown cu format "Provider Name - Company Name")
2. Cabinet (filtrat după Provider selectat)
3. Game Mix (filtrat după Provider selectat)
4. Model (auto-completat din Cabinet selectat, read-only)
5. Production Year (obligatoriu)
6. Ownership Type (Property/Rent cu selecție condițională)
7. Location (obligatoriu)
8. Serial Number (unic per mașină)
9. Restul câmpurilor

**Funcționalități obligatorii:**
- Filtrarea Cabinet-urilor după Provider selectat
- Filtrarea Game Mix-urilor după Provider selectat  
- Auto-completarea câmpului Model din Cabinet
- Dropdown-uri Provider afișează doar numele provider-ului (fără numele companiei)
- Câmpul Model trebuie să fie vizibil și cu același design ca restul câmpurilor

#### 🎨 **4. STILIZARE ȘI TEME**

**Culori și Stiluri:**
- Utilizarea exclusivă a variabilelor CSS (var(--text-primary), var(--text-secondary), etc.)
- **INTERZIS**: Fundal negru hardcodat în formulare
- Persistența temei selectate în localStorage
- Fundal light mode: culoare pastel light blue în loc de negru

#### 🔧 **5. FUNCȚIONALITĂȚI TEHNICE**

**Validări și Comportament:**
- Salvarea Production Year, Ownership Type și Location trebuie să funcționeze corect
- Provider-ul trebuie să se afișeze corect în tabel
- Filtrarea dropdown-urilor trebuie să fie funcțională
- Câmpul Model trebuie să fie auto-completat și read-only

#### ⚠️ **6. RESTRICȚII PENTRU MODIFICĂRI**

**REGULI STRICTE:**
- Asistentul NU poate modifica culorile, stilurile, header-ele sau elementele vizuale fără permisiune explicită
- Asistentul NU poate face îmbunătățiri estetice sau optimizări fără permisiune
- Pentru orice modificare vizuală viitoare, trebuie cerută permisiunea înainte de implementare
- Implementarea se face DOAR pentru cerințele explicit ordonate de utilizator

---

### 📊 **STAREA ACTUALĂ (IMPLEMENTATĂ)**

✅ **Avatare**: Implementate conform specificațiilor (68x68px, rotunde, shadow)  
✅ **Tabelul Slot Machines**: Structura coloanelor implementată corect  
✅ **Property Column**: Afișează numele companiei pentru ambele tipuri  
✅ **Formularul Create**: Ordinea câmpurilor și filtrările implementate  
✅ **Model Field**: Auto-completare și design implementate  
✅ **Provider Dropdowns**: Afișează doar numele provider-ului implementat  
✅ **Stilizare**: Variabile CSS și persistența temei implementate  
✅ **Funcționalități**: Salvare și afișare corectă implementate  

---

### 🎯 **CONCLUZIE**

Aceste cerințe reprezintă **STANDARDUL DE BAZĂ** pentru sistemul CASHPOT. Orice modificare viitoare trebuie să respecte aceste specificații ca punct de plecare obligatoriu.

**Data actualizării:** 21 Ianuarie 2025  
**Status:** Cerințe de Bază Confirmate și Implementate