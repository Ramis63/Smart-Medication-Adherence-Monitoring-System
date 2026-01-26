use crate::config::AppConfig;
use crate::database;
use crate::models::{MedicationLog, MedicationStatement, Observation, VitalsLog};
use actix::prelude::*;
use actix_web::{web, Error, HttpRequest, HttpResponse};
use actix_web_actors::ws;
use std::time::{Duration, Instant};

// WebSocket actor for medication updates
pub struct MedicationWebSocket {
    hb: Instant,
    last_update: Instant,
    database_url: String,
}

impl Actor for MedicationWebSocket {
    type Context = ws::WebsocketContext<Self>;

    fn started(&mut self, ctx: &mut Self::Context) {
        self.hb(ctx);
    }
}

impl StreamHandler<Result<ws::Message, ws::ProtocolError>> for MedicationWebSocket {
    fn handle(&mut self, msg: Result<ws::Message, ws::ProtocolError>, ctx: &mut Self::Context) {
        match msg {
            Ok(ws::Message::Ping(msg)) => {
                self.hb = Instant::now();
                ctx.pong(&msg);
            }
            Ok(ws::Message::Pong(_)) => {
                self.hb = Instant::now();
            }
            Ok(ws::Message::Text(text)) => {
                // Echo back or handle message
                ctx.text(text);
            }
            Ok(ws::Message::Binary(bin)) => {
                // Handle binary data for efficient transmission
                ctx.binary(bin);
            }
            Ok(ws::Message::Close(reason)) => {
                ctx.close(reason);
                ctx.stop();
            }
            _ => ctx.stop(),
        }
    }
}

impl MedicationWebSocket {
    fn hb(&mut self, ctx: &mut <Self as Actor>::Context) {
        ctx.run_interval(Duration::from_secs(5), |act, ctx| {
            // Send heartbeat or medication updates
            if Instant::now().duration_since(act.hb) > Duration::from_secs(30) {
                ctx.stop();
                return;
            }
            ctx.ping(b"");

            // Fetch and send latest medication updates every 10 seconds
            if Instant::now().duration_since(act.last_update) > Duration::from_secs(10) {
                act.last_update = Instant::now();

                if let Ok(conn) = database::get_connection(&act.database_url) {
                    let stmt = conn.prepare(
                        "SELECT id, medication_id, medication_name, scheduled_time, actual_time, status, temperature, heart_rate, created_at
                         FROM medication_logs
                         ORDER BY created_at DESC
                         LIMIT 5"
                    ).ok();

                    if let Some(mut stmt) = stmt {
                        let logs: Result<Vec<MedicationLog>, _> = stmt.query_map([], |row| {
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
                        }).and_then(|iter| iter.collect());

                        if let Ok(logs) = logs {
                            let statements: Vec<MedicationStatement> = logs.iter()
                                .map(MedicationStatement::from_db_log)
                                .collect();

                            if let Ok(json) = serde_json::to_string(&statements) {
                                ctx.text(json);
                            }
                        }
                    }
                }
            }
        });
    }
}

pub async fn medication_websocket(
    req: HttpRequest,
    stream: web::Payload,
    config: web::Data<AppConfig>,
) -> Result<HttpResponse, Error> {
    let resp = ws::start(
        MedicationWebSocket {
            hb: Instant::now(),
            last_update: Instant::now(),
            database_url: config.database_url.clone(),
        },
        &req,
        stream,
    )?;
    Ok(resp)
}

// WebSocket actor for vital signs updates
pub struct VitalsWebSocket {
    hb: Instant,
    last_update: Instant,
    database_url: String,
}

impl Actor for VitalsWebSocket {
    type Context = ws::WebsocketContext<Self>;

    fn started(&mut self, ctx: &mut Self::Context) {
        self.hb(ctx);
    }
}

impl StreamHandler<Result<ws::Message, ws::ProtocolError>> for VitalsWebSocket {
    fn handle(&mut self, msg: Result<ws::Message, ws::ProtocolError>, ctx: &mut Self::Context) {
        match msg {
            Ok(ws::Message::Ping(msg)) => {
                self.hb = Instant::now();
                ctx.pong(&msg);
            }
            Ok(ws::Message::Pong(_)) => {
                self.hb = Instant::now();
            }
            Ok(ws::Message::Text(text)) => {
                ctx.text(text);
            }
            Ok(ws::Message::Binary(bin)) => {
                // Handle binary data for efficient transmission
                ctx.binary(bin);
            }
            Ok(ws::Message::Close(reason)) => {
                ctx.close(reason);
                ctx.stop();
            }
            _ => ctx.stop(),
        }
    }
}

impl VitalsWebSocket {
    fn hb(&mut self, ctx: &mut <Self as Actor>::Context) {
        ctx.run_interval(Duration::from_secs(5), |act, ctx| {
            if Instant::now().duration_since(act.hb) > Duration::from_secs(30) {
                ctx.stop();
                return;
            }
            ctx.ping(b"");

            // Fetch and send latest vital signs every 10 seconds
            if Instant::now().duration_since(act.last_update) > Duration::from_secs(10) {
                act.last_update = Instant::now();

                if let Ok(conn) = database::get_connection(&act.database_url) {
                    let stmt = conn
                        .prepare(
                            "SELECT id, temperature, heart_rate, status, created_at
                         FROM vitals_logs
                         ORDER BY created_at DESC
                         LIMIT 5",
                        )
                        .ok();

                    if let Some(mut stmt) = stmt {
                        let logs: Result<Vec<VitalsLog>, _> = stmt
                            .query_map([], |row| {
                                Ok(VitalsLog {
                                    id: row.get(0)?,
                                    temperature: row.get(1)?,
                                    heart_rate: row.get(2)?,
                                    status: row.get(3)?,
                                    created_at: row.get(4)?,
                                })
                            })
                            .and_then(|iter| iter.collect());

                        if let Ok(logs) = logs {
                            let mut observations = Vec::new();
                            for log in &logs {
                                if let Some(temp_obs) = Observation::temperature_from_db(log) {
                                    observations.push(temp_obs);
                                }
                                if let Some(hr_obs) = Observation::heart_rate_from_db(log) {
                                    observations.push(hr_obs);
                                }
                            }

                            if let Ok(json) = serde_json::to_string(&observations) {
                                ctx.text(json);
                            }
                        }
                    }
                }
            }
        });
    }
}

pub async fn vitals_websocket(
    req: HttpRequest,
    stream: web::Payload,
    config: web::Data<AppConfig>,
) -> Result<HttpResponse, Error> {
    let resp = ws::start(
        VitalsWebSocket {
            hb: Instant::now(),
            last_update: Instant::now(),
            database_url: config.database_url.clone(),
        },
        &req,
        stream,
    )?;
    Ok(resp)
}
