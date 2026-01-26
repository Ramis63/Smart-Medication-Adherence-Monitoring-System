#[cfg(test)]
mod tests {
    use super::*;
    use chrono::Utc;

    #[test]
    fn test_medication_statement_from_db_log() {
        let log = MedicationLog {
            id: 1,
            medication_id: Some(1),
            medication_name: "Aspirin".to_string(),
            scheduled_time: "2024-01-13 08:00:00".to_string(),
            actual_time: "2024-01-13 08:05:00".to_string(),
            status: "taken".to_string(),
            temperature: Some(36.5),
            heart_rate: Some(72),
            created_at: "2024-01-13T08:05:00Z".to_string(),
        };

        let statement = MedicationStatement::from_db_log(&log);
        
        assert_eq!(statement.resource_type, "MedicationStatement");
        assert_eq!(statement.medication.display, "Aspirin");
        assert!(statement.id.len() > 0);
    }

    #[test]
    fn test_observation_temperature_from_db() {
        let log = VitalsLog {
            id: 1,
            temperature: Some(36.7),
            heart_rate: Some(75),
            status: "normal".to_string(),
            created_at: "2024-01-13T10:00:00Z".to_string(),
        };

        let obs = Observation::temperature_from_db(&log);
        assert!(obs.is_some());
        
        let observation = obs.unwrap();
        assert_eq!(observation.resource_type, "Observation");
        assert_eq!(observation.code.coding[0].code, "8310-5");
        assert_eq!(observation.value_quantity.as_ref().unwrap().value, 36.7);
    }

    #[test]
    fn test_observation_heart_rate_from_db() {
        let log = VitalsLog {
            id: 1,
            temperature: Some(36.7),
            heart_rate: Some(75),
            status: "normal".to_string(),
            created_at: "2024-01-13T10:00:00Z".to_string(),
        };

        let obs = Observation::heart_rate_from_db(&log);
        assert!(obs.is_some());
        
        let observation = obs.unwrap();
        assert_eq!(observation.resource_type, "Observation");
        assert_eq!(observation.code.coding[0].code, "8867-4");
        assert_eq!(observation.value_quantity.as_ref().unwrap().value, 75.0);
    }

    #[test]
    fn test_medication_status_mapping() {
        let taken_log = MedicationLog {
            id: 1,
            medication_id: Some(1),
            medication_name: "Test".to_string(),
            scheduled_time: "2024-01-13 08:00:00".to_string(),
            actual_time: "2024-01-13 08:05:00".to_string(),
            status: "taken".to_string(),
            temperature: None,
            heart_rate: None,
            created_at: "2024-01-13T08:05:00Z".to_string(),
        };

        let missed_log = MedicationLog {
            id: 2,
            medication_id: Some(1),
            medication_name: "Test".to_string(),
            scheduled_time: "2024-01-13 08:00:00".to_string(),
            actual_time: "2024-01-13 08:00:00".to_string(),
            status: "missed".to_string(),
            temperature: None,
            heart_rate: None,
            created_at: "2024-01-13T08:00:00Z".to_string(),
        };

        let taken_stmt = MedicationStatement::from_db_log(&taken_log);
        let missed_stmt = MedicationStatement::from_db_log(&missed_log);

        match taken_stmt.status {
            MedicationStatus::Completed => {},
            _ => panic!("Taken status should map to Completed"),
        }

        match missed_stmt.status {
            MedicationStatus::NotTaken => {},
            _ => panic!("Missed status should map to NotTaken"),
        }
    }
}

