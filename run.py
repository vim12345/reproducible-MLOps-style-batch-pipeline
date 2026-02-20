import argparse
import pandas as pd
import numpy as np
import yaml
import json
import logging
import time
import os
import sys

def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def load_config(path):
    if not os.path.exists(path):
        raise FileNotFoundError("Config file missing")
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    required = ["seed", "window", "version"]
    for key in required:
        if key not in config:
            raise ValueError("Invalid configuration structure")
    return config

def process_data(input_file, window):
    if not os.path.exists(input_file):
        raise FileNotFoundError("Input CSV not found")
    df = pd.read_csv(input_file)
    if df.empty:
        raise ValueError("Input CSV is empty")
    if "close" not in df.columns:
        raise ValueError("Missing required column: close")
    logging.info(f"Data loaded: {len(df)} rows")
    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    logging.info(f"Rolling mean calculated with window={window}")
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
    logging.info("Signals generated")
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)
    args = parser.parse_args()
    setup_logger(args.log_file)
    start_time = time.time()
    try:
        logging.info("Job started")
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]
        np.random.seed(seed)
        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")
        df = process_data(args.input, window)
        rows_processed = len(df)
        signal_rate = df["signal"].mean()
        latency_ms = int((time.time() - start_time) * 1000)
        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success",
        }
        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)
        logging.info(f"Metrics: signal_rate={signal_rate}, rows_processed={rows_processed}")
        logging.info(f"Job completed successfully in {latency_ms}ms")
        print(json.dumps(metrics, indent=4))
        sys.exit(0)
    except Exception as e:
        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e),
        }
        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=4)
        logging.error(str(e))
        print(json.dumps(error_output, indent=4))
        sys.exit(1)

if __name__ == "__main__":
    main()
