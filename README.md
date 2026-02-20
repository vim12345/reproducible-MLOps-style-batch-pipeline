# 🚀 MLOps Engineering Internship – Technical Assessment

## 📌 Overview

This project implements a **reproducible MLOps-style batch pipeline** for processing cryptocurrency OHLCV data and generating trading signals using rolling statistical analysis.

The pipeline demonstrates core MLOps principles including:

- Deterministic execution
- Configuration-driven workflow
- Structured logging
- Machine-readable metrics
- Dockerized deployment
- Robust error handling

---

## Setup
pip install -r requirements.txt

## Run Locally
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

## Docker
docker build -t mlops-task .
docker run --rm mlops-task

## Output
metrics.json and run.log generated automatically.

## Dependencies
- pandas
- numpy
- pyyaml

## ⚙️ Project Architecture
CLI → Config Loader → Data Validation
↓
Rolling Mean Calculation
↓
Signal Generation
↓
Metrics + Logging
↓
JSON Output

## 📂 Project Structure

mlops-task/
│
├── run.py # Main pipeline script
├── config.yaml # Configuration parameters
├── data.csv # Cryptocurrency OHLCV dataset
├── requirements.txt # Python dependencies
├── Dockerfile # Container setup
├── metrics.json # Example output
├── run.log # Example execution log
└── README.md

---

## 🧩 Configuration File

`config.yaml`

```yaml
seed: 42
window: 5
version: "v1"

 ## Local Execution
1. Install Dependencies
pip install -r requirements.txt
2. Run Pipeline
python run.py \
--input data.csv \
--config config.yaml \
--output metrics.json \
--log-file run.log
## 🐳 Docker Execution 
1. Build Docker Image
docker build -t mlops-task .
2. Run Container
docker run --rm mlops-task

