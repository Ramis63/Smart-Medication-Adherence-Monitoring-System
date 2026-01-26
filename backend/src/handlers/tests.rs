#[cfg(test)]
mod tests {
    use crate::config::AppConfig;
    use crate::database;
    use crate::handlers::{create_medication, create_vitals, get_medications};
    use actix_web::{http::header, test, web, App};
    use std::env;

    fn get_test_config() -> AppConfig {
        AppConfig {
            host: "127.0.0.1".to_string(),
            port: 8080,
            database_url: "test_handlers.db".to_string(),
            log_level: "test".to_string(),
        }
    }

    fn auth_header_value() -> String {
        let api_key = env::var("API_KEY").unwrap_or_else(|_| "dev-key-12345".to_string());
        format!("Bearer {}", api_key)
    }

    fn init_test_db(config: &AppConfig) {
        // Remove the old database file if it exists
        let _ = std::fs::remove_file(&config.database_url);

        let conn = database::get_connection(&config.database_url)
            .expect("Failed to connect to test database");

        let schema = vec![
            "CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                schedule_time TEXT NOT NULL,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )",
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
            "CREATE TABLE IF NOT EXISTS vitals_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL,
                heart_rate INTEGER,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )",
        ];

        for sql in schema {
            conn.execute(sql, []).expect("Failed to create test table");
        }
    }

    #[actix_web::test]
    async fn test_get_medications_empty() {
        let config = get_test_config();
        init_test_db(&config);

        let app = test::init_service(
            App::new()
                .app_data(web::Data::new(config))
                .route("/medications", web::get().to(get_medications)),
        )
        .await;

        let req = test::TestRequest::get()
            .uri("/medications")
            .insert_header((header::AUTHORIZATION, auth_header_value()))
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_success());
    }

    #[actix_web::test]
    async fn test_create_medication_valid() {
        let config = get_test_config();
        init_test_db(&config);

        let app = test::init_service(
            App::new()
                .app_data(web::Data::new(config))
                .route("/medications", web::post().to(create_medication)),
        )
        .await;

        let medication = serde_json::json!({
            "name": "Test Medication",
            "schedule_time": "08:00"
        });

        let req = test::TestRequest::post()
            .uri("/medications")
            .insert_header((header::AUTHORIZATION, auth_header_value()))
            .set_json(&medication)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_success() || resp.status().is_redirection());
    }

    #[actix_web::test]
    async fn test_create_medication_invalid_time() {
        let config = get_test_config();
        init_test_db(&config);

        let app = test::init_service(
            App::new()
                .app_data(web::Data::new(config))
                .route("/medications", web::post().to(create_medication)),
        )
        .await;

        let medication = serde_json::json!({
            "name": "Test Medication",
            "schedule_time": "25:00" // Invalid time
        });

        let req = test::TestRequest::post()
            .uri("/medications")
            .insert_header((header::AUTHORIZATION, auth_header_value()))
            .set_json(&medication)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_client_error()); // Should return 400 Bad Request
    }

    #[actix_web::test]
    async fn test_create_vitals_valid() {
        let config = get_test_config();
        init_test_db(&config);

        let app = test::init_service(
            App::new()
                .app_data(web::Data::new(config))
                .route("/vitals", web::post().to(create_vitals)),
        )
        .await;

        let vitals = serde_json::json!({
            "temperature": 36.5,
            "heart_rate": 72,
            "status": "normal"
        });

        let req = test::TestRequest::post()
            .uri("/vitals")
            .insert_header((header::AUTHORIZATION, auth_header_value()))
            .set_json(&vitals)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_success() || resp.status().is_redirection());
    }

    #[actix_web::test]
    async fn test_create_vitals_invalid_range() {
        let config = get_test_config();
        init_test_db(&config);

        let app = test::init_service(
            App::new()
                .app_data(web::Data::new(config))
                .route("/vitals", web::post().to(create_vitals)),
        )
        .await;

        let vitals = serde_json::json!({
            "temperature": 100.0, // Invalid temperature
            "heart_rate": 72,
            "status": "normal"
        });

        let req = test::TestRequest::post()
            .uri("/vitals")
            .insert_header((header::AUTHORIZATION, auth_header_value()))
            .set_json(&vitals)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_client_error()); // Should return 400 Bad Request
    }
}
