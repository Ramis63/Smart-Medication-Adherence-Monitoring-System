use serde::Deserialize;
use std::env;

#[derive(Clone, Deserialize)]
pub struct AppConfig {
    pub host: String,
    pub port: u16,
    pub database_url: String,
    #[allow(dead_code)]
    pub log_level: String,
}

impl AppConfig {
    pub fn from_env() -> Result<Self, config::ConfigError> {
        // Try to load from .env file first
        let _ = dotenv::dotenv();

        // Use Config::builder() which is more straightforward
        let mut config = config::Config::builder()
            .set_default("host", "127.0.0.1")?
            .set_default("port", 8080)?
            .set_default("database_url", "medhealth.db")?
            .set_default("log_level", "info")?;

        // Override with environment variables
        if let Ok(host) = env::var("HOST") {
            config = config.set_override("host", host)?;
        }
        if let Ok(port) = env::var("PORT") {
            config = config.set_override("port", port.parse::<u16>().unwrap_or(8080))?;
        }
        if let Ok(db_url) = env::var("DATABASE_URL") {
            config = config.set_override("database_url", db_url)?;
        }
        if let Ok(log_level) = env::var("LOG_LEVEL") {
            config = config.set_override("log_level", log_level)?;
        }

        config.build()?.try_deserialize()
    }
}
