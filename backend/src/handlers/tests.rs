#[cfg(test)]
mod tests {
    use super::{create_medication, create_vitals, get_medications};
    use crate::config::AppConfig;
    use crate::database;
    use actix_web::{test, web, App};

    fn get_test_config() -> AppConfig {
        AppConfig {
            host: "127.0.0.1".to_string(),
            port: 8080,
            database_url: ":memory:".to_string(), // In-memory database for tests
            log_level: "test".to_string(),
        }
    }

    #[actix_web::test]
    async fn test_get_medications_empty() {
        let config = get_test_config();
        // Initialize test database
        database::init_db(&config.database_url).unwrap();

        let app = test::init_service(
            App::new()
                .app_data(web::Data::new(config))
                .route("/medications", web::get().to(get_medications)),
        )
        .await;

        let req = test::TestRequest::get().uri("/medications").to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_success());
    }

    #[actix_web::test]
    async fn test_create_medication_valid() {
        let config = get_test_config();
        database::init_db(&config.database_url).unwrap();

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
            .set_json(&medication)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_success() || resp.status().is_redirection());
    }

    #[actix_web::test]
    async fn test_create_medication_invalid_time() {
        let config = get_test_config();
        database::init_db(&config.database_url).unwrap();

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
            .set_json(&medication)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_client_error()); // Should return 400 Bad Request
    }

    #[actix_web::test]
    async fn test_create_vitals_valid() {
        let config = get_test_config();
        database::init_db(&config.database_url).unwrap();

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
            .set_json(&vitals)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_success() || resp.status().is_redirection());
    }

    #[actix_web::test]
    async fn test_create_vitals_invalid_range() {
        let config = get_test_config();
        database::init_db(&config.database_url).unwrap();

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
            .set_json(&vitals)
            .to_request();
        let resp = test::call_service(&app, req).await;

        assert!(resp.status().is_client_error()); // Should return 400 Bad Request
    }
}
