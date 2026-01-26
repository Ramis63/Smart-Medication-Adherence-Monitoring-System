# Phase 2 Setup Instructions

## Overview

This document provides step-by-step instructions to set up and run Phase 2 of the MedHealth project - the Interactive Healthcare Data Visualization web application.

## Prerequisites

1. **Rust** (1.70+)
   - Install from: https://rustup.rs/
   - Verify: `rustc --version`

2. **SQLite Database**
   - Copy `medhealth.db` from Phase 1 to `backend/` directory
   - Or the backend will create a new one if it doesn't exist

3. **Web Browser**
   - Modern browser with WebSocket support (Chrome, Firefox, Edge)

## Backend Setup

### 1. Navigate to backend directory

```bash
cd backend
```

### 2. Create environment file

```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

### 3. Edit .env file (optional)

Default values:
```
HOST=127.0.0.1
PORT=8080
DATABASE_URL=medhealth.db
LOG_LEVEL=info
```

### 4. Build and run

```bash
# Build the project
cargo build

# Run the server
cargo run
```

The server will start on `http://127.0.0.1:8080`

### 5. Test the API

Open browser or use curl:
```
http://127.0.0.1:8080/api/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "medhealth-backend",
  "version": "0.1.0"
}
```

## Frontend Setup

### Option 1: Simple HTTP Server (Python)

```bash
cd frontend
python -m http.server 3000
```

Then open: `http://localhost:3000`

### Option 2: Node.js HTTP Server

```bash
cd frontend
npx http-server -p 3000
```

### Option 3: VS Code Live Server

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## Testing the Complete System

### 1. Start Backend

```bash
cd backend
cargo run
```

### 2. Start Frontend

```bash
cd frontend
python -m http.server 3000
```

### 3. Open Browser

Navigate to: `http://localhost:3000`

### 4. Test Features

- **Dashboard**: View statistics and overview
- **Medications**: View medication adherence timeline
- **Vital Signs**: View temperature and heart rate charts
- **Timeline**: Combined view of all data

## API Testing

### Get All Medications

```bash
curl http://127.0.0.1:8080/api/medications
```

### Get Medication Logs (FHIR)

```bash
curl http://127.0.0.1:8080/api/medications/1/logs
```

### Get Vital Signs (FHIR)

```bash
curl http://127.0.0.1:8080/api/vitals
```

## Troubleshooting

### Backend Issues

1. **Port already in use**
   - Change PORT in `.env` file
   - Or stop the process using port 8080

2. **Database not found**
   - Copy `medhealth.db` from Phase 1
   - Or backend will create a new empty database

3. **Compilation errors**
   - Run `cargo clean` and `cargo build` again
   - Check Rust version: `rustc --version` (should be 1.70+)

### Frontend Issues

1. **CORS errors**
   - Backend needs CORS headers (to be added)
   - Or use a proxy server

2. **WebSocket connection failed**
   - Ensure backend is running
   - Check WebSocket URL in `websocket.js`

3. **Charts not rendering**
   - Check browser console for errors
   - Ensure d3.js is loaded (check Network tab)

## Next Development Steps

1. Add CORS middleware to backend
2. Implement real-time data streaming in WebSockets
3. Complete d3.js visualizations
4. Add authentication
5. Add error handling and validation
6. Add unit tests
7. Deploy to production

## Course Requirements Progress

- ✅ Two-tier architecture (backend + frontend)
- ✅ FHIR-compliant JSON models
- ✅ REST API endpoints
- ✅ WebSocket infrastructure
- ⏳ Real-time data streaming (in progress)
- ⏳ Complete d3.js visualizations (in progress)
- ⏳ Authentication & security (pending)
- ⏳ Testing (pending)
- ⏳ Deployment (pending)

