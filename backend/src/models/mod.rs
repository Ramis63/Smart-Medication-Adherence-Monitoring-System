use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[cfg(test)]
mod tests;

// FHIR-compliant MedicationStatement
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct MedicationStatement {
    #[serde(rename = "resourceType")]
    pub resource_type: String,
    pub id: String,
    pub status: MedicationStatus,
    pub medication: MedicationReference,
    pub subject: SubjectReference,
    #[serde(rename = "effectiveDateTime")]
    pub effective_date_time: DateTime<Utc>,
    pub dosage: Option<Dosage>,
    pub meta: Option<Meta>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "kebab-case")]
pub enum MedicationStatus {
    Active,
    Completed,
    EnteredInError,
    Intended,
    Stopped,
    OnHold,
    Unknown,
    NotTaken,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct MedicationReference {
    pub reference: String,
    pub display: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct SubjectReference {
    pub reference: String,
    pub display: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Dosage {
    pub timing: Timing,
    pub text: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Timing {
    pub repeat: Repeat,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Repeat {
    pub frequency: i32,
    pub period: f64,
    pub period_unit: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Meta {
    pub version_id: String,
    pub last_updated: DateTime<Utc>,
}

// FHIR-compliant Observation (Vital Signs)
#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct Observation {
    #[serde(rename = "resourceType")]
    pub resource_type: String,
    pub id: String,
    pub status: ObservationStatus,
    pub category: Vec<CodeableConcept>,
    pub code: CodeableConcept,
    pub subject: SubjectReference,
    #[serde(rename = "effectiveDateTime")]
    pub effective_date_time: DateTime<Utc>,
    #[serde(rename = "valueQuantity")]
    pub value_quantity: Option<ValueQuantity>,
    pub meta: Option<Meta>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "kebab-case")]
pub enum ObservationStatus {
    Registered,
    Preliminary,
    Final,
    Amended,
    Corrected,
    Cancelled,
    EnteredInError,
    Unknown,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct CodeableConcept {
    pub coding: Vec<Coding>,
    pub text: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Coding {
    pub system: String,
    pub code: String,
    pub display: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
#[serde(rename_all = "camelCase")]
pub struct ValueQuantity {
    pub value: f64,
    pub unit: String,
    pub system: String,
    pub code: String,
}

// Internal database models
#[derive(Debug, Serialize, Deserialize)]
pub struct Medication {
    pub id: i32,
    pub name: String,
    pub schedule_time: String,
    pub active: bool,
    pub created_at: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct MedicationLog {
    pub id: i32,
    pub medication_id: Option<i32>,
    pub medication_name: String,
    pub scheduled_time: String,
    pub actual_time: String,
    pub status: String,
    pub temperature: Option<f64>,
    pub heart_rate: Option<i32>,
    pub created_at: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct VitalsLog {
    pub id: i32,
    pub temperature: Option<f64>,
    pub heart_rate: Option<i32>,
    pub status: String,
    pub created_at: String,
}

// Conversion functions
impl MedicationStatement {
    pub fn from_db_log(log: &MedicationLog) -> Self {
        let status = match log.status.as_str() {
            "taken" => MedicationStatus::Completed,
            "missed" => MedicationStatus::NotTaken,
            _ => MedicationStatus::Unknown,
        };

        MedicationStatement {
            resource_type: "MedicationStatement".to_string(),
            id: Uuid::new_v4().to_string(),
            status,
            medication: MedicationReference {
                reference: format!("Medication/{}", log.medication_id.unwrap_or(0)),
                display: log.medication_name.clone(),
            },
            subject: SubjectReference {
                reference: "Patient/1".to_string(),
                display: "Patient".to_string(),
            },
            effective_date_time: DateTime::parse_from_rfc3339(&log.created_at)
                .map(|dt| dt.with_timezone(&Utc))
                .unwrap_or_else(|_| Utc::now()),
            dosage: None,
            meta: Some(Meta {
                version_id: "1".to_string(),
                last_updated: Utc::now(),
            }),
        }
    }
}

impl Observation {
    pub fn temperature_from_db(log: &VitalsLog) -> Option<Self> {
        log.temperature.map(|temp| Observation {
            resource_type: "Observation".to_string(),
            id: Uuid::new_v4().to_string(),
            status: ObservationStatus::Final,
            category: vec![CodeableConcept {
                coding: vec![Coding {
                    system: "http://terminology.hl7.org/CodeSystem/observation-category"
                        .to_string(),
                    code: "vital-signs".to_string(),
                    display: "Vital Signs".to_string(),
                }],
                text: "Vital Signs".to_string(),
            }],
            code: CodeableConcept {
                coding: vec![Coding {
                    system: "http://loinc.org".to_string(),
                    code: "8310-5".to_string(),
                    display: "Body temperature".to_string(),
                }],
                text: "Body Temperature".to_string(),
            },
            subject: SubjectReference {
                reference: "Patient/1".to_string(),
                display: "Patient".to_string(),
            },
            effective_date_time: DateTime::parse_from_rfc3339(&log.created_at)
                .map(|dt| dt.with_timezone(&Utc))
                .unwrap_or_else(|_| Utc::now()),
            value_quantity: Some(ValueQuantity {
                value: temp,
                unit: "Cel".to_string(),
                system: "http://unitsofmeasure.org".to_string(),
                code: "Cel".to_string(),
            }),
            meta: Some(Meta {
                version_id: "1".to_string(),
                last_updated: Utc::now(),
            }),
        })
    }

    pub fn heart_rate_from_db(log: &VitalsLog) -> Option<Self> {
        log.heart_rate.map(|hr| Observation {
            resource_type: "Observation".to_string(),
            id: Uuid::new_v4().to_string(),
            status: ObservationStatus::Final,
            category: vec![CodeableConcept {
                coding: vec![Coding {
                    system: "http://terminology.hl7.org/CodeSystem/observation-category"
                        .to_string(),
                    code: "vital-signs".to_string(),
                    display: "Vital Signs".to_string(),
                }],
                text: "Vital Signs".to_string(),
            }],
            code: CodeableConcept {
                coding: vec![Coding {
                    system: "http://loinc.org".to_string(),
                    code: "8867-4".to_string(),
                    display: "Heart rate".to_string(),
                }],
                text: "Heart Rate".to_string(),
            },
            subject: SubjectReference {
                reference: "Patient/1".to_string(),
                display: "Patient".to_string(),
            },
            effective_date_time: DateTime::parse_from_rfc3339(&log.created_at)
                .map(|dt| dt.with_timezone(&Utc))
                .unwrap_or_else(|_| Utc::now()),
            value_quantity: Some(ValueQuantity {
                value: hr as f64,
                unit: "/min".to_string(),
                system: "http://unitsofmeasure.org".to_string(),
                code: "/min".to_string(),
            }),
            meta: Some(Meta {
                version_id: "1".to_string(),
                last_updated: Utc::now(),
            }),
        })
    }
}
