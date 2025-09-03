from fastapi import FastAPI, APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import uuid
from datetime import datetime, timedelta
import bcrypt
import jwt
from geopy.geocoders import Nominatim
import asyncio
import random
from datetime import date
import requests
import csv
from io import StringIO

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'casino_management')]

# Create the main app without a prefix
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001", "http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:8002", "http://127.0.0.1:8002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
security = HTTPBearer()
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-here')
JWT_ALGORITHM = 'HS256'

# Models
class UserRole(str):
    ADMIN = "admin"
    MANAGER = "manager"
    OPERATOR = "operator"

class UserPermissions(BaseModel):
    # Module access permissions
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
    # Action permissions per module
    actions: dict = {
        "companies": {"create": False, "read": False, "update": False, "delete": False},
        "locations": {"create": False, "read": False, "update": False, "delete": False},
        "providers": {"create": False, "read": False, "update": False, "delete": False},
        "cabinets": {"create": False, "read": False, "update": False, "delete": False},
        "game_mixes": {"create": False, "read": False, "update": False, "delete": False},
        "slot_machines": {"create": False, "read": False, "update": False, "delete": False},
        "invoices": {"create": False, "read": False, "update": False, "delete": False},
        "onjn_reports": {"create": False, "read": False, "update": False, "delete": False},
        "legal_documents": {"create": False, "read": False, "update": False, "delete": False},
        "metrology": {"create": False, "read": False, "update": False, "delete": False},
        "jackpots": {"create": False, "read": False, "update": False, "delete": False},
        "users": {"create": False, "read": False, "update": False, "delete": False}
    }
    # Accessible companies and locations
    accessible_companies: List[str] = []
    accessible_locations: List[str] = []

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    phone: Optional[str] = None
    password_hash: str
    first_name: str = ""  # Numele
    last_name: str = ""   # Prenumele
    role: str = UserRole.ADMIN
    assigned_locations: List[str] = []  # Location IDs user has access to
    permissions: UserPermissions = Field(default_factory=UserPermissions)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

class UserCreate(BaseModel):
    username: str
    email: str
    phone: Optional[str] = None
    password: str
    first_name: str = ""
    last_name: str = ""
    role: str = UserRole.ADMIN
    assigned_locations: List[str] = []
    permissions: Optional[UserPermissions] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    assigned_locations: Optional[List[str]] = None
    permissions: Optional[UserPermissions] = None
    is_active: Optional[bool] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Company(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    registration_number: str
    tax_id: str
    address: str
    phone: str
    email: str
    website: Optional[str] = None
    contact_person: str
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class CompanyCreate(BaseModel):
    name: str
    registration_number: str
    tax_id: str
    address: str
    phone: str
    email: str
    website: Optional[str] = None
    contact_person: str

class Location(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    address: str
    city: str
    county: str
    country: str = "Romania"
    postal_code: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    company_id: str
    manager_id: Optional[str] = None
    manager_phone: Optional[str] = None
    manager_email: Optional[str] = None
    contact_person_type: Optional[str] = "manual"
    contact_person_id: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class LocationCreate(BaseModel):
    name: str
    address: str
    city: str
    county: str
    country: str = "Romania"
    postal_code: str
    company_id: str
    manager_id: Optional[str] = None
    manager_phone: Optional[str] = None
    manager_email: Optional[str] = None
    contact_person_type: Optional[str] = "manual"
    contact_person_id: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

class Provider(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    company_name: str
    contact_person: str
    email: str
    phone: str
    address: str
    website: Optional[str] = None
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class ProviderCreate(BaseModel):
    name: str
    company_name: str
    contact_person: str
    email: str
    phone: str
    address: str
    website: Optional[str] = None

class GameMix(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    provider_id: str
    game_count: int
    games: List[str]
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class GameMixCreate(BaseModel):
    name: str
    description: str
    provider_id: str
    games: List[str]

class Cabinet(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    model: Optional[str] = None
    provider_id: str
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class CabinetCreate(BaseModel):
    name: str
    model: Optional[str] = None
    provider_id: str

class CabinetUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    provider_id: Optional[str] = None
class SlotMachine(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cabinet_id: str
    game_mix_id: str
    provider_id: str
    model: str
    serial_number: str  # Unique identifier for invoicing
    denomination: float
    max_bet: float
    rtp: float  # Return to Player percentage
    gaming_places: int
    commission_date: Optional[datetime] = None
    invoice_number: Optional[str] = None  # From invoices table
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None
    location_id: Optional[str] = None
    production_year: Optional[int] = None
    # Property fields
    ownership_type: Optional[str] = None  # "property" or "rent"
    owner_company_id: Optional[str] = None  # Company that owns the slot
    lease_provider_id: Optional[str] = None  # Provider for rented slots
    lease_contract_number: Optional[str] = None  # Contract number for rented slots

class SlotMachineCreate(BaseModel):
    cabinet_id: str
    game_mix_id: str
    provider_id: str
    model: str
    serial_number: str
    denomination: float
    max_bet: float
    rtp: float
    gaming_places: int
    commission_date: Optional[datetime] = None
    invoice_number: Optional[str] = None
    status: Optional[str] = "active"
    location_id: Optional[str] = None
    production_year: Optional[int] = None
    # Property fields
    ownership_type: Optional[str] = None  # "property" or "rent"
    owner_company_id: Optional[str] = None  # Company that owns the slot
    lease_provider_id: Optional[str] = None  # Provider for rented slots
    lease_contract_number: Optional[str] = None  # Contract number for rented slots

class SlotMachineUpdate(BaseModel):
    cabinet_id: Optional[str] = None
    game_mix_id: Optional[str] = None
    provider_id: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    denomination: Optional[float] = None
    max_bet: Optional[float] = None
    rtp: Optional[float] = None
    gaming_places: Optional[int] = None
    commission_date: Optional[datetime] = None
    invoice_number: Optional[str] = None
    status: Optional[str] = None
    location_id: Optional[str] = None
    production_year: Optional[int] = None
    # Property fields
    ownership_type: Optional[str] = None  # "property" or "rent"
    owner_company_id: Optional[str] = None  # Company that owns the slot
    lease_provider_id: Optional[str] = None  # Provider for rented slots
    lease_contract_number: Optional[str] = None  # Contract number for rented slots
    # Modification tracking fields
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None

class Attachment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    file_data: str  # base64 encoded file data
    entity_type: str  # users, providers, cabinets, game_mixes, slots, invoices, onjn, legal, metrology, jackpots
    entity_id: str
    uploaded_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AttachmentCreate(BaseModel):
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    file_data: str
    entity_type: str
    entity_id: str

class Invoice(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    invoice_number: str
    company_id: str
    location_id: str
    buyer_id: Optional[str] = None  # ID of the buyer company
    seller_id: Optional[str] = None  # ID of the seller provider
    transaction_type: Optional[str] = None  # rent, buy, sell
    serial_numbers: str  # Space-separated serial numbers
    issue_date: datetime
    due_date: datetime
    amount: float
    currency: str = "EUR"
    status: str = "pending"  # pending, paid, overdue
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class InvoiceCreate(BaseModel):
    invoice_number: str
    company_id: str
    location_id: str
    buyer_id: Optional[str] = None
    seller_id: Optional[str] = None
    transaction_type: Optional[str] = None  # rent, buy, sell
    serial_numbers: str
    issue_date: datetime
    due_date: datetime
    amount: float
    currency: str = "EUR"
    status: str = "pending"
    description: str

class ONJNReport(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    report_number: str
    report_type: str  # monthly, quarterly, annual
    company_id: str
    location_id: str
    report_date: datetime
    submission_date: Optional[datetime] = None
    status: str = "draft"  # draft, submitted, approved, rejected
    equipment_data: dict
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class ONJNReportCreate(BaseModel):
    report_number: str
    report_type: str
    company_id: str
    location_id: str
    report_date: datetime
    equipment_data: dict

class LegalDocument(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    document_type: str  # license, permit, certificate, contract
    company_id: str
    location_id: Optional[str] = None
    issue_date: datetime
    expiry_date: Optional[datetime] = None
    issuing_authority: str
    status: str = "active"  # active, expired, revoked
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class LegalDocumentCreate(BaseModel):
    title: str
    document_type: str
    company_id: str
    location_id: Optional[str] = None
    issue_date: datetime
    expiry_date: Optional[datetime] = None
    issuing_authority: str
    description: str

# Metrology Module
class Metrology(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    serial_number: str  # Links to slot machine
    certificate_number: str
    issue_date: str  # Store as string format YYYY-MM-DD
    issuing_authority: str
    status: str = "active"  # active, expired, pending
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    updated_at: Optional[datetime] = None
    updated_by: Optional[str] = None

class MetrologyCreate(BaseModel):
    serial_number: str
    certificate_number: str
    issue_date: str  # Accept string format YYYY-MM-DD
    issuing_authority: str
    status: Optional[str] = "active"
    description: str

    class Config:
        extra = "forbid"  # Prevent any extra fields

# Jackpot Module
class Jackpot(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    serial_number: str  # Links to slot machine
    jackpot_type: str  # progressive, fixed, mystery
    jackpot_name: str
    increment_rate: float  # percentage
    level_1: Optional[str] = None
    level_2: Optional[str] = None
    level_3: Optional[str] = None
    level_4: Optional[str] = None
    level_5: Optional[str] = None
    last_reset_date: datetime
    next_reset_date: Optional[datetime] = None
    status: str = "active"  # active, inactive, won
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str

class JackpotCreate(BaseModel):
    serial_number: str
    jackpot_type: str
    jackpot_name: str
    increment_rate: float
    level_1: Optional[str] = None
    level_2: Optional[str] = None
    level_3: Optional[str] = None
    level_4: Optional[str] = None
    level_5: Optional[str] = None
    description: str

class ComisionDate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_name: str  # Numele event-ului
    commission_date: datetime  # Data comisiei (selectabilă din calendar)
    serial_numbers: str  # Space-separated serial numbers
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Data creării (automată)
    created_by: str

class ComisionDateCreate(BaseModel):
    event_name: str  # Numele event-ului
    commission_date: datetime  # Data comisiei (selectabilă din calendar)
    serial_numbers: str  # Space-separated serial numbers

class ChangeHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    entity_type: str  # slots, providers, etc.
    entity_id: str
    field_name: str  # status, provider_id, etc.
    old_value: str
    new_value: str
    change_type: str = "Scheduled"  # "Scheduled" or "Manual"
    scheduled_datetime: datetime
    applied_datetime: Optional[datetime] = None
    applied_successfully: Optional[bool] = None
    user_id: str
    user_name: str  # Full name of user
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DashboardStats(BaseModel):
    total_companies: int
    total_locations: int
    active_companies: int
    active_locations: int
    total_providers: int
    total_cabinets: int
    total_slot_machines: int
    active_equipment: int
    total_invoices: int
    total_onjn_reports: int
    total_legal_documents: int
    total_metrology: int
    total_jackpots: int
    total_comision_dates: int
    total_users: int
    recent_activities: List[dict]

# ============= Marketing Module ============= #
class MarketingPayout(BaseModel):
    date: datetime
    location_id: str
    amount: float
    note: Optional[str] = None

class MarketingCampaign(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # tombola | promotion | tournament
    name: str
    description: Optional[str] = None
    locations: List[str] = []
    start_at: datetime
    end_at: datetime
    status: str = "draft"  # draft | active | ended
    payouts: List[MarketingPayout] = []
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Fortune Teller Models
class FortuneRequest(BaseModel):
    slot_serial_number: Optional[str] = None
    user_question: Optional[str] = None

class FortuneResponse(BaseModel):
    fortune: str
    prediction: str
    lucky_number: int
    advice: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Helper functions
def convert_objectid_to_str(data):
    """Convert MongoDB ObjectId to string for JSON serialization"""
    from bson import ObjectId
    
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    return data

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Helper functions for access control
async def check_user_permission(user: User, module: str, action: str) -> bool:
    """Check if user has permission for specific module and action"""
    if user.role == UserRole.ADMIN:
        return True  # Admin has all permissions
    
    # Check if user has access to the module
    if not user.permissions.modules.get(module, False):
        return False
    
    # Check if user has permission for the specific action
    module_actions = user.permissions.actions.get(module, {})
    return module_actions.get(action, False)

async def get_user_accessible_locations(user: User) -> List[str]:
    """Get list of location IDs that user has access to"""
    if user.role == UserRole.ADMIN:
        # Admin sees all locations
        locations = await db.locations.find({}).to_list(1000)
        return [loc["id"] for loc in locations]
    else:
        # Use explicit permissions if available, fallback to assigned_locations
        if user.permissions.accessible_locations:
            return user.permissions.accessible_locations
        # If no explicit permissions, use assigned_locations (which should be restricted)
        return user.assigned_locations if user.assigned_locations else []

async def get_user_accessible_companies(user: User) -> List[str]:
    """Get list of company IDs that user has access to through locations"""
    if user.role == UserRole.ADMIN:
        # Admin sees all companies
        companies = await db.companies.find({}).to_list(1000)
        return [comp["id"] for comp in companies]
    else:
        # Use explicit permissions if available
        if user.permissions.accessible_companies:
            return user.permissions.accessible_companies
        
        # Get companies from accessible locations
        accessible_locations = await get_user_accessible_locations(user)
        if not accessible_locations:
            return []  # No accessible locations = no accessible companies
        
        locations = await db.locations.find({"id": {"$in": accessible_locations}}).to_list(1000)
        company_ids = list(set([loc["company_id"] for loc in locations if "company_id" in loc]))
        return company_ids

async def filter_by_user_access(user: User, query: dict, entity_type: str) -> dict:
    """Add access control filters to query based on user role and locations"""
    if user.role == UserRole.ADMIN:
        return query  # Admin sees everything
    
    if entity_type == "companies":
        accessible_companies = await get_user_accessible_companies(user)
        query["id"] = {"$in": accessible_companies}
    elif entity_type == "locations":
        accessible_locations = await get_user_accessible_locations(user)
        query["id"] = {"$in": accessible_locations}
    elif entity_type in ["cabinets", "slot_machines"]:
        accessible_locations = await get_user_accessible_locations(user)
        query["location_id"] = {"$in": accessible_locations}
    elif entity_type in ["providers", "game_mixes"]:
        # These are accessible to managers but not operators
        if user.role == UserRole.OPERATOR:
            # Operators can only see providers/game_mixes used in their locations
            accessible_locations = await get_user_accessible_locations(user)
            if entity_type == "providers":
                # Get providers used in accessible cabinets
                cabinets = await db.cabinets.find({"location_id": {"$in": accessible_locations}}).to_list(1000)
                provider_ids = list(set([cab["provider_id"] for cab in cabinets if "provider_id" in cab]))
                query["id"] = {"$in": provider_ids}
            elif entity_type == "game_mixes":
                # Get game mixes used in accessible slot machines
                slot_machines = await db.slot_machines.find({}).to_list(1000)
                accessible_slots = []
                for slot in slot_machines:
                    # Check if slot has location_id and if it's in accessible locations
                    if slot.get("location_id") and slot["location_id"] in accessible_locations:
                        accessible_slots.append(slot)
                game_mix_ids = list(set([slot["game_mix_id"] for slot in accessible_slots if "game_mix_id" in slot]))
                query["id"] = {"$in": game_mix_ids}
    elif entity_type in ["invoices", "legal_documents"]:
        accessible_companies = await get_user_accessible_companies(user)
        accessible_locations = await get_user_accessible_locations(user)
        query["$or"] = [
            {"company_id": {"$in": accessible_companies}},
            {"location_id": {"$in": accessible_locations}}
        ]
    elif entity_type == "onjn_reports":
        accessible_companies = await get_user_accessible_companies(user)
        accessible_locations = await get_user_accessible_locations(user)
        query["$and"] = [
            {"company_id": {"$in": accessible_companies}},
            {"location_id": {"$in": accessible_locations}}
        ]
    
    return query

def verify_password(password: str, hashed: str) -> bool:
    try:
        # Ensure inputs are strings
        if not isinstance(password, str):
            password = str(password)
        if not isinstance(hashed, str):
            hashed = str(hashed)
        
        # Use bcrypt directly
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception as e:
        print(f"❌ Error in verify_password: {e}")
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user = await db.users.find_one({"id": user_id})
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return User(**user)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

async def geocode_address(address: str, city: str, country: str = "Romania"):
    try:
        geolocator = Nominatim(user_agent="financial_planner_pro")
        full_address = f"{address}, {city}, {country}"
        location = geolocator.geocode(full_address)
        if location:
            return location.latitude, location.longitude
        return None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None

# Routes
@api_router.post("/auth/register", response_model=dict)
async def register(user_data: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"$or": [{"username": user_data.username}, {"email": user_data.email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    # Create new user
    user_dict = user_data.model_dump()
    user_dict["password_hash"] = hash_password(user_data.password)
    del user_dict["password"]
    # Ensure permissions is always a valid dict
    if not user_dict.get("permissions"):
        from pydantic import parse_obj_as
        user_dict["permissions"] = UserPermissions().model_dump()
    user_obj = User(**user_dict)
    await db.users.insert_one(user_obj.model_dump())
    
    return {"message": "User created successfully", "user_id": user_obj.id}

@api_router.post("/auth/login", response_model=dict)
async def login(user_data: UserLogin):
    print(f"🔍 Login attempt for username: {user_data.username}")
    print(f"🔍 Password received: '{user_data.password}' (length: {len(user_data.password)})")
    print(f"🔍 Password type: {type(user_data.password)}")
    
    user = await db.users.find_one({"username": user_data.username})
    print(f"👤 User found: {user is not None}")
    
    if not user:
        print("❌ User not found")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    print(f"🔐 Hash from database: {user['password_hash']}")
    print(f"🔐 User ID: {user.get('id', 'N/A')}")
    print(f"🔐 Created at: {user.get('created_at', 'N/A')}")
    print(f"🔐 Password verification for user: {user['username']}")
    password_valid = verify_password(user_data.password, user["password_hash"])
    print(f"✅ Password valid: {password_valid}")
    
    if not password_valid:
        print("❌ Password invalid")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not user.get("is_active", True):
        print("❌ Account inactive")
        raise HTTPException(status_code=401, detail="Account is inactive")
    
    print("🎉 Login successful, creating token")
    access_token = create_access_token(data={"sub": user["id"]})
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user": {
            "id": user["id"], 
            "username": user["username"], 
            "first_name": user.get("first_name", ""),
            "last_name": user.get("last_name", ""),
            "role": user["role"]
        }
    }

@api_router.get("/auth/me", response_model=dict)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id, 
        "username": current_user.username, 
        "email": current_user.email, 
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
        "permissions": current_user.permissions.model_dump() if current_user.permissions else None
    }

@api_router.post("/companies", response_model=Company)
async def create_company(company_data: CompanyCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Check if company name already exists
    existing_company = await db.companies.find_one({"name": company_data.name})
    if existing_company:
        raise HTTPException(status_code=400, detail="Company name already exists")
    
    company_dict = company_data.model_dump()
    company_dict["created_by"] = current_user.id
    company_obj = Company(**company_dict)
    
    await db.companies.insert_one(company_obj.model_dump())
    return company_obj

@api_router.get("/companies", response_model=List[Company])
async def get_companies(current_user: User = Depends(get_current_user)):
    query = await filter_by_user_access(current_user, {}, "companies")
    companies = await db.companies.find(query).to_list(1000)
    # Convert ObjectIds to strings
    companies = [convert_objectid_to_str(company) for company in companies]
    return [Company(**company) for company in companies]

@api_router.get("/companies/{company_id}", response_model=Company)
async def get_company(company_id: str, current_user: User = Depends(get_current_user)):
    # Check if user has access to this company
    accessible_companies = await get_user_accessible_companies(current_user)
    if current_user.role != UserRole.ADMIN and company_id not in accessible_companies:
        raise HTTPException(status_code=403, detail="Access denied to this company")
    
    company = await db.companies.find_one({"id": company_id})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return Company(**company)

@api_router.put("/companies/{company_id}", response_model=Company)
async def update_company(company_id: str, company_data: CompanyCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    company = await db.companies.find_one({"id": company_id})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    update_data = company_data.model_dump()
    await db.companies.update_one({"id": company_id}, {"$set": update_data})
    
    updated_company = await db.companies.find_one({"id": company_id})
    return Company(**updated_company)

@api_router.delete("/companies/{company_id}")
async def delete_company(company_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    company = await db.companies.find_one({"id": company_id})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # HARD DELETE - actually remove from database
    await db.companies.delete_one({"id": company_id})
    return {"message": "Company deleted successfully"}

@api_router.post("/companies/bulk-delete")
async def bulk_delete_companies(company_ids: List[str], current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Verify all companies exist
    companies = await db.companies.find({"id": {"$in": company_ids}}).to_list(1000)
    found_ids = {company["id"] for company in companies}
    missing_ids = set(company_ids) - found_ids
    
    if missing_ids:
        raise HTTPException(status_code=404, detail=f"Companies not found: {', '.join(missing_ids)}")
    
    # HARD DELETE - actually remove from database
    result = await db.companies.delete_many({"id": {"$in": company_ids}})
    
    return {"message": f"Successfully deleted {result.deleted_count} companies"}

@api_router.post("/locations", response_model=Location)
async def create_location(location_data: LocationCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Verify company exists
    company = await db.companies.find_one({"id": location_data.company_id})
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")
    
    location_dict = location_data.model_dump()
    location_dict["created_by"] = current_user.id
    
    # If manager_id is provided, get manager details and populate phone/email
    if location_data.manager_id:
        manager = await db.users.find_one({"id": location_data.manager_id})
        if manager:
            location_dict["manager_phone"] = manager.get("phone", "")
            location_dict["manager_email"] = manager.get("email", "")
    
    # Geocode the address
    lat, lng = await geocode_address(location_data.address, location_data.city, location_data.country)
    location_dict["latitude"] = lat
    location_dict["longitude"] = lng
    
    location_obj = Location(**location_dict)
    await db.locations.insert_one(location_obj.model_dump())
    return location_obj

@api_router.get("/locations", response_model=List[Location])
async def get_locations(current_user: User = Depends(get_current_user)):
    query = await filter_by_user_access(current_user, {}, "locations")
    locations = await db.locations.find(query).to_list(1000)
    # Convert ObjectIds to strings
    locations = [convert_objectid_to_str(location) for location in locations]
    return [Location(**location) for location in locations]

@api_router.get("/locations/{location_id}", response_model=Location)
async def get_location(location_id: str, current_user: User = Depends(get_current_user)):
    # Check if user has access to this location
    accessible_locations = await get_user_accessible_locations(current_user)
    if current_user.role != UserRole.ADMIN and location_id not in accessible_locations:
        raise HTTPException(status_code=403, detail="Access denied to this location")
    
    location = await db.locations.find_one({"id": location_id})
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return Location(**location)

@api_router.put("/locations/{location_id}", response_model=Location)
async def update_location(location_id: str, location_data: LocationCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    location = await db.locations.find_one({"id": location_id})
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    update_data = location_data.model_dump()
    
    # If manager_id is provided, get manager details and populate phone/email
    if location_data.manager_id:
        manager = await db.users.find_one({"id": location_data.manager_id})
        if manager:
            update_data["manager_phone"] = manager.get("phone", "")
            update_data["manager_email"] = manager.get("email", "")
    else:
        # Clear manager details if no manager is selected
        update_data["manager_phone"] = None
        update_data["manager_email"] = None
    
    # Geocode the address if changed
    if location_data.address != location.get("address") or location_data.city != location.get("city"):
        lat, lng = await geocode_address(location_data.address, location_data.city, location_data.country)
        update_data["latitude"] = lat
        update_data["longitude"] = lng
    
    await db.locations.update_one({"id": location_id}, {"$set": update_data})
    
    updated_location = await db.locations.find_one({"id": location_id})
    return Location(**updated_location)

@api_router.delete("/locations/{location_id}")
async def delete_location(location_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    location = await db.locations.find_one({"id": location_id})
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    # HARD DELETE - actually remove from database
    await db.locations.delete_one({"id": location_id})
    return {"message": "Location deleted successfully"}

@api_router.post("/locations/bulk-delete")
async def bulk_delete_locations(location_ids: List[str], current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Verify all locations exist
    locations = await db.locations.find({"id": {"$in": location_ids}}).to_list(1000)
    found_ids = {location["id"] for location in locations}
    missing_ids = set(location_ids) - found_ids
    
    if missing_ids:
        raise HTTPException(status_code=404, detail=f"Locations not found: {', '.join(missing_ids)}")
    
    # HARD DELETE - actually remove from database
    result = await db.locations.delete_many({"id": {"$in": location_ids}})
    
    return {"message": f"Successfully deleted {result.deleted_count} locations"}

@api_router.post("/providers", response_model=Provider)
async def create_provider(provider_data: ProviderCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Check if provider name already exists
    existing_provider = await db.providers.find_one({"name": provider_data.name})
    if existing_provider:
        raise HTTPException(status_code=400, detail="Provider name already exists")
    
    provider_dict = provider_data.model_dump()
    provider_dict["created_by"] = current_user.id
    provider_obj = Provider(**provider_dict)
    
    await db.providers.insert_one(provider_obj.model_dump())
    return provider_obj

@api_router.get("/providers", response_model=List[Provider])
async def get_providers(current_user: User = Depends(get_current_user)):
    query = await filter_by_user_access(current_user, {}, "providers")
    providers = await db.providers.find(query).to_list(1000)
    # Convert ObjectIds to strings
    providers = [convert_objectid_to_str(provider) for provider in providers]
    return [Provider(**provider) for provider in providers]

@api_router.get("/providers/{provider_id}", response_model=Provider)
async def get_provider(provider_id: str, current_user: User = Depends(get_current_user)):
    provider = await db.providers.find_one({"id": provider_id})
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return Provider(**provider)

@api_router.put("/providers/{provider_id}", response_model=Provider)
async def update_provider(provider_id: str, provider_data: ProviderCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    provider = await db.providers.find_one({"id": provider_id})
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    update_data = provider_data.model_dump()
    await db.providers.update_one({"id": provider_id}, {"$set": update_data})
    
    updated_provider = await db.providers.find_one({"id": provider_id})
    return Provider(**updated_provider)

@api_router.delete("/providers/{provider_id}")
async def delete_provider(provider_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    provider = await db.providers.find_one({"id": provider_id})
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    # HARD DELETE - actually remove from database
    await db.providers.delete_one({"id": provider_id})
    return {"message": "Provider deleted successfully"}

@api_router.post("/game-mixes", response_model=GameMix)
async def create_game_mix(game_mix_data: GameMixCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Verify provider exists
    provider = await db.providers.find_one({"id": game_mix_data.provider_id})
    if not provider:
        raise HTTPException(status_code=400, detail="Provider not found")
    
    game_mix_dict = game_mix_data.model_dump()
    game_mix_dict["created_by"] = current_user.id
    game_mix_dict["game_count"] = len(game_mix_data.games)
    game_mix_obj = GameMix(**game_mix_dict)
    
    await db.game_mixes.insert_one(game_mix_obj.model_dump())
    return game_mix_obj

@api_router.get("/game-mixes", response_model=List[GameMix])
async def get_game_mixes(current_user: User = Depends(get_current_user)):
    query = await filter_by_user_access(current_user, {}, "game_mixes")
    game_mixes = await db.game_mixes.find(query).to_list(1000)
    # Convert ObjectIds to strings
    game_mixes = [convert_objectid_to_str(game_mix) for game_mix in game_mixes]
    return [GameMix(**game_mix) for game_mix in game_mixes]

@api_router.get("/game-mixes/{game_mix_id}", response_model=GameMix)
async def get_game_mix(game_mix_id: str, current_user: User = Depends(get_current_user)):
    game_mix = await db.game_mixes.find_one({"id": game_mix_id})
    if not game_mix:
        raise HTTPException(status_code=404, detail="Game mix not found")
    return GameMix(**game_mix)

@api_router.put("/game-mixes/{game_mix_id}", response_model=GameMix)
async def update_game_mix(game_mix_id: str, game_mix_data: GameMixCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    game_mix = await db.game_mixes.find_one({"id": game_mix_id})
    if not game_mix:
        raise HTTPException(status_code=404, detail="Game mix not found")
    
    update_data = game_mix_data.model_dump()
    update_data["game_count"] = len(game_mix_data.games)
    await db.game_mixes.update_one({"id": game_mix_id}, {"$set": update_data})
    
    updated_game_mix = await db.game_mixes.find_one({"id": game_mix_id})
    return GameMix(**updated_game_mix)

@api_router.delete("/game-mixes/{game_mix_id}")
async def delete_game_mix(game_mix_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    game_mix = await db.game_mixes.find_one({"id": game_mix_id})
    if not game_mix:
        raise HTTPException(status_code=404, detail="Game mix not found")
    
    # HARD DELETE - actually remove from database
    await db.game_mixes.delete_one({"id": game_mix_id})
    return {"message": "Game mix deleted successfully"}

@api_router.post("/cabinets", response_model=Cabinet)
async def create_cabinet(cabinet_data: CabinetCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Verify provider exists
    provider = await db.providers.find_one({"id": cabinet_data.provider_id})
    if not provider:
        raise HTTPException(status_code=400, detail="Provider not found")
    
    cabinet_dict = cabinet_data.model_dump()
    cabinet_dict["created_by"] = current_user.id
    cabinet_obj = Cabinet(**cabinet_dict)
    
    await db.cabinets.insert_one(cabinet_obj.model_dump())
    return cabinet_obj

@api_router.get("/cabinets", response_model=List[Cabinet])
async def get_cabinets(current_user: User = Depends(get_current_user)):
    # Return all cabinets - FINAL SIMPLE VERSION
    try:
        cabinets = await db.cabinets.find({}).to_list(1000)
        result = []
        for cabinet in cabinets:
            # Create a simple dict
            cabinet_dict = {
                "id": str(cabinet["_id"]),
                "name": cabinet.get("name", ""),
                "model": cabinet.get("model", ""),
                "provider_id": cabinet.get("provider_id", ""),
                "status": cabinet.get("status", "active"),
                "created_at": "2025-07-31T00:00:00",
                "created_by": cabinet.get("created_by", "")
            }
            result.append(cabinet_dict)
        print(f"Returning {len(result)} cabinets from API")
        return result
    except Exception as e:
        print(f"Error in get_cabinets: {e}")
        return []

@api_router.get("/cabinets-simple")
async def get_cabinets_simple():
    # Simple endpoint without authentication
    try:
        cabinets = await db.cabinets.find({}).to_list(1000)
        result = []
        for cabinet in cabinets:
            cabinet_dict = {
                "id": str(cabinet["_id"]),
                "name": cabinet.get("name", ""),
                "model": cabinet.get("model", ""),
                "provider_id": cabinet.get("provider_id", ""),
                "status": cabinet.get("status", "active"),
                "created_at": "2025-07-31T00:00:00",
                "created_by": cabinet.get("created_by", "")
            }
            result.append(cabinet_dict)
        print(f"Simple endpoint returning {len(result)} cabinets")
        return result
    except Exception as e:
        print(f"Error in get_cabinets_simple: {e}")
        return []





@api_router.get("/cabinets-test", response_model=List[Cabinet])
async def get_cabinets_test():
    # Test endpoint without authentication
    cabinets = await db.cabinets.find({}).to_list(1000)
    # Convert ObjectIds to strings
    cabinets = [convert_objectid_to_str(cabinet) for cabinet in cabinets]
    return [Cabinet(**cabinet) for cabinet in cabinets]

@api_router.get("/cabinets/{cabinet_id}", response_model=Cabinet)
async def get_cabinet(cabinet_id: str, current_user: User = Depends(get_current_user)):
    # Try to find by _id first (ObjectId), then by id (UUID string)
    try:
        cabinet = await db.cabinets.find_one({"_id": ObjectId(cabinet_id)})
    except Exception as e:
        cabinet = await db.cabinets.find_one({"id": cabinet_id})
    
    if not cabinet:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return Cabinet(**cabinet)

@api_router.put("/cabinets/{cabinet_id}", response_model=Cabinet)
async def update_cabinet(cabinet_id: str, cabinet_data: CabinetUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Try to find by _id first (ObjectId), then by id (UUID string)
    try:
        cabinet = await db.cabinets.find_one({"_id": ObjectId(cabinet_id)})
        query = {"_id": ObjectId(cabinet_id)}
    except:
        cabinet = await db.cabinets.find_one({"id": cabinet_id})
        query = {"id": cabinet_id}
    
    if not cabinet:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    
    # Only update fields that are provided (not None)
    update_data = {}
    for field, value in cabinet_data.model_dump().items():
        if value is not None:
            update_data[field] = value
    
    if update_data:
        await db.cabinets.update_one(query, {"$set": update_data})
    
    updated_cabinet = await db.cabinets.find_one(query)
    
    if not updated_cabinet:
        raise HTTPException(status_code=404, detail="Cabinet not found after update")
    
    # Debug: Print the cabinet data to see what fields are present
    print(f"DEBUG: Cabinet data from DB: {updated_cabinet}")
    
    # Ensure all required fields are present for Cabinet model
    # Convert ObjectId to string for id field
    if '_id' in updated_cabinet:
        updated_cabinet['id'] = str(updated_cabinet['_id'])
    
    # Ensure created_by field exists (use existing or default)
    if 'created_by' not in updated_cabinet:
        print(f"DEBUG: created_by field missing, setting to: {current_user.id}")
        updated_cabinet['created_by'] = current_user.id
    
    # Ensure status field exists
    if 'status' not in updated_cabinet:
        updated_cabinet['status'] = "active"
    
    # Ensure created_at field exists
    if 'created_at' not in updated_cabinet:
        updated_cabinet['created_at'] = datetime.utcnow()
    
    print(f"DEBUG: Final cabinet data: {updated_cabinet}")
    
    try:
        return Cabinet(**updated_cabinet)
    except Exception as e:
        print(f"DEBUG: Error creating Cabinet object: {e}")
        print(f"DEBUG: Cabinet data that failed: {updated_cabinet}")
        raise HTTPException(status_code=500, detail=f"Error creating cabinet object: {str(e)}")

@api_router.delete("/cabinets/{cabinet_id}")
async def delete_cabinet(cabinet_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Try to find by _id first (ObjectId), then by id (UUID string)
    try:
        cabinet = await db.cabinets.find_one({"_id": ObjectId(cabinet_id)})
        query = {"_id": ObjectId(cabinet_id)}
    except:
        cabinet = await db.cabinets.find_one({"id": cabinet_id})
        query = {"id": cabinet_id}
    
    if not cabinet:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    
    # HARD DELETE - actually remove from database
    await db.cabinets.delete_one(query)
    return {"message": "Cabinet deleted successfully"}

@api_router.post("/slot-machines", response_model=SlotMachine)
async def create_slot_machine(slot_data: SlotMachineCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Verify cabinet and game mix exist
    cabinet = await db.cabinets.find_one({"id": slot_data.cabinet_id})
    if not cabinet:
        raise HTTPException(status_code=400, detail="Cabinet not found")
    
    game_mix = await db.game_mixes.find_one({"id": slot_data.game_mix_id})
    if not game_mix:
        raise HTTPException(status_code=400, detail="Game mix not found")
    
    slot_dict = slot_data.model_dump()
    slot_dict["created_by"] = current_user.id
    
    slot_obj = SlotMachine(**slot_dict)
    
    await db.slot_machines.insert_one(slot_obj.model_dump())
    return slot_obj

@api_router.get("/slot-machines", response_model=List[SlotMachine])
async def get_slot_machines(current_user: User = Depends(get_current_user)):
    query = await filter_by_user_access(current_user, {}, "slot_machines")
    slot_machines = await db.slot_machines.find(query).to_list(1000)
    # Convert ObjectIds to strings
    slot_machines = [convert_objectid_to_str(slot_machine) for slot_machine in slot_machines]
    return [SlotMachine(**slot_machine) for slot_machine in slot_machines]

@api_router.get("/slot-machines/{slot_machine_id}", response_model=SlotMachine)
async def get_slot_machine(slot_machine_id: str, current_user: User = Depends(get_current_user)):
    slot_machine = await db.slot_machines.find_one({"id": slot_machine_id})
    if not slot_machine:
        raise HTTPException(status_code=404, detail="Slot machine not found")
    return SlotMachine(**slot_machine)

@api_router.put("/slot-machines/{slot_machine_id}", response_model=SlotMachine)
async def update_slot_machine(slot_machine_id: str, slot_data: SlotMachineUpdate, current_user: User = Depends(get_current_user)):
    try:
        # Check if slot machine exists
        slot_machine = await db.slot_machines.find_one({"id": slot_machine_id})
        if not slot_machine:
            raise HTTPException(status_code=404, detail="Slot machine not found")
        
        # Check user permissions (basic role check)
        if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        # Convert update data to dict and filter out None values
        update_data = {k: v for k, v in slot_data.model_dump().items() if v is not None}
        
        # Add updated_by and updated_at fields
        update_data["updated_by"] = current_user.id
        update_data["updated_at"] = datetime.utcnow()
        
        # Record manual changes to change history
        for field_name, new_value in update_data.items():
            if field_name in ["updated_by", "updated_at"]:
                continue  # Skip tracking fields
            old_value = slot_machine.get(field_name, "N/A")
            if str(old_value) != str(new_value):
                change_record = {
                    "entity_type": "slots",
                    "entity_id": slot_machine_id,
                    "field_name": field_name,
                    "old_value": str(old_value),
                    "new_value": str(new_value),
                    "change_type": "Manual",
                    "scheduled_datetime": datetime.utcnow(),
                    "applied_datetime": datetime.utcnow(),
                    "applied_successfully": True,
                    "user_id": current_user.id,
                    "user_name": f"{current_user.first_name} {current_user.last_name}".strip() or current_user.username
                }
                await db.change_history.insert_one(change_record)
        
        # Update the slot machine
        result = await db.slot_machines.update_one(
            {"id": slot_machine_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes made to slot machine")
        
        # Return updated slot machine
        updated_slot = await db.slot_machines.find_one({"id": slot_machine_id})
        return SlotMachine(**updated_slot)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating slot machine: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.delete("/slot-machines/{slot_machine_id}")
async def delete_slot_machine(slot_machine_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    slot_machine = await db.slot_machines.find_one({"id": slot_machine_id})
    if not slot_machine:
        raise HTTPException(status_code=404, detail="Slot machine not found")
    
    # HARD DELETE - actually remove from database
    await db.slot_machines.delete_one({"id": slot_machine_id})
    return {"message": "Slot machine deleted successfully"}
# File upload helper functions
import base64
import mimetypes

def validate_file_upload(file_data: str, filename: str, max_size_mb: int = 50):
    """Validate file upload data"""
    try:
        # Validate base64 data
        if not file_data or not isinstance(file_data, str):
            raise HTTPException(status_code=400, detail="Invalid file data format")
        
        # Clean the base64 data
        clean_file_data = file_data.replace('\n', '').replace('\r', '').replace(' ', '')
        
        # Decode base64 to get actual file size
        try:
            file_bytes = base64.b64decode(clean_file_data)
            file_size = len(file_bytes)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 data: {str(e)}")
        
        # Check file size (50MB limit)
        if file_size > max_size_mb * 1024 * 1024:
            raise HTTPException(status_code=400, detail=f"File size exceeds {max_size_mb}MB limit")
        
        # Get mime type
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type:
            mime_type = "application/octet-stream"
        
        # Debug: Print filename and detected mime type
        print(f"DEBUG: Filename: {filename}")
        print(f"DEBUG: Detected MIME type: {mime_type}")
        
        # Validate file types (common business file types)
        allowed_types = [
            'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/jpg',
            'application/pdf', 'application/msword', 
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'text/plain', 'text/csv'
        ]
        
        # Additional check for image files by extension
        if mime_type not in allowed_types:
            # Check if it's an image file by extension
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff']
            file_extension = filename.lower()
            if any(file_extension.endswith(ext) for ext in image_extensions):
                print(f"DEBUG: File has image extension, allowing: {filename}")
                # For image files, use a generic image mime type
                mime_type = "image/jpeg"  # Default to jpeg for images
            else:
                print(f"DEBUG: File type not allowed: {mime_type} for {filename}")
                raise HTTPException(status_code=400, detail="File type not allowed")
        
        print(f"DEBUG: Final MIME type: {mime_type}")
        return file_size, mime_type
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid file data: {str(e)}")

# Attachment routes
@api_router.post("/attachments", response_model=Attachment)
async def upload_attachment(attachment_data: AttachmentCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Validate file
    file_size, mime_type = validate_file_upload(attachment_data.file_data, attachment_data.filename)
    
    # Verify entity exists based on entity_type
    entity_collections = {
        'users': db.users,
        'companies': db.companies,
        'locations': db.locations,
        'providers': db.providers,
        'cabinets': db.cabinets,
        'game_mixes': db.game_mixes,
        'slot_machines': db.slot_machines,
        'slots': db.slot_machines,  # Alias for slots
        'invoices': db.invoices,
        'onjn_reports': db.onjn_reports,
        'onjn': db.onjn_reports,  # Alias for onjn
        'legal_documents': db.legal_documents,
        'metrology': db.metrology,
        'jackpots': db.jackpots,
        'comision_dates': db.comision_dates,
        'comision_date': db.comision_dates  # Alias for comision_date
    }
    
    if attachment_data.entity_type not in entity_collections:
        raise HTTPException(status_code=400, detail="Invalid entity type")
    
    collection = entity_collections[attachment_data.entity_type]
    
    print(f"Looking for {attachment_data.entity_type} with id: {attachment_data.entity_id}")
    print(f"Entity type: {attachment_data.entity_type}")
    print(f"Available entity types: {list(entity_collections.keys())}")
    print(f"Is entity_type in collections: {attachment_data.entity_type in entity_collections}")
    
    # For cabinets, the frontend sends the _id as string, so we need to convert it back to ObjectId
    if attachment_data.entity_type == "cabinets":
        print("Processing cabinet entity")
        try:
            entity = await collection.find_one({"_id": ObjectId(attachment_data.entity_id)})
            print(f"Found cabinet by _id: {entity is not None}")
            if entity:
                print(f"Cabinet found: {entity.get('name', 'Unknown')}")
        except Exception as e:
            print(f"Error with _id lookup: {e}")
            entity = None
    else:
        # For other entities, try to find by _id first (ObjectId), then by id (UUID string)
        try:
            entity = await collection.find_one({"_id": ObjectId(attachment_data.entity_id)})
            print(f"Found by _id: {entity is not None}")
        except Exception as e:
            print(f"Error with _id lookup: {e}")
            entity = await collection.find_one({"id": attachment_data.entity_id})
            print(f"Found by id: {entity is not None}")
    
    if not entity:
        print(f"Entity not found for {attachment_data.entity_type} with id {attachment_data.entity_id}")
        raise HTTPException(status_code=404, detail=f"{attachment_data.entity_type.title()} not found")
    
    attachment_dict = attachment_data.model_dump()
    attachment_dict["file_size"] = file_size
    attachment_dict["mime_type"] = mime_type
    attachment_dict["uploaded_by"] = current_user.id
    attachment_obj = Attachment(**attachment_dict)
    
    await db.attachments.insert_one(attachment_obj.model_dump())
    return attachment_obj

@api_router.get("/attachments/{entity_type}/{entity_id}", response_model=List[dict])
async def get_entity_attachments(entity_type: str, entity_id: str, current_user: User = Depends(get_current_user)):
    # Verify user has access to the entity
    entity_collections = {
        'users': db.users,
        'companies': db.companies,
        'locations': db.locations,
        'providers': db.providers,
        'cabinets': db.cabinets,
        'game_mixes': db.game_mixes,
        'slot_machines': db.slot_machines,
        'slots': db.slot_machines,  # Alias for slots
        'invoices': db.invoices,
        'onjn_reports': db.onjn_reports,
        'onjn': db.onjn_reports,  # Alias for onjn
        'legal_documents': db.legal_documents,
        'metrology': db.metrology,
        'comision_dates': db.comision_dates,
        'comision_date': db.comision_dates,  # Alias for comision_date
        'marketing': db.marketing_campaigns  # Support for marketing campaigns
    }
    
    if entity_type not in entity_collections:
        raise HTTPException(status_code=400, detail="Invalid entity type")
    
    # Check access based on entity type
    if entity_type == "companies":
        accessible_companies = await get_user_accessible_companies(current_user)
        if current_user.role != UserRole.ADMIN and entity_id not in accessible_companies:
            raise HTTPException(status_code=403, detail="Access denied to this entity")
    elif entity_type == "locations":
        accessible_locations = await get_user_accessible_locations(current_user)
        if current_user.role != UserRole.ADMIN and entity_id not in accessible_locations:
            raise HTTPException(status_code=403, detail="Access denied to this entity")
    elif entity_type in ["cabinets", "slot_machines"]:
        # Check if entity belongs to accessible location
        collection = entity_collections[entity_type]
        entity = await collection.find_one({"id": entity_id})
        if entity:
            accessible_locations = await get_user_accessible_locations(current_user)
            if current_user.role != UserRole.ADMIN and entity.get("location_id") not in accessible_locations:
                raise HTTPException(status_code=403, detail="Access denied to this entity")
    elif entity_type == "marketing":
        # Check if user has access to marketing campaigns
        # Marketing campaigns are accessible to all authenticated users for now
        # You can add more specific access control here if needed
        pass
    
    attachments = await db.attachments.find({
        "entity_type": entity_type,
        "entity_id": entity_id
    }).to_list(1000)
    
    # Convert ObjectIds to strings and add creator information
    result = []
    for attachment in attachments:
        attachment_data = convert_objectid_to_str(attachment)
        
        # Get creator information
        creator_info = {"first_name": "", "last_name": ""}
        if "uploaded_by" in attachment_data:
            creator = await db.users.find_one({"id": attachment_data["uploaded_by"]})
            if creator:
                creator_info = {
                    "first_name": creator.get("first_name", ""),
                    "last_name": creator.get("last_name", "")
                }
        
        # Add creator info to attachment data
        attachment_data["creator_name"] = f"{creator_info['first_name']} {creator_info['last_name']}".strip()
        
        result.append(attachment_data)
    
    return result

@api_router.get("/attachments/{attachment_id}")
async def download_attachment(attachment_id: str, current_user: User = Depends(get_current_user)):
    attachment = await db.attachments.find_one({"id": attachment_id})
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    return {
        "filename": attachment["original_filename"],
        "mime_type": attachment["mime_type"],
        "file_data": attachment["file_data"]
    }

@api_router.delete("/attachments/{attachment_id}")
async def delete_attachment(attachment_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    attachment = await db.attachments.find_one({"id": attachment_id})
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    await db.attachments.delete_one({"id": attachment_id})
    return {"message": "Attachment deleted successfully"}

@api_router.get("/attachments/marketing/{campaign_id}/count")
async def get_marketing_attachments_count(campaign_id: str, current_user: User = Depends(get_current_user)):
    """Get the count of attachments for a specific marketing campaign"""
    try:
        # Check if marketing campaign exists
        campaign = await db.marketing_campaigns.find_one({"id": campaign_id})
        if not campaign:
            raise HTTPException(status_code=404, detail="Marketing campaign not found")
        
        # Count attachments for this campaign
        count = await db.attachments.count_documents({
            "entity_type": "marketing",
            "entity_id": campaign_id
        })
        
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting attachments: {str(e)}")

# Invoice management routes
@api_router.post("/invoices", response_model=Invoice)
async def create_invoice(invoice_data: InvoiceCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Verify company and location exist
    company = await db.companies.find_one({"id": invoice_data.company_id})
    if not company:
        raise HTTPException(status_code=400, detail="Company not found")
    
    location = await db.locations.find_one({"id": invoice_data.location_id})
    if not location:
        raise HTTPException(status_code=400, detail="Location not found")
    
    # Check if invoice number already exists
    existing_invoice = await db.invoices.find_one({"invoice_number": invoice_data.invoice_number})
    if existing_invoice:
        raise HTTPException(status_code=400, detail="Invoice number already exists")
    
    # Verify serial numbers exist in slot machines and update them with invoice number
    serial_numbers = invoice_data.serial_numbers.strip().split()
    if serial_numbers:
        for serial_number in serial_numbers:
            if serial_number:  # Skip empty strings
                slot_machine = await db.slot_machines.find_one({"serial_number": serial_number})
                if not slot_machine:
                    raise HTTPException(status_code=400, detail=f"Serial number {serial_number} not found in slot machines")
    
    invoice_dict = invoice_data.model_dump()
    invoice_dict["created_by"] = current_user.id
    invoice_obj = Invoice(**invoice_dict)
    
    # Create the invoice
    await db.invoices.insert_one(invoice_obj.model_dump())
    
    # Update slot machines with invoice number
    if serial_numbers:
        for serial_number in serial_numbers:
            if serial_number:
                await db.slot_machines.update_one(
                    {"serial_number": serial_number},
                    {"$set": {"invoice_number": invoice_data.invoice_number}}
                )
    
    return invoice_obj

@api_router.get("/invoices", response_model=List[Invoice])
async def get_invoices(current_user: User = Depends(get_current_user)):
    query = await filter_by_user_access(current_user, {}, "invoices")
    invoices = await db.invoices.find(query).to_list(1000)
    # Convert ObjectIds to strings
    invoices = [convert_objectid_to_str(invoice) for invoice in invoices]
    return [Invoice(**invoice) for invoice in invoices]

@api_router.get("/invoices/{invoice_id}", response_model=Invoice)
async def get_invoice(invoice_id: str, current_user: User = Depends(get_current_user)):
    invoice = await db.invoices.find_one({"id": invoice_id})
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return Invoice(**invoice)

@api_router.put("/invoices/{invoice_id}", response_model=Invoice)
async def update_invoice(invoice_id: str, invoice_data: InvoiceCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    invoice = await db.invoices.find_one({"id": invoice_id})
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    update_data = invoice_data.model_dump()
    await db.invoices.update_one({"id": invoice_id}, {"$set": update_data})
    
    updated_invoice = await db.invoices.find_one({"id": invoice_id})
    return Invoice(**updated_invoice)

@api_router.delete("/invoices/{invoice_id}")
async def delete_invoice(invoice_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    await db.invoices.delete_one({"id": invoice_id})
    return {"message": "Invoice deleted successfully"}

# ONJN Report routes
@api_router.post("/onjn-reports", response_model=ONJNReport)
async def create_onjn_report(report_data: ONJNReportCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Check if report number already exists
    existing_report = await db.onjn_reports.find_one({"report_number": report_data.report_number})
    if existing_report:
        raise HTTPException(status_code=400, detail="Report number already exists")
    
    report_dict = report_data.model_dump()
    report_dict["created_by"] = current_user.id
    report_obj = ONJNReport(**report_dict)
    
    await db.onjn_reports.insert_one(report_obj.model_dump())
    return report_obj

@api_router.get("/onjn-reports", response_model=List[ONJNReport])
async def get_onjn_reports(current_user: User = Depends(get_current_user)):
    query = await filter_by_user_access(current_user, {}, "onjn_reports")
    reports = await db.onjn_reports.find(query).to_list(1000)
    # Convert ObjectIds to strings
    reports = [convert_objectid_to_str(report) for report in reports]
    return [ONJNReport(**report) for report in reports]

@api_router.get("/onjn-reports/{report_id}", response_model=ONJNReport)
async def get_onjn_report(report_id: str, current_user: User = Depends(get_current_user)):
    report = await db.onjn_reports.find_one({"id": report_id})
    if not report:
        raise HTTPException(status_code=404, detail="ONJN report not found")
    return ONJNReport(**report)

@api_router.put("/onjn-reports/{report_id}", response_model=ONJNReport)
async def update_onjn_report(report_id: str, report_data: ONJNReportCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    report = await db.onjn_reports.find_one({"id": report_id})
    if not report:
        raise HTTPException(status_code=404, detail="ONJN report not found")
    
    update_data = report_data.model_dump()
    await db.onjn_reports.update_one({"id": report_id}, {"$set": update_data})
    
    updated_report = await db.onjn_reports.find_one({"id": report_id})
    return ONJNReport(**updated_report)

@api_router.delete("/onjn-reports/{report_id}")
async def delete_onjn_report(report_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    await db.onjn_reports.delete_one({"id": report_id})
    return {"message": "ONJN report deleted successfully"}

# Legal Document routes
@api_router.post("/legal-documents", response_model=LegalDocument)
async def create_legal_document(document_data: LegalDocumentCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    document_dict = document_data.model_dump()
    document_dict["created_by"] = current_user.id
    document_obj = LegalDocument(**document_dict)
    
    await db.legal_documents.insert_one(document_obj.model_dump())
    return document_obj

@api_router.get("/legal-documents", response_model=List[LegalDocument])
async def get_legal_documents(current_user: User = Depends(get_current_user)):
    query = await filter_by_user_access(current_user, {}, "legal_documents")
    documents = await db.legal_documents.find(query).to_list(1000)
    # Convert ObjectIds to strings
    documents = [convert_objectid_to_str(document) for document in documents]
    return [LegalDocument(**document) for document in documents]

@api_router.get("/legal-documents/{document_id}", response_model=LegalDocument)
async def get_legal_document(document_id: str, current_user: User = Depends(get_current_user)):
    document = await db.legal_documents.find_one({"id": document_id})
    if not document:
        raise HTTPException(status_code=404, detail="Legal document not found")
    return LegalDocument(**document)

@api_router.put("/legal-documents/{document_id}", response_model=LegalDocument)
async def update_legal_document(document_id: str, document_data: LegalDocumentCreate, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    document = await db.legal_documents.find_one({"id": document_id})
    if not document:
        raise HTTPException(status_code=404, detail="Legal document not found")
    
    update_data = document_data.model_dump()
    await db.legal_documents.update_one({"id": document_id}, {"$set": update_data})
    
    updated_document = await db.legal_documents.find_one({"id": document_id})
    return LegalDocument(**updated_document)

@api_router.delete("/legal-documents/{document_id}")
async def delete_legal_document(document_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    await db.legal_documents.delete_one({"id": document_id})
    return {"message": "Legal document deleted successfully"}

# Metrology endpoints
@api_router.post("/metrology", response_model=Metrology)
async def create_metrology(metrology_data: MetrologyCreate, current_user: User = Depends(get_current_user)):
    metrology = Metrology(
        **metrology_data.model_dump(),
        created_by=current_user.id
    )
    
    await db.metrology.insert_one(metrology.model_dump())
    return metrology

@api_router.get("/metrology", response_model=List[dict])
async def get_metrology(current_user: User = Depends(get_current_user)):
    cursor = db.metrology.find({})
    metrology_list = await cursor.to_list(length=None)
    
    # Fix: Ensure all records have an 'id' field
    for item in metrology_list:
        if '_id' in item and 'id' not in item:
            # Add UUID id field for records that don't have it
            item['id'] = str(uuid.uuid4())
            await db.metrology.update_one({'_id': item['_id']}, {'$set': {'id': item['id']}})
            print(f"🔧 Added missing 'id' field to metrology record: {item['_id']} -> {item['id']}")
    
    result = []
    for item in metrology_list:
        # Convert ObjectId to string
        metrology_data = convert_objectid_to_str(item)
        
        # Get creator information
        creator_info = {"first_name": "", "last_name": ""}
        if "created_by" in metrology_data:
            print(f"🔍 Looking for creator with ID: {metrology_data['created_by']}")
            creator = await db.users.find_one({"id": metrology_data["created_by"]})
            if creator:
                creator_info = {
                    "first_name": creator.get("first_name", ""),
                    "last_name": creator.get("last_name", "")
                }
                print(f"✅ Found creator: {creator_info['first_name']} {creator_info['last_name']}")
            else:
                print(f"❌ Creator not found for ID: {metrology_data['created_by']}")
        
        # Add creator info to metrology data
        creator_name = f"{creator_info['first_name']} {creator_info['last_name']}".strip()
        metrology_data["creator_name"] = creator_name if creator_name else "Unknown User"
        print(f"📝 Final creator_name: {metrology_data['creator_name']}")
        
        # Get updater information
        updater_info = {"first_name": "", "last_name": ""}
        if "updated_by" in metrology_data and metrology_data["updated_by"]:
            print(f"🔍 Looking for updater with ID: {metrology_data['updated_by']}")
            updater = await db.users.find_one({"id": metrology_data["updated_by"]})
            if updater:
                updater_info = {
                    "first_name": updater.get("first_name", ""),
                    "last_name": updater.get("last_name", "")
                }
                print(f"✅ Found updater: {updater_info['first_name']} {updater_info['last_name']}")
            else:
                print(f"❌ Updater not found for ID: {metrology_data['updated_by']}")
        
        # Add updater info to metrology data
        updater_name = f"{updater_info['first_name']} {updater_info['last_name']}".strip()
        metrology_data["updater_name"] = updater_name if updater_name else "Unknown User"
        print(f"📝 Final updater_name: {metrology_data['updater_name']}")
        
        result.append(metrology_data)
    
    return result

@api_router.get("/metrology/{metrology_id}", response_model=dict)
async def get_metrology_record(metrology_id: str, current_user: User = Depends(get_current_user)):
    # Try to find by id first, then by _id
    metrology = await db.metrology.find_one({"id": metrology_id})
    if not metrology:
        # Try with _id (ObjectId)
        try:
            from bson import ObjectId
            metrology = await db.metrology.find_one({"_id": ObjectId(metrology_id)})
        except:
            pass
    
    if not metrology:
        raise HTTPException(status_code=404, detail="Metrology record not found")
    
    # Convert ObjectId to string
    metrology_data = convert_objectid_to_str(metrology)
    
    # Get creator information
    creator_info = {"first_name": "", "last_name": ""}
    if "created_by" in metrology_data:
        print(f"🔍 Looking for creator with ID: {metrology_data['created_by']}")
        creator = await db.users.find_one({"id": metrology_data["created_by"]})
        if creator:
            creator_info = {
                "first_name": creator.get("first_name", ""),
                "last_name": creator.get("last_name", "")
            }
            print(f"✅ Found creator: {creator_info['first_name']} {creator_info['last_name']}")
        else:
            print(f"❌ Creator not found for ID: {metrology_data['created_by']}")
    
    # Add creator info to metrology data
    creator_name = f"{creator_info['first_name']} {creator_info['last_name']}".strip()
    metrology_data["creator_name"] = creator_name if creator_name else "Unknown User"
    print(f"📝 Final creator_name: {metrology_data['creator_name']}")
    
    # Get updater information
    updater_info = {"first_name": "", "last_name": ""}
    if "updated_by" in metrology_data and metrology_data["updated_by"]:
        print(f"🔍 Looking for updater with ID: {metrology_data['updated_by']}")
        updater = await db.users.find_one({"id": metrology_data["updated_by"]})
        if updater:
            updater_info = {
                "first_name": updater.get("first_name", ""),
                "last_name": updater.get("last_name", "")
            }
            print(f"✅ Found updater: {updater_info['first_name']} {updater_info['last_name']}")
        else:
            print(f"❌ Updater not found for ID: {metrology_data['updated_by']}")
    
    # Add updater info to metrology data
    updater_name = f"{updater_info['first_name']} {updater_info['last_name']}".strip()
    metrology_data["updater_name"] = updater_name if updater_name else "Unknown User"
    print(f"📝 Final updater_name: {metrology_data['updater_name']}")
    
    return metrology_data

@api_router.put("/metrology/{metrology_id}")
async def update_metrology_simple(metrology_id: str, request: Request, current_user: User = Depends(get_current_user)):
    print(f"🔍 Looking for metrology record with ID: {metrology_id}")
    
    # Get raw JSON data from request
    body = await request.json()
    print(f"📦 Received update data: {body}")
    
    # Check if metrology record exists - try both id and _id
    existing_metrology = await db.metrology.find_one({"id": metrology_id})
    print(f"🔍 Search by 'id' field result: {existing_metrology is not None}")
    
    if not existing_metrology:
        # Try with _id (ObjectId)
        try:
            from bson import ObjectId
            existing_metrology = await db.metrology.find_one({"_id": ObjectId(metrology_id)})
            print(f"🔍 Search by '_id' field result: {existing_metrology is not None}")
        except Exception as e:
            print(f"❌ Error converting to ObjectId: {e}")
            pass
    
    if not existing_metrology:
        print(f"❌ Metrology record not found for ID: {metrology_id}")
        raise HTTPException(status_code=404, detail="Metrology record not found")
    
    print(f"✅ Found metrology record: {existing_metrology.get('_id', 'No _id')}")
    
    # Create update data from raw JSON - ONLY the fields that exist
    update_data = {
        "serial_number": str(body.get("serial_number", "")),
        "certificate_number": str(body.get("certificate_number", "")),
        "issue_date": str(body.get("issue_date", "")),
        "issuing_authority": str(body.get("issuing_authority", "")),
        "status": str(body.get("status", "active")),
        "description": str(body.get("description", "")),
        "updated_at": datetime.utcnow(),
        "updated_by": current_user.id
    }
    
    print(f"📝 Update data prepared: {update_data}")
    
    # Try to update by id first, then by _id
    result = await db.metrology.update_one({"id": metrology_id}, {"$set": update_data})
    if result.modified_count == 0:
        # Try with _id (ObjectId)
        try:
            from bson import ObjectId
            result = await db.metrology.update_one({"_id": ObjectId(metrology_id)}, {"$set": update_data})
        except:
            pass
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Metrology record not found")
    
    print(f"✅ Update successful, modified count: {result.modified_count}")
    
    # Get updated record
    updated_metrology = await db.metrology.find_one({"id": metrology_id})
    if not updated_metrology:
        try:
            from bson import ObjectId
            updated_metrology = await db.metrology.find_one({"_id": ObjectId(metrology_id)})
        except:
            pass
    
    return convert_objectid_to_str(updated_metrology)

@api_router.delete("/metrology/{metrology_id}")
async def delete_metrology(metrology_id: str, current_user: User = Depends(get_current_user)):
    # Check if metrology record exists - try both _id and id
    metrology = await db.metrology.find_one({"id": metrology_id})
    if not metrology:
        # Try with _id (ObjectId)
        try:
            from bson import ObjectId
            metrology = await db.metrology.find_one({"_id": ObjectId(metrology_id)})
        except:
            pass
    
    if not metrology:
        raise HTTPException(status_code=404, detail="Metrology record not found")
    
    # Delete metrology record - try both _id and id
    result = await db.metrology.delete_one({"id": metrology_id})
    if result.deleted_count == 0:
        # Try with _id (ObjectId)
        try:
            from bson import ObjectId
            result = await db.metrology.delete_one({"_id": ObjectId(metrology_id)})
        except:
            pass
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Metrology record not found")
    
    return {"message": "Metrology record deleted successfully"}

# Jackpot endpoints
@api_router.post("/jackpots", response_model=Jackpot)
async def create_jackpot(jackpot_data: JackpotCreate, current_user: User = Depends(get_current_user)):
    jackpot = Jackpot(
        **jackpot_data.model_dump(),
        last_reset_date=datetime.utcnow(),
        created_by=current_user.id
    )
    
    jackpot_dict = jackpot.model_dump()
    jackpot_dict["id"] = str(uuid.uuid4())  # Set UUID for jackpot
    
    await db.jackpots.insert_one(jackpot_dict)
    return Jackpot(**jackpot_dict)

@api_router.get("/jackpots", response_model=List[Jackpot])
async def get_jackpots(current_user: User = Depends(get_current_user)):
    cursor = db.jackpots.find({})
    jackpot_list = await cursor.to_list(length=None)
    return [Jackpot(**convert_objectid_to_str(item)) for item in jackpot_list]

@api_router.get("/jackpots/{jackpot_id}", response_model=Jackpot)
async def get_jackpot(jackpot_id: str, current_user: User = Depends(get_current_user)):
    jackpot = await db.jackpots.find_one({"id": jackpot_id})
    if not jackpot:
        raise HTTPException(status_code=404, detail="Jackpot record not found")
    
    return Jackpot(**convert_objectid_to_str(jackpot))

@api_router.put("/jackpots/{jackpot_id}", response_model=Jackpot)
async def update_jackpot(jackpot_id: str, jackpot_data: JackpotCreate, current_user: User = Depends(get_current_user)):
    # Check if jackpot record exists
    existing_jackpot = await db.jackpots.find_one({"id": jackpot_id})
    if not existing_jackpot:
        raise HTTPException(status_code=404, detail="Jackpot record not found")
    
    await db.jackpots.update_one({"id": jackpot_id}, {"$set": jackpot_data.model_dump()})
    
    updated_jackpot = await db.jackpots.find_one({"id": jackpot_id})
    return Jackpot(**convert_objectid_to_str(updated_jackpot))

@api_router.delete("/jackpots/{jackpot_id}")
async def delete_jackpot(jackpot_id: str, current_user: User = Depends(get_current_user)):
    # Check if jackpot record exists
    jackpot = await db.jackpots.find_one({"id": jackpot_id})
    if not jackpot:
        raise HTTPException(status_code=404, detail="Jackpot record not found")
    
    # Delete jackpot record
    await db.jackpots.delete_one({"id": jackpot_id})
    return {"message": "Jackpot record deleted successfully"}

# Comision Date endpoints
@api_router.post("/comision-dates", response_model=ComisionDate)
async def create_comision_date(comision_data: ComisionDateCreate, current_user: User = Depends(get_current_user)):
    # Create comision date document
    comision_dict = comision_data.model_dump()
    comision_dict["created_by"] = current_user.id
    
    # Create comision date
    comision_doc = {
        "id": str(uuid.uuid4()),
        "event_name": comision_dict["event_name"],
        "commission_date": comision_dict["commission_date"],
        "serial_numbers": comision_dict["serial_numbers"],
        "created_at": datetime.utcnow(),
        "created_by": comision_dict["created_by"]
    }
    
    await db.comision_dates.insert_one(comision_doc)
    
    # Update slot machines with commission date
    serial_numbers = comision_dict["serial_numbers"].split()
    for serial_number in serial_numbers:
        serial_number = serial_number.strip()
        if serial_number:
            # Update slot machine with commission date
            await db.slot_machines.update_one(
                {"serial_number": serial_number},
                {"$set": {"commission_date": comision_dict["commission_date"]}}
            )
    
    return ComisionDate(**comision_doc)

@api_router.get("/comision-dates", response_model=List[ComisionDate])
async def get_comision_dates(current_user: User = Depends(get_current_user)):
    comision_dates = await db.comision_dates.find({}).to_list(1000)
    comision_dates = [convert_objectid_to_str(comision) for comision in comision_dates]
    
    # Add creator full name
    for comision in comision_dates:
        if comision.get("created_by"):
            creator = await db.users.find_one({"id": comision["created_by"]})
            if creator:
                full_name = f"{creator.get('first_name', '')} {creator.get('last_name', '')}".strip()
                comision["created_by"] = full_name if full_name else "Unknown"
            else:
                comision["created_by"] = "Unknown"
        else:
            comision["created_by"] = "Unknown"
        print(f"DEBUG created_by: {comision['created_by']}")
    
    return [ComisionDate(**comision) for comision in comision_dates]

@api_router.get("/comision-dates/{comision_id}", response_model=ComisionDate)
async def get_comision_date(comision_id: str, current_user: User = Depends(get_current_user)):
    comision = await db.comision_dates.find_one({"id": comision_id})
    if not comision:
        raise HTTPException(status_code=404, detail="Comision date not found")
    
    comision = convert_objectid_to_str(comision)
    
    # Add creator full name
    if comision.get("created_by"):
        creator = await db.users.find_one({"id": comision["created_by"]})
        if creator:
            full_name = f"{creator.get('first_name', '')} {creator.get('last_name', '')}".strip()
            comision["created_by"] = full_name if full_name else "Unknown"
        else:
            comision["created_by"] = "Unknown"
    else:
        comision["created_by"] = "Unknown"
    
    return ComisionDate(**comision)

@api_router.put("/comision-dates/{comision_id}", response_model=ComisionDate)
async def update_comision_date(comision_id: str, comision_data: ComisionDateCreate, current_user: User = Depends(get_current_user)):
    # Check if comision date exists
    comision = await db.comision_dates.find_one({"id": comision_id})
    if not comision:
        raise HTTPException(status_code=404, detail="Comision date not found")
    
    # Debug: Log the received data
    print(f"🔍 DEBUG: Updating comision date {comision_id}")
    print(f"🔍 DEBUG: Received comision_data: {comision_data}")
    print(f"🔍 DEBUG: event_name: {comision_data.event_name}")
    print(f"🔍 DEBUG: commission_date: {comision_data.commission_date}")
    print(f"🔍 DEBUG: serial_numbers: {comision_data.serial_numbers}")
    
    # Update comision date
    update_data = comision_data.model_dump()
    print(f"🔍 DEBUG: update_data: {update_data}")
    
    await db.comision_dates.update_one({"id": comision_id}, {"$set": update_data})
    
    # Update slot machines with new commission date
    serial_numbers = update_data["serial_numbers"].split()
    for serial_number in serial_numbers:
        serial_number = serial_number.strip()
        if serial_number:
            # Update slot machine with commission date
            await db.slot_machines.update_one(
                {"serial_number": serial_number},
                {"$set": {"commission_date": update_data["commission_date"]}}
            )
    
    updated_comision = await db.comision_dates.find_one({"id": comision_id})
    updated_comision = convert_objectid_to_str(updated_comision)
    print(f"🔍 DEBUG: Updated comision: {updated_comision}")
    return ComisionDate(**updated_comision)

@api_router.delete("/comision-dates/{comision_id}")
async def delete_comision_date(comision_id: str, current_user: User = Depends(get_current_user)):
    # Check if comision date exists
    comision = await db.comision_dates.find_one({"id": comision_id})
    if not comision:
        raise HTTPException(status_code=404, detail="Comision date not found")
    
    # Remove commission date from slot machines
    serial_numbers = comision["serial_numbers"].split()
    for serial_number in serial_numbers:
        serial_number = serial_number.strip()
        if serial_number:
            # Remove commission date from slot machine
            await db.slot_machines.update_one(
                {"serial_number": serial_number},
                {"$unset": {"commission_date": ""}}
            )
    
    # Delete comision date record
    await db.comision_dates.delete_one({"id": comision_id})
    return {"message": "Comision date deleted successfully"}

@api_router.post("/users", response_model=dict)
async def create_user(user_data: UserCreate, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Check if user already exists
    existing_user = await db.users.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create user document
    user_dict = user_data.model_dump()
    user_dict["password_hash"] = hash_password(user_data.password)
    user_dict.pop("password", None)  # Remove plain password
    user_dict["created_by"] = current_user.id
    
    # Create user without permissions validation
    user_doc = {
        "id": user_dict.get("id", str(uuid.uuid4())),
        "username": user_dict["username"],
        "email": user_dict["email"],
        "phone": user_dict.get("phone"),
        "password_hash": user_dict["password_hash"],
        "first_name": user_dict.get("first_name", ""),
        "last_name": user_dict.get("last_name", ""),
        "role": user_dict.get("role", "operator"),
        "assigned_locations": user_dict.get("assigned_locations", []),
        "permissions": {
            "modules": {
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
            },
            "actions": {
                "companies": {"create": False, "read": False, "update": False, "delete": False},
                "locations": {"create": False, "read": False, "update": False, "delete": False},
                "providers": {"create": False, "read": False, "update": False, "delete": False},
                "cabinets": {"create": False, "read": False, "update": False, "delete": False},
                "game_mixes": {"create": False, "read": False, "update": False, "delete": False},
                "slot_machines": {"create": False, "read": False, "update": False, "delete": False},
                "invoices": {"create": False, "read": False, "update": False, "delete": False},
                "onjn_reports": {"create": False, "read": False, "update": False, "delete": False},
                "legal_documents": {"create": False, "read": False, "update": False, "delete": False},
                "metrology": {"create": False, "read": False, "update": False, "delete": False},
                "jackpots": {"create": False, "read": False, "update": False, "delete": False},
                "users": {"create": False, "read": False, "update": False, "delete": False}
            },
            "accessible_companies": [],
            "accessible_locations": []
        },
        "created_at": datetime.utcnow(),
        "is_active": True,
        "created_by": user_dict["created_by"]
    }
    
    await db.users.insert_one(user_doc)
    
    # Return user without password hash
    user_response = user_doc.copy()
    user_response.pop("password_hash", None)
    return user_response
    


@api_router.get("/users", response_model=List[dict])
async def get_users(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    users = await db.users.find({}).to_list(1000)
    # Convert ObjectIds to strings and remove password hashes
    users = [convert_objectid_to_str(user) for user in users]
    for user in users:
        user.pop('password_hash', None)
    return users

@api_router.get("/users/{user_id}", response_model=dict)
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Convert ObjectId to string and remove password hash
    user = convert_objectid_to_str(user)
    user.pop('password_hash', None)
    return user

@api_router.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: str, user_data: UserUpdate, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = {}
    if user_data.username is not None:
        update_data["username"] = user_data.username
    if user_data.email is not None:
        update_data["email"] = user_data.email
    if user_data.phone is not None:
        update_data["phone"] = user_data.phone
    if user_data.first_name is not None:
        update_data["first_name"] = user_data.first_name
    if user_data.last_name is not None:
        update_data["last_name"] = user_data.last_name
    if user_data.role is not None:
        update_data["role"] = user_data.role
    if user_data.assigned_locations is not None:
        update_data["assigned_locations"] = user_data.assigned_locations
    if user_data.permissions is not None:
        update_data["permissions"] = user_data.permissions.model_dump()
    if user_data.is_active is not None:
        update_data["is_active"] = user_data.is_active
    if user_data.password is not None:
        update_data["password_hash"] = hash_password(user_data.password)
    
    await db.users.update_one({"id": user_id}, {"$set": update_data})
    
    updated_user = await db.users.find_one({"id": user_id})
    # Convert ObjectId to string and remove password hash
    updated_user = convert_objectid_to_str(updated_user)
    updated_user.pop('password_hash', None)
    return updated_user

# Add endpoint to get all companies and locations for user form
@api_router.get("/admin/companies-locations")
async def get_companies_locations_for_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    companies = await db.companies.find({}).to_list(1000)
    locations = await db.locations.find({}).to_list(1000)
    
    return {
        "companies": [{"id": comp["id"], "name": comp["name"]} for comp in companies],
        "locations": [{"id": loc["id"], "name": loc["name"], "company_id": loc.get("company_id")} for loc in locations]
    }

@api_router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    user = await db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # HARD DELETE - actually remove from database
    await db.users.delete_one({"id": user_id})
    return {"message": "User deleted successfully"}

@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    # Get user accessible data for statistics
    accessible_companies = await get_user_accessible_companies(current_user)
    accessible_locations = await get_user_accessible_locations(current_user)
    
    # Get counts based on user access
    total_companies = len(accessible_companies)
    total_locations = len(accessible_locations)
    
    # Count active entities within user's access
    active_companies_query = {"id": {"$in": accessible_companies}, "status": "active"}
    active_locations_query = {"id": {"$in": accessible_locations}, "status": "active"}
    
    active_companies = await db.companies.count_documents(active_companies_query)
    active_locations = await db.locations.count_documents(active_locations_query)
    
    # Get equipment counts based on accessible locations
    cabinets_query = {"location_id": {"$in": accessible_locations}}
    
    # For slot machines, we need to find cabinets in accessible locations first
    accessible_cabinets = await db.cabinets.find(cabinets_query).to_list(1000)
    accessible_cabinet_ids = [cab["id"] for cab in accessible_cabinets]
    slots_query = {"cabinet_id": {"$in": accessible_cabinet_ids}} if accessible_cabinet_ids else {"cabinet_id": {"$in": []}}
    
    # For admin, get all providers and game mixes; for others, get only those used in accessible locations
    if current_user.role == UserRole.ADMIN:
        total_providers = await db.providers.count_documents({})
        total_game_mixes = await db.game_mixes.count_documents({})
    else:
        # Get providers used in accessible cabinets
        cabinets = await db.cabinets.find(cabinets_query).to_list(1000)
        provider_ids = list(set([cab["provider_id"] for cab in cabinets if "provider_id" in cab]))
        total_providers = len(provider_ids)
        
        # Get game mixes used in accessible slot machines
        slot_machines = await db.slot_machines.find({}).to_list(1000)
        accessible_slots = []
        for slot in slot_machines:
            cabinet = await db.cabinets.find_one({"id": slot["cabinet_id"]})
            if cabinet and cabinet.get("location_id") in accessible_locations:
                accessible_slots.append(slot)
        game_mix_ids = list(set([slot["game_mix_id"] for slot in accessible_slots if "game_mix_id" in slot]))
        total_game_mixes = len(game_mix_ids)
    
    total_cabinets = await db.cabinets.count_documents(cabinets_query)
    total_slot_machines = await db.slot_machines.count_documents(slots_query)
    active_equipment = await db.cabinets.count_documents({**cabinets_query, "status": "active"}) + \
                     await db.slot_machines.count_documents({**slots_query, "status": "active"})
    
    # Get financial and legal document counts
    invoices_query = await filter_by_user_access(current_user, {}, "invoices")
    onjn_query = await filter_by_user_access(current_user, {}, "onjn_reports")
    legal_query = await filter_by_user_access(current_user, {}, "legal_documents")
    
    total_invoices = await db.invoices.count_documents(invoices_query)
    total_onjn_reports = await db.onjn_reports.count_documents(onjn_query)
    total_legal_documents = await db.legal_documents.count_documents(legal_query)
    
    # Get metrology and jackpot counts
    total_metrology = await db.metrology.count_documents({})
    total_jackpots = await db.jackpots.count_documents({})
    
    # Get comision dates count
    total_comision_dates = await db.comision_dates.count_documents({})
    
    # Get user count (only for admin)
    total_users = await db.users.count_documents({}) if current_user.role == UserRole.ADMIN else 0
    
    # Get recent activities based on user access
    recent_companies = await db.companies.find({"id": {"$in": accessible_companies}}).sort("created_at", -1).limit(3).to_list(3)
    recent_locations = await db.locations.find({"id": {"$in": accessible_locations}}).sort("created_at", -1).limit(3).to_list(3)
    
    # Get recent providers and cabinets based on access
    recent_providers = []
    recent_cabinets = []
    
    if current_user.role == UserRole.ADMIN:
        recent_providers = await db.providers.find({}).sort("created_at", -1).limit(2).to_list(2)
        recent_cabinets = await db.cabinets.find({}).sort("created_at", -1).limit(2).to_list(2)
    else:
        # Get providers used in accessible locations
        cabinets = await db.cabinets.find({"location_id": {"$in": accessible_locations}}).to_list(1000)
        provider_ids = list(set([cab["provider_id"] for cab in cabinets if "provider_id" in cab]))
        if provider_ids:
            recent_providers = await db.providers.find({"id": {"$in": provider_ids}}).sort("created_at", -1).limit(2).to_list(2)
        
        recent_cabinets = await db.cabinets.find({"location_id": {"$in": accessible_locations}}).sort("created_at", -1).limit(2).to_list(2)
    
    recent_activities = []
    for company in recent_companies:
        recent_activities.append({
            "type": "company",
            "action": "created",
            "name": company["name"],
            "date": company["created_at"].isoformat() if isinstance(company["created_at"], datetime) else company["created_at"]
        })
    
    for location in recent_locations:
        recent_activities.append({
            "type": "location",
            "action": "created",
            "name": location["name"],
            "date": location["created_at"].isoformat() if isinstance(location["created_at"], datetime) else location["created_at"]
        })
    
    for provider in recent_providers:
        recent_activities.append({
            "type": "provider",
            "action": "created",
            "name": provider["name"],
            "date": provider["created_at"].isoformat() if isinstance(provider["created_at"], datetime) else provider["created_at"]
        })
    
    for cabinet in recent_cabinets:
        recent_activities.append({
            "type": "cabinet",
            "action": "created",
            "name": f"{cabinet['name']} {cabinet['model']}",
            "date": cabinet["created_at"].isoformat() if isinstance(cabinet["created_at"], datetime) else cabinet["created_at"]
        })
    
    # Sort by date
    recent_activities.sort(key=lambda x: x["date"], reverse=True)
    recent_activities = recent_activities[:10]
    
    return DashboardStats(
        total_companies=total_companies,
        total_locations=total_locations,
        active_companies=active_companies,
        active_locations=active_locations,
        total_providers=total_providers,
        total_cabinets=total_cabinets,
        total_slot_machines=total_slot_machines,
        active_equipment=active_equipment,
        total_invoices=total_invoices,
        total_onjn_reports=total_onjn_reports,
        total_legal_documents=total_legal_documents,
        total_metrology=total_metrology,
        total_jackpots=total_jackpots,
        total_comision_dates=total_comision_dates,
        total_users=total_users,
        recent_activities=recent_activities
    )

@api_router.post("/change-history", response_model=ChangeHistory)
async def create_change_history(change_data: dict, current_user: User = Depends(get_current_user)):
    """Create a new change history record"""
    change_history = ChangeHistory(
        entity_type=change_data["entity_type"],
        entity_id=change_data["entity_id"],
        field_name=change_data["field_name"],
        old_value=change_data["old_value"],
        new_value=change_data["new_value"],
        change_type=change_data.get("change_type", "Scheduled"),
        scheduled_datetime=change_data["scheduled_datetime"],
        user_id=current_user.id,
        user_name=f"{current_user.first_name} {current_user.last_name}".strip()
    )
    
    result = await db.change_history.insert_one(change_history.model_dump())
    change_history.id = str(result.inserted_id)
    return change_history

@api_router.get("/change-history/{entity_type}/{entity_id}", response_model=List[dict])
async def get_change_history(entity_type: str, entity_id: str, current_user: User = Depends(get_current_user)):
    """Get change history for a specific entity"""
    # Get all changes for this entity, ordered by scheduled datetime (newest first)
    changes = await db.change_history.find({
        "entity_type": entity_type,
        "entity_id": entity_id
    }).sort("scheduled_datetime", -1).to_list(length=100)
    
    # Convert ObjectId to string and format dates
    for change in changes:
        change["id"] = str(change["_id"])
        del change["_id"]
        change["scheduled_datetime"] = change["scheduled_datetime"].isoformat()
        if change.get("applied_datetime"):
            change["applied_datetime"] = change["applied_datetime"].isoformat()
        change["created_at"] = change["created_at"].isoformat()
    
    return changes

@api_router.get("/change-history/{entity_type}/all", response_model=List[dict])
async def get_all_change_history(entity_type: str, current_user: User = Depends(get_current_user)):
    """Get recent change history for a specific entity type (newest first).

    Uses created_at primarily to include both manual and scheduled changes reliably.
    Falls back to scheduled_datetime when present for stable ordering.
    """
    query = {"entity_type": entity_type}
    # Prefer created_at for sorting; also add secondary sort on scheduled_datetime if present
    cursor = db.change_history.find(query).sort([
        ("created_at", -1),
        ("scheduled_datetime", -1),
    ])
    changes = await cursor.to_list(length=500)

    # Convert ObjectId to string and format dates
    for change in changes:
        change_id = change.get("_id")
        if change_id is not None:
            change["id"] = str(change_id)
            del change["_id"]
        # Safely stringify datetimes if present
        if change.get("scheduled_datetime"):
            change["scheduled_datetime"] = change["scheduled_datetime"].isoformat()
        if change.get("applied_datetime"):
            change["applied_datetime"] = change["applied_datetime"].isoformat()
        if change.get("created_at"):
            change["created_at"] = change["created_at"].isoformat()

    return changes

# ------------- Marketing APIs ------------- #

@api_router.post("/marketing/campaigns", response_model=MarketingCampaign)
async def create_marketing_campaign(campaign: MarketingCampaign, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    campaign_dict = campaign.model_dump()
    campaign_dict["created_by"] = current_user.id
    await db.marketing_campaigns.insert_one(campaign_dict)
    return campaign

@api_router.get("/marketing/campaigns", response_model=List[MarketingCampaign])
async def list_marketing_campaigns(current_user: User = Depends(get_current_user)):
    items = await db.marketing_campaigns.find({}).sort("created_at", -1).to_list(1000)
    return [MarketingCampaign(**it) for it in items]

@api_router.get("/marketing/campaigns/{campaign_id}", response_model=MarketingCampaign)
async def get_marketing_campaign(campaign_id: str, current_user: User = Depends(get_current_user)):
    it = await db.marketing_campaigns.find_one({"id": campaign_id})
    if not it:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return MarketingCampaign(**it)

@api_router.put("/marketing/campaigns/{campaign_id}", response_model=MarketingCampaign)
async def update_marketing_campaign(campaign_id: str, payload: dict, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    payload["updated_at"] = datetime.utcnow()
    await db.marketing_campaigns.update_one({"id": campaign_id}, {"$set": payload})
    it = await db.marketing_campaigns.find_one({"id": campaign_id})
    return MarketingCampaign(**it)

@api_router.delete("/marketing/campaigns/{campaign_id}")
async def delete_marketing_campaign(campaign_id: str, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    await db.marketing_campaigns.delete_one({"id": campaign_id})
    return {"message": "Deleted"}

class GenerateRecurringRequest(BaseModel):
    recurrence: Literal["daily", "weekly", "monthly"]
    amount: float
    from_date: datetime
    to_date: datetime
    location_ids: List[str]

@api_router.post("/marketing/campaigns/{campaign_id}/payouts/generate")
async def generate_recurring_payouts(campaign_id: str, body: GenerateRecurringRequest, current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    camp = await db.marketing_campaigns.find_one({"id": campaign_id})
    if not camp:
        raise HTTPException(status_code=404, detail="Campaign not found")
    payouts = camp.get("payouts", [])
    cursor = body.from_date
    while cursor <= body.to_date:
        for loc in body.location_ids:
            payouts.append({"date": cursor, "location_id": loc, "amount": body.amount})
        if body.recurrence == "daily":
            cursor = cursor + timedelta(days=1)
        elif body.recurrence == "weekly":
            cursor = cursor + timedelta(weeks=1)
        else:
            # monthly
            month = cursor.month + 1
            year = cursor.year + (1 if month > 12 else 0)
            month = 1 if month > 12 else month
            cursor = cursor.replace(year=year, month=month)
    await db.marketing_campaigns.update_one({"id": campaign_id}, {"$set": {"payouts": payouts, "updated_at": datetime.utcnow()}})
    return {"added": len(payouts)}


@api_router.put("/change-history/{change_id}/apply")
async def mark_change_applied(change_id: str, success: bool, current_user: User = Depends(get_current_user)):
    """Mark a change as applied with success/failure status"""
    result = await db.change_history.update_one(
        {"id": change_id},
        {
            "$set": {
                "applied_datetime": datetime.utcnow(),
                "applied_successfully": success
            }
        }
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Change history record not found")
    
    return {"message": "Change status updated successfully"}

@api_router.post("/fortune-teller", response_model=FortuneResponse)
async def get_slot_machine_fortune(request: FortuneRequest, current_user: User = Depends(get_current_user)):
    """
    🎰✨ Get a mystical fortune and prediction for your slot machines!
    This endpoint provides random fortunes, predictions, and advice for casino operators.
    """
    
    # Fortune messages
    fortunes = [
        "The stars align in your favor today! Your slot machines will bring great fortune.",
        "A mysterious energy surrounds your gaming floor. Expect unexpected wins!",
        "The ancient spirits of luck whisper secrets of prosperity to your machines.",
        "Your dedication to excellence will be rewarded with bountiful returns.",
        "The cosmic forces of chance smile upon your casino operations.",
        "A golden opportunity awaits in the most unexpected corner of your floor.",
        "Your slot machines are blessed with the magic of abundance.",
        "The universe conspires to bring success to your gaming enterprise.",
        "Fortune favors the bold, and you are among the boldest!",
        "Your machines hold the keys to unimaginable wealth and prosperity."
    ]
    
    # Predictions
    predictions = [
        "A record-breaking jackpot will be hit within the next 7 days.",
        "Your most popular slot machine will exceed all previous performance records.",
        "A VIP player will discover your casino and become a regular customer.",
        "Your slot machine maintenance schedule will prevent costly breakdowns.",
        "The new game mix you're considering will be a massive success.",
        "Your RTP optimization will result in increased player satisfaction.",
        "A strategic location change will boost machine performance by 25%.",
        "Your metrology compliance will earn you industry recognition.",
        "The jackpot system will generate unprecedented excitement.",
        "Your slot machine portfolio will become the envy of competitors."
    ]
    
    # Advice
    advice_list = [
        "Trust your instincts when making slot machine decisions.",
        "Regular maintenance is the key to long-term success.",
        "Listen to your players - they know what they want.",
        "Innovation and tradition can coexist beautifully.",
        "Patience in business decisions leads to lasting rewards.",
        "Your team's expertise is your greatest asset.",
        "Stay ahead of industry trends while maintaining quality.",
        "Balance risk and reward in your gaming strategy.",
        "Build relationships with providers for better deals.",
        "Focus on player experience, and profits will follow."
    ]
    
    # Generate random responses
    fortune = random.choice(fortunes)
    prediction = random.choice(predictions)
    lucky_number = random.randint(1, 777)  # Lucky casino number!
    advice = random.choice(advice_list)
    
    # Add personalized touch if serial number provided
    if request.slot_serial_number:
        fortune = f"🔮 For slot machine {request.slot_serial_number}: {fortune}"
        prediction = f"🎯 Specific prediction: {prediction}"
    
    # Add personalized touch if user question provided
    if request.user_question:
        advice = f"💭 Answering '{request.user_question}': {advice}"
    
    return FortuneResponse(
        fortune=fortune,
        prediction=prediction,
        lucky_number=lucky_number,
        advice=advice
    )

@api_router.get("/fortune-teller/daily", response_model=FortuneResponse)
async def get_daily_fortune(current_user: User = Depends(get_current_user)):
    """
    🌅 Get your daily fortune - a new prediction every day!
    """
    
    # Use date as seed for consistent daily fortunes
    today = date.today()
    random.seed(today.strftime("%Y-%m-%d"))
    
    daily_fortunes = [
        "Today is a day of new beginnings in your casino operations.",
        "The morning brings fresh opportunities for slot machine success.",
        "Your gaming floor will shine with positive energy today.",
        "A breakthrough in slot machine performance awaits you.",
        "Today's decisions will shape tomorrow's prosperity.",
        "The universe has planned something special for your casino today.",
        "Your slot machines are ready to deliver exceptional results.",
        "Today's challenges will reveal hidden opportunities.",
        "The stars have aligned for a day of gaming excellence.",
        "Your casino will attract the right players at the right time."
    ]
    
    daily_predictions = [
        "A major jackpot event will occur before sunset.",
        "Your slot machine analytics will reveal surprising insights.",
        "A VIP player will make their first appearance today.",
        "Your maintenance team will prevent a potential issue.",
        "Today's revenue will exceed expectations by 15%.",
        "A new game will become an instant hit with players.",
        "Your slot machine layout will receive positive feedback.",
        "Today's operations will set a new standard for excellence.",
        "A strategic insight will come from an unexpected source.",
        "Your casino will be mentioned positively in industry circles."
    ]
    
    daily_advice = [
        "Start your day with gratitude for your casino's success.",
        "Take time to observe your players' behavior patterns.",
        "Trust the process of continuous improvement.",
        "Celebrate small wins throughout the day.",
        "Stay focused on long-term goals while managing daily tasks.",
        "Your positive energy will attract positive results.",
        "Remember why you chose this exciting industry.",
        "Every challenge is an opportunity in disguise.",
        "Your passion for gaming will inspire your team.",
        "Success comes to those who prepare for it daily."
    ]
    
    fortune = random.choice(daily_fortunes)
    prediction = random.choice(daily_predictions)
    lucky_number = random.randint(1, 999)
    advice = random.choice(daily_advice)
    
    return FortuneResponse(
        fortune=fortune,
        prediction=prediction,
        lucky_number=lucky_number,
        advice=advice
    )





# Temporary endpoint to check users (remove after use)
@app.get("/check-users")
async def check_users():
    users = await db.users.find({}).to_list(1000)
    user_list = []
    for user in users:
        user_info = {
            "username": user.get("username"),
            "email": user.get("email"),
            "first_name": user.get("first_name"),
            "last_name": user.get("last_name"),
            "role": user.get("role"),
            "is_active": user.get("is_active", True)
        }
        user_list.append(user_info)
    return {"users": user_list}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_client():
    # Check if admin user exists
    admin_user = await db.users.find_one({"username": "admin"})
    if admin_user:
        logger.info("Admin user already exists")
        # Update admin user with proper names if they're empty
        if not admin_user.get("first_name") and not admin_user.get("last_name"):
            await db.users.update_one(
                {"username": "admin"},
                {"$set": {"first_name": "Eugeniu", "last_name": "Cazmal"}}
            )
            logger.info("Updated admin user with default names")
    else:
        logger.info("No admin user found - please create one manually")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

@api_router.get("/games")
async def get_games_from_sheets(current_user: User = Depends(get_current_user)):
    """
    Fetch games data directly from Google Sheets
    """
    try:
        # Google Sheets CSV export URL with your actual sheet ID and GID
        sheet_url = "https://docs.google.com/spreadsheets/d/14DTdJCtddVIwkA3mXC9IMwly70B7Is7TEVG6dcTbM14/export?format=csv&gid=837978082"
        
        response = requests.get(sheet_url, allow_redirects=True)
        response.raise_for_status()
        
        # Parse CSV data
        csv_data = StringIO(response.text)
        csv_reader = csv.DictReader(csv_data)
        
        games = []
        for row in csv_reader:
            # Map the exact column names from your Google Sheet
            game = {
                "id": row.get("game id", "").strip(),
                "game_name": row.get("Game Name", "").strip(),
                "provider": row.get("Provider", "").strip(),
                "game_provider_id": row.get("game_provider_id", "").strip(),
                "game_type_sub_category": row.get("game_type_sub_category", "").strip(),
                "game_type": row.get("game_type", "").strip(),
                "product": row.get("product", "").strip(),
                "classification": row.get("classification", "").strip(),
                "game_mechanic": row.get("game_mechanic", "").strip(),
                "theme": row.get("theme", "").strip(),
                "volatility": row.get("volatility", "").strip(),
                "lines": row.get("lines", "").strip(),
                "layout": row.get("layout", "").strip(),
                "link": row.get("link", "").strip()
            }
            
            # Only add if we have essential data
            if game["id"] and game["game_name"]:
                games.append(game)
        
        logger.info(f"Successfully fetched {len(games)} games from Google Sheets")
        return {"games": games, "count": len(games)}
            
    except Exception as e:
        logger.error(f"Error fetching games from Google Sheets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch games data: {str(e)}")

@api_router.post("/games/refresh")
async def refresh_games_data(current_user: User = Depends(get_current_user)):
    """
    Refresh games data from Google Sheets
    """
    return await get_games_from_sheets(current_user)

# Include the router in the main app
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)