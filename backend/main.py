"""
AI-Powered Disaster Response Platform - Main Backend
FastAPI application with authentication, real-time updates, and resource management
"""
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
import os
from ai_engine.disaster_prediction import DisasterPredictor
from ai_engine.resource_optimizer import ResourceOptimizer
from services.alert_service import AlertService
import numpy as np
from dotenv import load_dotenv
load_dotenv()
from bson import ObjectId
import asyncio
import subprocess

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

# Initialize FastAPI
app = FastAPI(
    title="Disaster Response API",
    description="AI-Powered Disaster Management Platform",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database
client = AsyncIOMotorClient(MONGODB_URL)
db = client.disaster_management
predictor = DisasterPredictor()
optimizer = ResourceOptimizer()
alerter = AlertService()

# Data Models
class User(BaseModel):
    username: str
    email: str
    role: str = "user"

class Token(BaseModel):
    access_token: str
    token_type: str

class Incident(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    disaster_type: str
    severity: int = Field(..., ge=1, le=5)
    latitude: float
    longitude: float
    status: str = "active"
    reported_by: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Resource(BaseModel):
    id: Optional[str] = None
    name: str
    type: str
    quantity: int
    location_lat: float
    location_lng: float
    status: str = "available"

class Alert(BaseModel):
    id: Optional[str] = None
    message: str
    severity: str
    disaster_type: str
    affected_areas: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Helper Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return username
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def fix_mongo_ids(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# API Routes
@app.get("/")
async def root():
    return {"message": "Disaster Response API", "status": "operational"}

@app.post("/register")
async def register(username: str, email: str, password: str):
    if len(password) > 72:
        raise HTTPException(status_code=400, detail="Password cannot be longer than 72 characters.")
    existing = await db.users.find_one({"username": username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = {
        "username": username,
        "email": email,
        "hashed_password": get_password_hash(password),
        "role": "user",
        "created_at": datetime.utcnow()
    }
    await db.users.insert_one(user)
    return {"message": "User registered successfully"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await db.users.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/incidents")
async def create_incident(incident: Incident, current_user: str = Depends(get_current_user)):
    incident.reported_by = current_user
    result = await db.incidents.insert_one(incident.dict())
    incident.id = str(result.inserted_id)
    await manager.broadcast({"type": "new_incident", "data": incident.dict()})
    return incident

# —— PUBLIC (no login needed) ——
@app.get("/incidents")
async def get_incidents():
    incidents = await db.incidents.find().to_list(100)
    return [fix_mongo_ids(doc) for doc in incidents]

@app.post("/resources")
async def create_resource(resource: Resource, current_user: str = Depends(get_current_user)):
    result = await db.resources.insert_one(resource.dict())
    resource.id = str(result.inserted_id)
    return resource

# —— PUBLIC (no login needed) ——
@app.get("/resources")
async def get_resources():
    resources = await db.resources.find().to_list(100)
    return [fix_mongo_ids(doc) for doc in resources]

@app.post("/alerts")
async def create_alert(alert: Alert, current_user: str = Depends(get_current_user)):
    result = await db.alerts.insert_one(alert.dict())
    alert.id = str(result.inserted_id)
    await manager.broadcast({"type": "alert", "data": alert.dict()})
    return alert

@app.get("/alerts")
async def get_alerts():
    alerts = await db.alerts.find().sort("created_at", -1).to_list(50)
    return [fix_mongo_ids(doc) for doc in alerts]

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast({"type": "message", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

from fastapi import Body
@app.post("/predict/{disaster_type}")
async def predict_disaster(disaster_type: str, payload: dict = Body(...)):
    disaster_type = disaster_type.lower()
    if disaster_type == "flood":
        result = predictor.predict_flood_risk(
            payload["rainfall"], payload["river_level"], payload["soil_moisture"],
            payload["temperature"], payload["humidity"]
        )
    elif disaster_type == "earthquake":
        result = predictor.predict_earthquake_risk(
            payload["magnitude"], payload["depth"], payload["distance_from_fault"], payload["peak_ground_accel"]
        )
    elif disaster_type == "cloudburst":
        result = predictor.predict_cloudburst_risk(
            payload["rainfall_rate"], payload["duration"],
            payload["cloud_water_content"], payload["temp_diff"]
        )
    elif disaster_type == "avalanche":
        result = predictor.predict_avalanche_risk(
            payload["snow_depth"], payload["slope_angle"],
            payload["temperature"], payload["wind_speed"]
        )
    else:
        raise HTTPException(status_code=400, detail="Unknown disaster type")
    return result

@app.post("/optimize/resources")
async def optimize_resources(payload: dict = Body(...)):
    resource_coords = np.array(payload["resource_coords"])
    incident_coords = np.array(payload["incident_coords"])
    assignments, costs = optimizer.assign_resources(resource_coords, incident_coords)
    return {"assignments": assignments, "costs": costs.tolist()}

@app.post("/alerts/sms")
async def send_sms_api(payload: dict = Body(...)):
    message = payload.get("message", "")
    to = payload.get("to", "")
    ok = alerter.send_sms(message, to)
    return {"success": ok}

@app.post("/alerts/email")
async def send_email_api(payload: dict = Body(...)):
    subject = payload.get("subject", "")
    message = payload.get("message", "")
    to = payload.get("to", "")
    ok = alerter.send_email(subject, message, to)
    return {"success": ok}

@app.on_event("startup")
async def run_fetch_script_periodically():
    async def fetch_loop():
        while True:
            try:
                subprocess.run(["python", "fetch_earthquake.py"])
            except Exception as e:
                print("fetch_earthquake.py error:", e)
            await asyncio.sleep(1800)  # every 30 minutes
    asyncio.create_task(fetch_loop())

@app.on_event("startup")
async def run_fetch_flood_periodically():
    async def fetch_loop():
        while True:
            try:
                subprocess.run(["python", "fetch_flood.py"])
            except Exception as e:
                print("fetch_flood.py error:", e)
            await asyncio.sleep(1800)
    asyncio.create_task(fetch_loop())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
