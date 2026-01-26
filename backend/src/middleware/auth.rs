// Authentication middleware for API key validation
// This module provides authentication infrastructure
// For production use, enable authentication by wrapping routes with auth_middleware()

use actix_web::dev::ServiceRequest;
use std::env;

// Simple API key check function
// This can be used in handlers to validate API keys
#[allow(dead_code)]
pub fn check_api_key(req: &ServiceRequest) -> bool {
    if let Some(auth_header) = req.headers().get("Authorization") {
        if let Ok(auth_str) = auth_header.to_str() {
            if auth_str.starts_with("Bearer ") {
                let token = &auth_str[7..];
                let api_key = env::var("API_KEY").unwrap_or_else(|_| "dev-key-12345".to_string());
                return token == api_key;
            }
        }
    }
    false
}

// Extract API key from request header
#[allow(dead_code)]
pub fn get_api_key_from_request(req: &ServiceRequest) -> Option<String> {
    if let Some(auth_header) = req.headers().get("Authorization") {
        if let Ok(auth_str) = auth_header.to_str() {
            if auth_str.starts_with("Bearer ") {
                return Some(auth_str[7..].to_string());
            }
        }
    }
    None
}

// Validate API key
#[allow(dead_code)]
pub fn validate_api_key(token: &str) -> bool {
    let api_key = env::var("API_KEY").unwrap_or_else(|_| "dev-key-12345".to_string());
    token == api_key
}

// Note: Full HttpAuthentication middleware is available but requires proper configuration
// For now, use check_api_key() in handlers for simple authentication
// Example usage in handler:
//   if !middleware::auth::check_api_key(&req) {
//       return Err(actix_web::error::ErrorUnauthorized("Invalid API key"));
//   }
