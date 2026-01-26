use crate::config::AppConfig;
use crate::database;
use crate::models::{Medication, MedicationLog, MedicationStatement, Observation, VitalsLog};
use actix_web::{web, HttpResponse, Result};
use log::error;
use rusqlite::params;

mod retry;

#[cfg(test)]
mod tests;

pub async fn get_medications(config: web::Data<AppConfig>) -> Result<HttpResponse> {
    let conn = database::get_connection(&config.database_url).map_err(|e| {
        error!("Database error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    let mut stmt = conn
        .prepare(
            "SELECT id, name, schedule_time, active, created_at FROM medications WHERE active = 1",
        )
        .map_err(|e| {
            error!("Prepare error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    let med_iter = stmt
        .query_map([], |row| {
            Ok(Medication {
                id: row.get(0)?,
                name: row.get(1)?,
                schedule_time: row.get(2)?,
                active: row.get::<_, i32>(3)? == 1,
                created_at: row.get(4)?,
            })
        })
        .map_err(|e| {
            error!("Query error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    let medications: Vec<Medication> = med_iter.collect::<Result<Vec<_>, _>>().map_err(|e| {
        error!("Collection error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    Ok(HttpResponse::Ok().json(medications))
}

// Input validation helper
fn validate_medication_name(name: &str) -> Result<(), actix_web::Error> {
    if name.is_empty() {
        return Err(actix_web::error::ErrorBadRequest(
            "Medication name cannot be empty",
        ));
    }
    if name.len() > 100 {
        return Err(actix_web::error::ErrorBadRequest(
            "Medication name too long (max 100 characters)",
        ));
    }
    // Sanitize: remove potentially dangerous characters
    if name.contains('<') || name.contains('>') || name.contains('"') || name.contains('\'') {
        return Err(actix_web::error::ErrorBadRequest(
            "Invalid characters in medication name",
        ));
    }
    Ok(())
}

fn validate_schedule_time(time: &str) -> Result<(), actix_web::Error> {
    // Validate HH:MM format
    let parts: Vec<&str> = time.split(':').collect();
    if parts.len() != 2 {
        return Err(actix_web::error::ErrorBadRequest(
            "Invalid time format. Use HH:MM",
        ));
    }
    if let (Ok(hour), Ok(minute)) = (parts[0].parse::<u8>(), parts[1].parse::<u8>()) {
        if hour > 23 || minute > 59 {
            return Err(actix_web::error::ErrorBadRequest(
                "Invalid time. Hour must be 0-23, minute must be 0-59",
            ));
        }
    } else {
        return Err(actix_web::error::ErrorBadRequest(
            "Time must be numeric (HH:MM)",
        ));
    }
    Ok(())
}

pub async fn create_medication(
    config: web::Data<AppConfig>,
    med: web::Json<serde_json::Value>,
) -> Result<HttpResponse> {
    let conn = database::get_connection(&config.database_url).map_err(|e| {
        error!("Database error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    let name = med["name"].as_str().unwrap_or("").trim();
    let schedule_time = med["schedule_time"].as_str().unwrap_or("").trim();

    // Input validation
    validate_medication_name(name)?;
    validate_schedule_time(schedule_time)?;

    conn.execute(
        "INSERT INTO medications (name, schedule_time) VALUES (?1, ?2)",
        params![name, schedule_time],
    )
    .map_err(|e| {
        error!("Insert error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    Ok(HttpResponse::Created().json(serde_json::json!({
        "status": "created",
        "name": name,
        "schedule_time": schedule_time
    })))
}

pub async fn get_medication(
    config: web::Data<AppConfig>,
    path: web::Path<i32>,
) -> Result<HttpResponse> {
    let id = path.into_inner();
    let conn = database::get_connection(&config.database_url).map_err(|e| {
        error!("Database error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    let med = conn
        .query_row(
            "SELECT id, name, schedule_time, active, created_at FROM medications WHERE id = ?1",
            params![id],
            |row| {
                Ok(Medication {
                    id: row.get(0)?,
                    name: row.get(1)?,
                    schedule_time: row.get(2)?,
                    active: row.get::<_, i32>(3)? == 1,
                    created_at: row.get(4)?,
                })
            },
        )
        .map_err(|e| {
            error!("Query error: {}", e);
            actix_web::error::ErrorNotFound("Medication not found")
        })?;

    Ok(HttpResponse::Ok().json(med))
}

pub async fn delete_medication(
    config: web::Data<AppConfig>,
    path: web::Path<i32>,
) -> Result<HttpResponse> {
    let id = path.into_inner();
    let conn = database::get_connection(&config.database_url).map_err(|e| {
        error!("Database error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    conn.execute(
        "UPDATE medications SET active = 0 WHERE id = ?1",
        params![id],
    )
    .map_err(|e| {
        error!("Update error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    Ok(HttpResponse::Ok().json(serde_json::json!({
        "status": "deleted",
        "id": id
    })))
}

pub async fn get_medication_logs(
    config: web::Data<AppConfig>,
    path: web::Path<i32>,
) -> Result<HttpResponse> {
    let med_id = path.into_inner();
    let conn = database::get_connection(&config.database_url).map_err(|e| {
        error!("Database error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    let mut stmt = conn
        .prepare(
            "SELECT id, medication_id, medication_name, scheduled_time, actual_time, 
         status, temperature, heart_rate, created_at 
         FROM medication_logs WHERE medication_id = ?1 ORDER BY created_at DESC LIMIT 20",
        )
        .map_err(|e| {
            error!("Prepare error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    let log_iter = stmt
        .query_map(params![med_id], |row| {
            Ok(MedicationLog {
                id: row.get(0)?,
                medication_id: row.get(1)?,
                medication_name: row.get(2)?,
                scheduled_time: row.get(3)?,
                actual_time: row.get(4)?,
                status: row.get(5)?,
                temperature: row.get(6)?,
                heart_rate: row.get(7)?,
                created_at: row.get(8)?,
            })
        })
        .map_err(|e| {
            error!("Query error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    let logs: Vec<MedicationLog> = log_iter.collect::<Result<Vec<_>, _>>().map_err(|e| {
        error!("Collection error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    // Convert to FHIR MedicationStatement
    let fhir_statements: Vec<MedicationStatement> =
        logs.iter().map(MedicationStatement::from_db_log).collect();

    Ok(HttpResponse::Ok().json(fhir_statements))
}

pub async fn get_all_medication_logs(config: web::Data<AppConfig>) -> Result<HttpResponse> {
    let conn = database::get_connection(&config.database_url).map_err(|e| {
        error!("Database error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    let mut stmt = conn
        .prepare(
            "SELECT id, medication_id, medication_name, scheduled_time, actual_time, 
         status, temperature, heart_rate, created_at 
         FROM medication_logs ORDER BY created_at DESC LIMIT 100",
        )
        .map_err(|e| {
            error!("Prepare error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    let log_iter = stmt
        .query_map([], |row| {
            Ok(MedicationLog {
                id: row.get(0)?,
                medication_id: row.get(1)?,
                medication_name: row.get(2)?,
                scheduled_time: row.get(3)?,
                actual_time: row.get(4)?,
                status: row.get(5)?,
                temperature: row.get(6)?,
                heart_rate: row.get(7)?,
                created_at: row.get(8)?,
            })
        })
        .map_err(|e| {
            error!("Query error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    let logs: Vec<MedicationLog> = log_iter.collect::<Result<Vec<_>, _>>().map_err(|e| {
        error!("Collection error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    // Convert to FHIR
    let fhir_statements: Vec<MedicationStatement> =
        logs.iter().map(MedicationStatement::from_db_log).collect();

    Ok(HttpResponse::Ok().json(fhir_statements))
}

pub async fn get_vitals(config: web::Data<AppConfig>) -> Result<HttpResponse> {
    let conn = database::get_connection(&config.database_url).map_err(|e| {
        error!("Database error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    let mut stmt = conn
        .prepare(
            "SELECT id, temperature, heart_rate, status, created_at 
         FROM vitals_logs ORDER BY created_at DESC LIMIT 100",
        )
        .map_err(|e| {
            error!("Prepare error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    let vitals_iter = stmt
        .query_map([], |row| {
            Ok(VitalsLog {
                id: row.get(0)?,
                temperature: row.get(1)?,
                heart_rate: row.get(2)?,
                status: row.get(3)?,
                created_at: row.get(4)?,
            })
        })
        .map_err(|e| {
            error!("Query error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    let vitals: Vec<VitalsLog> = vitals_iter.collect::<Result<Vec<_>, _>>().map_err(|e| {
        error!("Collection error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    // Convert to FHIR Observations
    let mut observations: Vec<Observation> = Vec::new();
    for log in &vitals {
        if let Some(temp_obs) = Observation::temperature_from_db(log) {
            observations.push(temp_obs);
        }
        if let Some(hr_obs) = Observation::heart_rate_from_db(log) {
            observations.push(hr_obs);
        }
    }

    Ok(HttpResponse::Ok().json(observations))
}

fn validate_vitals(
    temperature: Option<f64>,
    heart_rate: Option<i32>,
) -> Result<(), actix_web::Error> {
    if let Some(temp) = temperature {
        if !(20.0..=45.0).contains(&temp) {
            return Err(actix_web::error::ErrorBadRequest(
                "Temperature out of valid range (20-45°C)",
            ));
        }
    }
    if let Some(hr) = heart_rate {
        if !(30..=250).contains(&hr) {
            return Err(actix_web::error::ErrorBadRequest(
                "Heart rate out of valid range (30-250 bpm)",
            ));
        }
    }
    Ok(())
}

pub async fn create_vitals(
    config: web::Data<AppConfig>,
    vitals: web::Json<serde_json::Value>,
) -> Result<HttpResponse> {
    let conn = database::get_connection(&config.database_url).map_err(|e| {
        error!("Database error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    let temperature = vitals["temperature"].as_f64();
    let heart_rate = vitals["heart_rate"].as_i64().map(|v| v as i32);
    let status = vitals["status"].as_str().unwrap_or("normal").to_string();

    // Input validation
    validate_vitals(temperature, heart_rate)?;

    // Validate status
    let valid_statuses = ["normal", "abnormal", "warning"];
    if !valid_statuses.contains(&status.as_str()) {
        return Err(actix_web::error::ErrorBadRequest(
            "Invalid status. Must be: normal, abnormal, or warning",
        ));
    }

    conn.execute(
        "INSERT INTO vitals_logs (temperature, heart_rate, status) VALUES (?1, ?2, ?3)",
        params![temperature, heart_rate, status],
    )
    .map_err(|e| {
        error!("Insert error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    Ok(HttpResponse::Created().json(serde_json::json!({
        "status": "created",
        "temperature": temperature,
        "heart_rate": heart_rate
    })))
}

pub async fn get_all_vitals_logs(config: web::Data<AppConfig>) -> Result<HttpResponse> {
    get_vitals(config).await
}
