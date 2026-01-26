// WebSocket client for real-time updates
const WS_BASE = 'ws://127.0.0.1:8080/ws';

let medicationWS = null;
let vitalsWS = null;

function connectMedicationWebSocket() {
    if (medicationWS) return;
    
    medicationWS = new WebSocket(`${WS_BASE}/medications`);
    
    medicationWS.onopen = () => {
        console.log('Medication WebSocket connected');
    };
    
    medicationWS.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleMedicationUpdate(data);
        } catch (e) {
            console.error('Error parsing medication update:', e);
        }
    };
    
    medicationWS.onerror = (error) => {
        console.error('Medication WebSocket error:', error);
    };
    
    medicationWS.onclose = () => {
        console.log('Medication WebSocket closed');
        medicationWS = null;
        // Reconnect after 5 seconds
        setTimeout(connectMedicationWebSocket, 5000);
    };
}

function connectVitalsWebSocket() {
    if (vitalsWS) return;
    
    vitalsWS = new WebSocket(`${WS_BASE}/vitals`);
    
    vitalsWS.onopen = () => {
        console.log('Vitals WebSocket connected');
    };
    
    vitalsWS.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            handleVitalsUpdate(data);
        } catch (e) {
            console.error('Error parsing vitals update:', e);
        }
    };
    
    vitalsWS.onerror = (error) => {
        console.error('Vitals WebSocket error:', error);
    };
    
    vitalsWS.onclose = () => {
        console.log('Vitals WebSocket closed');
        vitalsWS = null;
        // Reconnect after 5 seconds
        setTimeout(connectVitalsWebSocket, 5000);
    };
}

function handleMedicationUpdate(data) {
    // Update medications array and re-render
    console.log('Medication update received:', data);
    // Trigger UI update
    if (typeof window.updateMedications === 'function') {
        window.updateMedications(data);
    }
}

function handleVitalsUpdate(data) {
    // Update vitals array and re-render
    console.log('Vitals update received:', data);
    // Trigger UI update
    if (typeof window.updateVitals === 'function') {
        window.updateVitals(data);
    }
}

// Initialize connections
if (typeof window !== 'undefined') {
    window.addEventListener('load', () => {
        connectMedicationWebSocket();
        connectVitalsWebSocket();
    });
}


