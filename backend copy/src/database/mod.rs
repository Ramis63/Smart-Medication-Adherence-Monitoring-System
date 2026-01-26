use rusqlite::{Connection, Result as SqlResult};
use log::info;

pub fn init_db(db_path: &str) -> SqlResult<()> {
    let conn = Connection::open(db_path)?;
    
    // Create tables if they don't exist (matching Phase 1 schema)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            schedule_time TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )",
        [],
    )?;
    
    conn.execute(
        "CREATE TABLE IF NOT EXISTS medication_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medication_id INTEGER,
            medication_name TEXT,
            scheduled_time TEXT,
            actual_time TEXT,
            status TEXT,
            temperature REAL,
            heart_rate INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medication_id) REFERENCES medications(id)
        )",
        [],
    )?;
    
    conn.execute(
        "CREATE TABLE IF NOT EXISTS vitals_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            heart_rate INTEGER,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )",
        [],
    )?;
    
    info!("Database initialized successfully: {}", db_path);
    Ok(())
}

pub fn get_connection(db_path: &str) -> SqlResult<Connection> {
    Connection::open(db_path)
}


