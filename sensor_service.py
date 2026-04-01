import time
import random
from flask import Flask, jsonify
from prometheus_client import Counter, Gauge, Histogram, generate_latest

app = Flask(__name__)

# Reduced from 5MB to 500KB to save memory
data_blob = "X" * 500_000

REQUEST_COUNT = Counter("sensor_requests_total", "Total sensor requests")
CPU_SPIKE = Gauge("sensor_cpu_spike", "Simulated CPU spike state")
PROCESS_LATENCY = Histogram("sensor_processing_latency_seconds", "Processing time")
LARGE_DATA_RETURNS = Counter("sensor_large_data_returns_total", "Total large data returns")
SENSOR_DATA_SIZE = Histogram("sensor_data_size_bytes", "Size of sensor data returned")

@app.route("/metrics")
def metrics():
    start = time.time()
    # Reduced busy loop from 2M to 20K iterations to reduce CPU spike and scrape delay
    for _ in range(20000):
        pass
    # Reduced memory allocation: only multiply by 1
    temp_data = data_blob * 1
    PROCESS_LATENCY.observe(time.time() - start)
    CPU_SPIKE.set(random.randint(0, 1))
    REQUEST_COUNT.inc()
    return generate_latest()

@app.route("/sensor")
def sensor():
    if random.random() < 0.2:
        LARGE_DATA_RETURNS.inc()
        SENSOR_DATA_SIZE.observe(len(data_blob))
        return jsonify({"data": data_blob})
    SENSOR_DATA_SIZE.observe(0)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
