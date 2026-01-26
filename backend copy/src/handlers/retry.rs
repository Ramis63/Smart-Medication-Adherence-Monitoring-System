// Retry logic for database operations

use std::time::Duration;
use std::thread;

/// Retry a database operation with exponential backoff
pub fn retry_db_operation<F, T, E>(mut operation: F, max_retries: u32) -> Result<T, E>
where
    F: FnMut() -> Result<T, E>,
{
    let mut retries = 0;
    let mut delay = Duration::from_millis(100);
    
    loop {
        match operation() {
            Ok(result) => return Ok(result),
            Err(e) => {
                if retries >= max_retries {
                    return Err(e);
                }
                
                retries += 1;
                thread::sleep(delay);
                delay *= 2; // Exponential backoff
            }
        }
    }
}

/// Retry with custom delay
pub fn retry_with_delay<F, T, E>(
    mut operation: F,
    max_retries: u32,
    initial_delay_ms: u64,
) -> Result<T, E>
where
    F: FnMut() -> Result<T, E>,
{
    let mut retries = 0;
    let mut delay = Duration::from_millis(initial_delay_ms);
    
    loop {
        match operation() {
            Ok(result) => return Ok(result),
            Err(e) => {
                if retries >= max_retries {
                    return Err(e);
                }
                
                retries += 1;
                thread::sleep(delay);
                delay *= 2;
            }
        }
    }
}

