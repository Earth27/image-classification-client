from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import base64
import json
import time

from absl import app
from absl import flags
import numpy as np
import requests

flags.DEFINE_string('hostname', 'http://localhost', 'The hostname for serving.')
flags.DEFINE_string('input_image_file', None, 'The input image file name.')
flags.DEFINE_string('output_result_file', None, 'The prediction output file name.')
flags.DEFINE_integer('port', None, 'The port of rest api.')
flags.DEFINE_integer('num_of_requests', 1, 'The number of requests to send.')

FLAGS = flags.FLAGS

def create_request_body(input_image_file):
    """Creates the request body to perform API calls.

    Args:
        input_image_file: String, the input image file name.

    Returns:
        A JSON string with base64-encoded image bytes:
        {"image_bytes": "<BASE64_IMAGE_BYTES>"}
    """
    with open(input_image_file, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    request_body = {'image_bytes': encoded_string}
    return json.dumps(request_body)


def predict(hostname, input_image_file, port):
    """Sends a single prediction request to the server."""
    url = f"{hostname}:{port}/predict"
    headers = {"Content-Type": "application/json"}
    data = create_request_body(input_image_file)

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def compute_latency_percentile(hostname, input_image_file, port, num_requests):
    """Sends multiple requests and computes latency percentiles."""
    latency_list = []

    for _ in range(num_requests):
        start = time.time()
        predict(hostname, input_image_file, port)
        end = time.time()
        latency_list.append(end - start)

    latency_percentile = {}
    percentiles = [75, 90, 95, 99]
    for percentile in percentiles:
        latency_percentile[percentile] = np.percentile(latency_list, percentile)

    return latency_percentile


def main(_):
    if FLAGS.num_of_requests > 1:
        latency_percentile = compute_latency_percentile(
            FLAGS.hostname,
            FLAGS.input_image_file,
            FLAGS.port,
            FLAGS.num_of_requests
        )
        print(latency_percentile)
        with open(FLAGS.output_result_file, 'w+') as latency_result:
            latency_result.write(json.dumps(latency_percentile))
    else:
        start = time.time()
        results = predict(FLAGS.hostname, FLAGS.input_image_file, FLAGS.port)
        end = time.time()
        print('Processed image {} in {:.3f}s.'.format(FLAGS.input_image_file, end - start))
        print(json.dumps(results, indent=2))
        with open(FLAGS.output_result_file, 'w+') as prediction_result:
            prediction_result.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    flags.mark_flag_as_required('input_image_file')
    flags.mark_flag_as_required('port')
    flags.mark_flag_as_required('output_result_file')
    app.run(main)
