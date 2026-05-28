from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
import os
from datetime import datetime

app = FastAPI(title="OrbitalWatch API", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
FIRMS_BASE = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat(), "service": "OrbitalWatch"}

@app.get("/api/fires")
async def get_fire_data():
    """Retorna focos de calor ativos no Brasil via NASA FIRMS API"""
    try:
        url = f"{FIRMS_BASE}/{NASA_API_KEY}/VIIRS_SNPP_NRT/BRA/1"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            return JSONResponse({"error": "NASA API indisponível", "fires": [], "source": "nasa_firms"}, status_code=503)
        
        lines = response.text.strip().split("\n")
        fires = []
        if len(lines) > 1:
            headers = lines[0].split(",")
            for line in lines[1:101]:  # limita 100 registros
                values = line.split(",")
                if len(values) >= len(headers):
                    record = dict(zip(headers, values))
                    fires.append({
                        "lat": float(record.get("latitude", 0)),
                        "lon": float(record.get("longitude", 0)),
                        "brightness": float(record.get("bright_ti4", 0)),
                        "date": record.get("acq_date", ""),
                        "confidence": record.get("confidence", ""),
                        "satellite": record.get("satellite", "VIIRS"),
                    })
        
        return {
            "fires": fires,
            "total": len(fires),
            "source": "NASA FIRMS VIIRS",
            "region": "Brasil",
            "updated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        # Dados simulados para demo quando API não responde
        return {
            "fires": [
                {"lat": -3.47, "lon": -62.21, "brightness": 342.1, "date": datetime.utcnow().strftime("%Y-%m-%d"), "confidence": "high", "satellite": "VIIRS"},
                {"lat": -9.81, "lon": -55.49, "brightness": 318.7, "date": datetime.utcnow().strftime("%Y-%m-%d"), "confidence": "nominal", "satellite": "VIIRS"},
                {"lat": -12.34, "lon": -50.12, "brightness": 356.2, "date": datetime.utcnow().strftime("%Y-%m-%d"), "confidence": "high", "satellite": "VIIRS"},
                {"lat": -6.22, "lon": -57.83, "brightness": 301.5, "date": datetime.utcnow().strftime("%Y-%m-%d"), "confidence": "low", "satellite": "VIIRS"},
                {"lat": -15.77, "lon": -47.93, "brightness": 389.0, "date": datetime.utcnow().strftime("%Y-%m-%d"), "confidence": "high", "satellite": "VIIRS"},
            ],
            "total": 5,
            "source": "Dados simulados (demo)",
            "region": "Brasil",
            "updated_at": datetime.utcnow().isoformat()
        }

@app.get("/api/stats")
async def get_stats():
    """Estatísticas gerais da plataforma"""
    return {
        "satellites_monitored": 6847,
        "active_alerts": 12,
        "area_monitored_km2": 8_515_767,
        "data_points_today": 142_380,
        "ods": "ODS 13 - Ação Climática",
        "last_update": datetime.utcnow().isoformat()
    }
