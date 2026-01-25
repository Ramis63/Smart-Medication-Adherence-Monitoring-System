# Project Phase 2: Interactive Healthcare Data Visualization

## Overview

This phase converts the Raspberry Pi Medication Adherence System (Media Management project) into a web application with:
- **Backend**: Rust (Actix-web) emitting FHIR-compliant JSON
- **Frontend**: d3.js for real-time data visualization
- **Real-time Communication**: WebSockets for live data updates

## Course Requirements

Based on: https://github.com/dominikb1888/inco_new

### Deliverables
1. Web Application with real-time data visualization
2. Two-tier architecture:
   - Backend emitting FHIR-compliant JSON
   - Frontend using d3.js to visualize and interact with data
3. Real-time data transmission (WebSockets, may use pure binary)

### Course Materials
- "0 to Production in Rust" by Luca Palmieri
- Web Sockets in Actix
- Real-time Communication with Rust

## Data Model (FHIR Compliance)

### MedicationAdherence (FHIR MedicationStatement)
- Resource Type: MedicationStatement
- Status: taken, missed, not-taken
- Medication: Reference to Medication resource
- Subject: Patient reference
- EffectiveDateTime: When medication was taken
- Dosage: Schedule information

### VitalSigns (FHIR Observation)
- Resource Type: Observation
- Category: vital-signs
- Code: Temperature (8310-5) or Heart Rate (8867-4)
- ValueQuantity: Numeric value with unit
- EffectiveDateTime: When measurement was taken
- Subject: Patient reference

### Medication (FHIR Medication)
- Resource Type: Medication
- Code: Medication name
- Form: Tablet, capsule, etc.

## Project Structure

```
medhealth-web/
├── backend/              # Rust Actix-web backend
│   ├── src/
│   │   ├── main.rs
│   │   ├── handlers/     # API handlers
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
│   │   ├── app.js       # Main application
│   │   ├── charts.js    # d3.js visualizations
│   │   └── websocket.js # WebSocket client
│   └── assets/
├── database/            # SQLite database (from Phase 1)
│   └── medhealth.db
└── README.md
```

## Implementation Phases

### Phase 1: Backend Setup (Week 1-2)
- [ ] Initialize Rust project with Actix-web
- [ ] Set up database connection (SQLite)
- [ ] Create FHIR-compliant data models
- [ ] Implement basic REST API endpoints
- [ ] Add configuration management

### Phase 2: Data Migration (Week 2-3)
- [ ] Create database schema migration
- [ ] Export data from Phase 1 database
- [ ] Transform to FHIR format
- [ ] Import into new database

### Phase 3: WebSocket Implementation (Week 3-4)
- [ ] Implement WebSocket server (Actix)
- [ ] Real-time medication alarm notifications
- [ ] Real-time vital signs streaming
- [ ] Binary data transmission option

### Phase 4: Frontend Development (Week 4-5)
- [ ] Set up HTML/CSS structure
- [ ] Implement d3.js visualizations:
  - Medication adherence timeline
  - Vital signs charts (temperature, heart rate)
  - Real-time dashboard
- [ ] WebSocket client integration
- [ ] Interactive features

### Phase 5: Testing & Deployment (Week 5-6)
- [ ] Unit tests
- [ ] Integration tests
- [ ] FHIR validation
- [ ] Security testing
- [ ] Deployment setup

## Evaluation Criteria

Based on course checklist:

1. **Development Environment Setup**
   - Git with meaningful commits
   - Environment portability
   - CI/CD pipeline

2. **Unit & Integration Testing**
   - Core logic coverage
   - FHIR validation tests
   - API endpoint tests

3. **Configuration Management**
   - Dev/Stage/Prod configs
   - Environment variables
   - Secrets management

4. **Logging**
   - Structured logging
   - Error tracking
   - Performance metrics

5. **Deployment & System Architecture**
   - Containerized deployment
   - Modular architecture
   - Scalability

6. **Input Validation & Security**
   - FHIR schema validation
   - SQL injection protection
   - XSS protection

7. **Error Handling**
   - Graceful error handling
   - Meaningful error messages
   - Recovery mechanisms

8. **Authentication & Encryption**
   - Token-based auth
   - TLS encryption
   - Data encryption at rest

9. **Fault-tolerancy**
   - Retry logic
   - Circuit breakers
   - Fallback mechanisms

10. **FHIR Compliance**
    - FHIR resource modeling
    - Schema validation
    - Interoperability

## Next Steps

1. Initialize Rust backend project
2. Set up project structure
3. Create FHIR data models
4. Implement basic API endpoints
5. Set up frontend structure


