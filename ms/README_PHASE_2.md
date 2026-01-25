# Phase 2: Interactive Healthcare Data Visualization

## Overview

This phase converts the Raspberry Pi Medication Adherence System into a web application with:
- **Backend**: Rust (Actix-web) with FHIR-compliant JSON API
- **Frontend**: d3.js for real-time data visualization
- **Real-time Communication**: WebSockets for live updates

## Project Structure

```
medhealth-web/
├── backend/              # Rust Actix-web backend
│   ├── src/
│   │   ├── main.rs      # Main server
│   │   ├── handlers/    # API handlers
│   │   ├── models/      # FHIR data models
│   │   ├── database/    # Database connection
│   │   ├── websocket/   # WebSocket handlers
│   │   └── config.rs    # Configuration
│   ├── Cargo.toml
│   └── .env
├── frontend/            # d3.js frontend
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
└── README.md
```

## Quick Start

### Backend

```bash
cd backend
cp .env.example .env
cargo run
```

Server runs on `http://127.0.0.1:8080`

### Frontend

Open `frontend/index.html` in a web browser or use a local server:

```bash
cd frontend
python -m http.server 3000
```

Then open `http://localhost:3000`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/medications` - Get all medications
- `POST /api/medications` - Create medication
- `GET /api/medications/{id}/logs` - Get medication logs (FHIR)
- `GET /api/vitals` - Get vital signs (FHIR)
- `WS /ws/medications` - WebSocket for medication updates
- `WS /ws/vitals` - WebSocket for vital signs updates

## FHIR Compliance

All data is returned in FHIR-compliant format:
- **MedicationStatement** for medication adherence
- **Observation** for vital signs (LOINC codes: 8310-5 for temperature, 8867-4 for heart rate)

## Next Steps

1. Complete WebSocket real-time data streaming
2. Implement full d3.js visualizations
3. Add authentication and security
4. Deploy to production

## Course Requirements

Based on: https://github.com/dominikb1888/inco_new

This project fulfills the requirements for:
- Two-tier architecture (backend + frontend)
- FHIR-compliant JSON
- Real-time data visualization with d3.js
- WebSocket communication

