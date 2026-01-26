// Main application controller
const API_BASE = 'http://127.0.0.1:8080/api';
let currentView = 'dashboard';
let medications = [];
let vitals = [];

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    loadInitialData();
    setupWebSockets();
    setInterval(updateDashboard, 5000); // Update every 5 seconds
});

// Navigation
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            switchView(view);
            navButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

function switchView(view) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(`${view}-view`).classList.add('active');
    currentView = view;
    
    // Load view-specific data
    switch(view) {
        case 'medications':
            renderMedicationTimeline();
            break;
        case 'vitals':
            renderVitalSignsCharts();
            break;
        case 'timeline':
            renderCombinedTimeline();
            break;
        case 'dashboard':
            renderDashboardCharts();
            break;
    }
}

// Load initial data
async function loadInitialData() {
    try {
        const [medsRes, vitalsRes] = await Promise.all([
            fetch(`${API_BASE}/medications`),
            fetch(`${API_BASE}/vitals`)
        ]);
        
        medications = await medsRes.json();
        vitals = await vitalsRes.json();
        
        updateDashboard();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Update dashboard
async function updateDashboard() {
    // Update stats
    const activeMeds = medications.filter(m => m.active).length;
    document.getElementById('active-meds-count').textContent = activeMeds;
    
    // Get today's taken count
    try {
        const logsRes = await fetch(`${API_BASE}/logs/medications`);
        const logs = await logsRes.json();
        const today = new Date().toISOString().split('T')[0];
        const takenToday = logs.filter(log => {
            const dateStr = log.effectiveDateTime || log.effective_date_time || '';
            const logDate = dateStr.split('T')[0];
            const status = log.status?.toLowerCase() || '';
            return logDate === today && (status === 'completed' || status === 'taken');
        }).length;
        document.getElementById('taken-today').textContent = takenToday;
    } catch (e) {
        document.getElementById('taken-today').textContent = '--';
    }
    
    // Get latest vitals (handle both camelCase and snake_case)
    const latestVitals = vitals
        .filter(v => (v.resourceType === 'Observation' || v.resource_type === 'Observation'))
        .sort((a, b) => {
            const dateA = new Date(a.effectiveDateTime || a.effective_date_time || 0);
            const dateB = new Date(b.effectiveDateTime || b.effective_date_time || 0);
            return dateB - dateA;
        });
    
    const latestTemp = latestVitals.find(v => {
        const code = v.code?.coding?.[0]?.code;
        return code === '8310-5';
    });
    const latestHR = latestVitals.find(v => {
        const code = v.code?.coding?.[0]?.code;
        return code === '8867-4';
    });
    
    if (latestTemp?.valueQuantity || latestTemp?.value_quantity) {
        const value = latestTemp.valueQuantity?.value || latestTemp.value_quantity?.value;
        document.getElementById('current-temp').textContent = 
            `${value.toFixed(1)}°C`;
    } else {
        document.getElementById('current-temp').textContent = '--°C';
    }
    
    if (latestHR?.valueQuantity || latestHR?.value_quantity) {
        const value = latestHR.valueQuantity?.value || latestHR.value_quantity?.value;
        document.getElementById('current-hr').textContent = 
            `${Math.round(value)} bpm`;
    } else {
        document.getElementById('current-hr').textContent = '-- bpm';
    }
    
    // Render dashboard charts if on dashboard view
    if (currentView === 'dashboard') {
        renderDashboardCharts();
    }
}

// Render functions
async function renderDashboardCharts() {
    try {
        const res = await fetch(`${API_BASE}/logs/medications`);
        const data = await res.json();
        if (data.length > 0 && window.renderMedicationAdherenceTimeline) {
            window.renderMedicationAdherenceTimeline(data.slice(0, 20), 'dashboard-charts');
        } else {
            document.getElementById('dashboard-charts').innerHTML = 
                '<p style="text-align: center; padding: 50px; color: #666;">No medication data available</p>';
        }
    } catch (error) {
        console.error('Error rendering dashboard charts:', error);
        document.getElementById('dashboard-charts').innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">Error loading charts</p>';
    }
}

async function renderMedicationTimeline() {
    try {
        const res = await fetch(`${API_BASE}/logs/medications`);
        const data = await res.json();
        if (data.length > 0 && window.renderMedicationAdherenceTimeline) {
            window.renderMedicationAdherenceTimeline(data, 'medication-timeline');
        } else {
            document.getElementById('medication-timeline').innerHTML = 
                '<p style="text-align: center; padding: 50px; color: #666;">No medication data available</p>';
        }
    } catch (error) {
        console.error('Error rendering medication timeline:', error);
        document.getElementById('medication-timeline').innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">Error loading timeline</p>';
    }
}

async function renderVitalSignsCharts() {
    try {
        const res = await fetch(`${API_BASE}/vitals`);
        const data = await res.json();
        if (data.length > 0) {
            if (window.renderTemperatureChart) {
                window.renderTemperatureChart(data, 'temperature-chart');
            }
            if (window.renderHeartRateChart) {
                window.renderHeartRateChart(data, 'heartrate-chart');
            }
        } else {
            document.getElementById('temperature-chart').innerHTML = 
                '<p style="text-align: center; padding: 50px; color: #666;">No vital signs data available</p>';
            document.getElementById('heartrate-chart').innerHTML = 
                '<p style="text-align: center; padding: 50px; color: #666;">No vital signs data available</p>';
        }
    } catch (error) {
        console.error('Error rendering vital signs charts:', error);
        document.getElementById('temperature-chart').innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">Error loading charts</p>';
        document.getElementById('heartrate-chart').innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">Error loading charts</p>';
    }
}

async function renderCombinedTimeline() {
    try {
        const [medsRes, vitalsRes] = await Promise.all([
            fetch(`${API_BASE}/logs/medications`),
            fetch(`${API_BASE}/vitals`)
        ]);
        const meds = await medsRes.json();
        const vitals = await vitalsRes.json();
        
        if (meds.length > 0 && window.renderMedicationAdherenceTimeline) {
            window.renderMedicationAdherenceTimeline(meds, 'combined-timeline');
        } else {
            document.getElementById('combined-timeline').innerHTML = 
                '<p style="text-align: center; padding: 50px; color: #666;">No data available</p>';
        }
    } catch (error) {
        console.error('Error rendering combined timeline:', error);
        document.getElementById('combined-timeline').innerHTML = 
            '<p style="text-align: center; padding: 50px; color: #666;">Error loading timeline</p>';
    }
}

// WebSocket setup
function setupWebSockets() {
    // WebSocket setup is handled in websocket.js
    console.log('WebSocket setup initialized');
}
