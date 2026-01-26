use actix_web::{web, App, HttpServer, Result, HttpResponse};
use actix_web::middleware::Logger;
use actix_cors::Cors;
use log::info;

mod handlers;
mod models;
mod database;
mod websocket;
mod config;
mod middleware;

use config::AppConfig;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Initialize logger
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));
    
    // Load configuration
    let config = AppConfig::from_env().expect("Failed to load configuration");
    
    info!("Starting MedHealth Backend Server");
    info!("Database: {}", config.database_url);
    info!("Server will run on: {}:{}", config.host, config.port);
    
    // Initialize database
    database::init_db(&config.database_url)
        .expect("Failed to initialize database");
    
    let config_data = web::Data::new(config.clone());
    
    HttpServer::new(move || {
        App::new()
            .app_data(config_data.clone())
            .wrap(Logger::default())
            .wrap(
                Cors::permissive()
                    .allowed_origin("http://localhost:3000")
                    .allowed_origin("http://127.0.0.1:3000")
                    .allowed_methods(vec!["GET", "POST", "DELETE", "OPTIONS"])
                    .allowed_headers(vec![
                        actix_web::http::header::AUTHORIZATION,
                        actix_web::http::header::ACCEPT,
                    ])
                    .allowed_header(actix_web::http::header::CONTENT_TYPE)
                    .supports_credentials()
            )
            .service(
                web::scope("/api")
                    .route("/health", web::get().to(health_check))
                    .service(
                        web::scope("/medications")
                            .route("", web::get().to(handlers::get_medications))
                            .route("", web::post().to(handlers::create_medication))
                            .route("/{id}", web::get().to(handlers::get_medication))
                            .route("/{id}", web::delete().to(handlers::delete_medication))
                            .route("/{id}/logs", web::get().to(handlers::get_medication_logs))
                    )
                    .service(
                        web::scope("/vitals")
                            .route("", web::get().to(handlers::get_vitals))
                            .route("", web::post().to(handlers::create_vitals))
                    )
                    .service(
                        web::scope("/logs")
                            .route("/medications", web::get().to(handlers::get_all_medication_logs))
                            .route("/vitals", web::get().to(handlers::get_all_vitals_logs))
                    )
            )
            .service(
                web::scope("/ws")
                    .app_data(config_data.clone())
                    .route("/medications", web::get().to(websocket::medication_websocket))
                    .route("/vitals", web::get().to(websocket::vitals_websocket))
            )
    })
    .bind(format!("{}:{}", config.host, config.port))?
    .run()
    .await
}

async fn health_check() -> Result<HttpResponse> {
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "status": "healthy",
        "service": "medhealth-backend",
        "version": "0.1.0"
    })))
}


