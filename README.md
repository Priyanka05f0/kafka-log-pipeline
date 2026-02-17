# Kafka Log Processing Pipeline

## Overview

This project implements a containerized log processing pipeline using Apache Kafka, Docker, and Python.

The system consists of:

- **Producer Service** – Generates synthetic application logs and publishes them to a Kafka topic.
- **Kafka Broker** – Message broker for streaming logs.
- **Consumer Service** – Consumes logs from Kafka, filters ERROR and WARN logs, and stores them locally.
- **Zookeeper** – Required for Kafka coordination.

The entire pipeline runs using Docker Compose.

---

## Architecture

Producer → Kafka Topic (`application-logs`) → Consumer → JSONL Output File

- Logs are generated as JSON objects.
- Consumer filters logs based on `LOG_LEVEL_FILTER`.
- Filtered logs are stored in `processed_errors_warnings.jsonl`.

---

## Technologies Used

- Python 3.10
- Apache Kafka (Confluent 7.5.0)
- Docker & Docker Compose
- Pytest (Unit Testing)

---

## Project Structure
```
kafka-log-pipeline/
│
├── docker-compose.yml
├── README.md
├── .env.example
├── output/
│
├── src/
│ ├── producer/
│ │ ├── producer.py
│ │ ├── Dockerfile
│ │ └── requirements.txt
│ │
│ └── consumer/
│ ├── consumer.py
│ ├── Dockerfile
│ └── requirements.txt
│
└── tests/
└── test_consumer.py
```

---

## Environment Variables

| Variable | Description | Default |
|----------|------------|---------|
| KAFKA_BROKER_URL | Kafka broker address | kafka:9092 |
| KAFKA_TOPIC | Kafka topic name | application-logs |
| MESSAGE_RATE | Logs per second | 1 |
| LOG_LEVEL_FILTER | Levels to store | ERROR,WARN |
| OUTPUT_FILE_PATH | Output file name | processed_errors_warnings.jsonl |

---

## Setup Instructions

### 1️⃣ Install Prerequisites

- Install Docker Desktop
- Ensure Docker Compose is available:
```bash
docker --version
docker compose version
```

---

### 2️⃣ Build and Run the Pipeline

From project root:
```bash
docker compose up --build -d
```
To verify containers:
```bash
docker compose ps
```

You should see:
- zookeeper
- kafka
- producer
- consumer

---

### 3️⃣ View Logs

Producer logs:
```bash
docker compose logs producer
```
Consumer logs:
```bash
docker compose logs consumer
```
---

### 4️⃣ Verify Output File

Filtered logs are saved to:
```
output/processed_errors_warnings.jsonl
```
To view:
```bash
cat output/processed_errors_warnings.jsonl
```

You should see only ERROR and WARN logs.

---

## Unit Testing

Unit tests are implemented for the log filtering logic.

Run locally:
```bash
pytest
```
Expected result:
4 passed

Tests cover:
- Valid ERROR logs
- Valid WARN logs
- INFO logs (should not pass filter)
- Invalid log objects

---

## Graceful Shutdown

Both Producer and Consumer handle:

- SIGINT
- SIGTERM

When stopping containers:
```bash
docker compose down
```

Services close cleanly without data loss.

---

## Error Handling

The consumer includes:

- try/except blocks for JSON deserialization
- Validation for incorrect log format
- Logging of unexpected errors
- Non-blocking message processing

---

## Stop the Pipeline
```bash
docker compose down
```
To remove volumes and clean everything:
```bash
docker compose down -v
```
---

## Troubleshooting

### Kafka not available error
Wait a few seconds. The consumer includes retry logic.

### No logs appearing
Check:
```bash
docker compose logs producer
```

### Output file not updating
Ensure volume is mounted in docker-compose.yml and check consumer logs.

---

## Submission Notes

This repository contains:

- Complete source code for Producer and Consumer
- Dockerfiles for both services
- docker-compose configuration
- Unit tests
- Graceful shutdown implementation
- Environment variable documentation

All requirements from Phase 1, Phase 2, and Phase 3 have been implemented.

---