# MedHealth Backend - Rust Actix-web API

FHIR-compliant backend for the Medication Adherence and Health Monitoring System.

## Features

- RESTful API with FHIR-compliant JSON responses
- WebSocket support for real-time updates
- SQLite database integration
- Medication management endpoints
- Vital signs endpoints
- FHIR MedicationStatement and Observation resources
- Input validation and security
- Unit and integration tests
- Docker containerization support

## Setup

### Prerequisites

- Rust 1.70+ (install from https://rustup.rs/)
- SQLite database from Phase 1 (medhealth.db)

### Installation

```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
cargo build
```

### Running

```bash
cargo run
```

The server will start on `http://127.0.0.1:8080`

### Running Tests

```bash
cargo test
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build just the backend
docker build -t medhealth-backend ./backend
docker run -p 8080:8080 medhealth-backend
```

## API Endpoints

### Health Check
- `GET /api/health` - Server health status

### Medications
- `GET /api/medications` - Get all active medications
- `POST /api/medications` - Create new medication (requires validation)
- `GET /api/medications/{id}` - Get specific medication
- `DELETE /api/medications/{id}` - Delete medication
- `GET /api/medications/{id}/logs` - Get medication logs (FHIR MedicationStatement)

### Vital Signs
- `GET /api/vitals` - Get all vital signs (FHIR Observation)
- `POST /api/vitals` - Create new vital signs entry (requires validation)

### Logs
- `GET /api/logs/medications` - Get all medication logs
- `GET /api/logs/vitals` - Get all vital signs logs

### WebSockets
- `WS /ws/medications` - Real-time medication updates
- `WS /ws/vitals` - Real-time vital signs updates

## Input Validation

The API validates all inputs:

- **Medication names**: Max 100 characters, no HTML/script tags
- **Schedule times**: Must be in HH:MM format (0-23 hours, 0-59 minutes)
- **Temperature**: Must be between 20-45°C
- **Heart rate**: Must be between 30-250 bpm
- **Status**: Must be one of: normal, abnormal, warning

## Security

- SQL injection protection via parameterized queries
- Input sanitization and validation
- CORS configuration
- Optional API key authentication (set `API_KEY` environment variable)

## FHIR Compliance

All medication and vital signs data is returned in FHIR-compliant format:
- MedicationStatement for medication adherence
- Observation for vital signs (temperature, heart rate)
- LOINC codes: 8310-5 (temperature), 8867-4 (heart rate)

## Development

```bash
# Run with hot reload (requires cargo-watch)
cargo install cargo-watch
cargo watch -x run
```

## Testing

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_create_medication
```

## Environment Variables

Create a `.env` file:

```
HOST=127.0.0.1
PORT=8080
DATABASE_URL=medhealth.db
LOG_LEVEL=info
API_KEY=your-secret-key-here  # Optional, for authentication
```

## Docker Deployment

```bash
# Build
docker build -t medhealth-backend ./backend

# Run
docker run -p 8080:8080 \
  -e HOST=0.0.0.0 \
  -e PORT=8080 \
  -e DATABASE_URL=medhealth.db \
  -v $(pwd)/medhealth.db:/app/medhealth.db \
  medhealth-backend
```

## CI/CD

GitHub Actions workflow is configured in `.github/workflows/ci.yml`:
- Automated testing on push/PR
- Code formatting checks
- Clippy linting
