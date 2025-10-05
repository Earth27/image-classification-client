# Image Prediction API Client

A Python client to send images to a REST API for predictions and optionally measure request latency.
This tool encodes images in Base64, sends them to a server endpoint, and stores the prediction results or latency metrics in a JSON file.

---

## Features

* Send images to a REST API (`/predict` endpoint).
* Receive and store prediction results in JSON format.
* Measure request latency across multiple requests.
* Compute 75th, 90th, 95th, and 99th percentile latency.

---

## Requirements

* Python 3.7+
* [absl-py](https://abseil.io/docs/python/guides/flags)
* requests
* numpy

Install dependencies:

```bash
pip install absl-py requests numpy
```

---

## Usage

Run the script with the required flags:

```bash
python client.py \
  --hostname http://localhost \
  --port 8501 \
  --input_image_file ./sample.jpg \
  --output_result_file ./results.json
```

### Options

* `--hostname`: The hostname of the REST API server (default: `http://localhost`).
* `--port`: The port of the REST API server (required).
* `--input_image_file`: Path to the input image file (required).
* `--output_result_file`: Path to save prediction or latency results (required).
* `--num_of_requests`: Number of requests to send (default: `1`).

  * If set to more than `1`, latency percentiles will be computed instead of prediction results.

---

## Examples

### Single Prediction

```bash
python client.py \
  --hostname http://localhost \
  --port 8501 \
  --input_image_file ./dog.jpg \
  --output_result_file ./prediction.json
```

### Latency Benchmark

```bash
python client.py \
  --hostname http://localhost \
  --port 8501 \
  --input_image_file ./dog.jpg \
  --output_result_file ./latency.json \
  --num_of_requests 50
```

---

## Output

* **Prediction mode**: JSON file with model prediction results.
* **Latency mode**: JSON file with latency percentiles (75th, 90th, 95th, 99th).

---

